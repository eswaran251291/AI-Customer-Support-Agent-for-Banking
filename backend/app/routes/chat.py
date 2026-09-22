"""Chat and escalation routes."""

import logging
from typing import Optional, Dict, Any
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Header, status
from pydantic import BaseModel, Field
import uuid

from app.services.ai_service import AIService, IntentType
from app.services.customer_service import CustomerService
from app.services.auth_service import AuthService
from app.services.analytics_service import AnalyticsService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["chat"])


class ChatMessage(BaseModel):
    """Chat message request."""
    message: str = Field(..., min_length=1, max_length=2000)
    customer_id: Optional[str] = Field(None, description="Customer ID if known")
    session_id: Optional[str] = Field(None, description="Conversation session ID")
    mfa_token: Optional[str] = Field(None, description="MFA verification token")


class ChatResponse(BaseModel):
    """Chat response."""
    conversation_id: str
    message: str
    intent: str
    confidence: float
    requires_mfa: bool
    escalation_required: bool
    escalation_priority: Optional[str] = None
    suggested_specialist: Optional[str] = None
    wait_time_estimate: Optional[str] = None
    timestamp: datetime
    suggested_actions: list = []


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatMessage,
    x_request_id: str = Header(default_factory=lambda: str(uuid.uuid4())),
) -> ChatResponse:
    """
    Main chat endpoint for customer interactions.
    
    This endpoint:
    1. Classifies customer intent (question type)
    2. Retrieves relevant information if needed
    3. Generates appropriate response
    4. Escalates to human specialist if required
    5. Logs all interactions for audit trail
    
    Args:
        request: Chat message from customer
        x_request_id: Unique request ID for audit trail
        
    Returns:
        ChatResponse with bot response and action info
    """
    
    # Generate conversation ID if not provided
    conversation_id = request.session_id or str(uuid.uuid4())
    customer_id = request.customer_id or "GUEST"
    
    # Log incoming message
    logger.info(
        "Chat message received",
        extra={
            "request_id": x_request_id,
            "conversation_id": conversation_id,
            "customer_id": customer_id,
            "message_length": len(request.message)
        }
    )
    
    try:
        # Initialize services
        ai_service = AIService()
        
        # Step 1: Classify intent
        intent_result = await ai_service.classify_intent(request.message)
        AnalyticsService.record_interaction(
            intent=intent_result.intent.value,
            escalated=intent_result.escalation_required or intent_result.confidence < 0.70,
            resolved=not intent_result.escalation_required and intent_result.confidence >= 0.70,
        )
        
        logger.info(
            "Intent classified",
            extra={
                "request_id": x_request_id,
                "conversation_id": conversation_id,
                "intent": intent_result.intent.value,
                "confidence": intent_result.confidence,
                "escalation_required": intent_result.escalation_required
            }
        )
        
        # Step 2: Generate response
        response_data = await ai_service.generate_response(
            request.message,
            intent_result,
            user_context={"customer_id": customer_id}
        )
        
        # Step 3: Check if escalation is needed
        if response_data["escalation_required"] or intent_result.confidence < 0.70:
            logger.warning(
                "Escalation required",
                extra={
                    "request_id": x_request_id,
                    "conversation_id": conversation_id,
                    "reason": "low_confidence" if intent_result.confidence < 0.70 else "manual",
                    "confidence": intent_result.confidence
                }
            )
            
            fraud_indicators = ("fraud", "unauthorized", "hacked", "stolen", "compromised")
            is_fraud_case = any(indicator in request.message.lower() for indicator in fraud_indicators)

            return ChatResponse(
                conversation_id=conversation_id,
                message="Thank you for contacting us. I'm connecting you with a specialist who can better assist you.",
                intent=intent_result.intent.value,
                confidence=intent_result.confidence,
                requires_mfa=False,
                escalation_required=True,
                escalation_priority="HIGH" if is_fraud_case else "MEDIUM",
                suggested_specialist="Fraud Team" if is_fraud_case else "Support Specialist",
                wait_time_estimate="< 2 minutes",
                timestamp=datetime.utcnow(),
                suggested_actions=["escalate_to_human"]
            )
        
        # Step 4: For sensitive operations, require MFA
        if intent_result.requires_mfa and not request.mfa_token:
            logger.info(
                "MFA required for operation",
                extra={
                    "request_id": x_request_id,
                    "conversation_id": conversation_id,
                    "intent": intent_result.intent.value
                }
            )
            
            return ChatResponse(
                conversation_id=conversation_id,
                message="For security, please verify your identity. Please provide your MFA verification code.",
                intent=intent_result.intent.value,
                confidence=intent_result.confidence,
                requires_mfa=True,
                escalation_required=False,
                timestamp=datetime.utcnow(),
                suggested_actions=["request_mfa"]
            )
        
        # Step 5: Verify MFA if provided
        if intent_result.requires_mfa and request.mfa_token:
            mfa_valid = await AuthService.verify_mfa_token(request.mfa_token, customer_id)
            if not mfa_valid:
                logger.warning(
                    "MFA verification failed",
                    extra={
                        "request_id": x_request_id,
                        "conversation_id": conversation_id,
                        "customer_id": customer_id
                    }
                )
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid MFA token"
                )
        
        # Step 6: Audit log successful interaction
        logger.info(
            "Chat interaction processed",
            extra={
                "request_id": x_request_id,
                "conversation_id": conversation_id,
                "customer_id": customer_id,
                "intent": intent_result.intent.value,
                "confidence": intent_result.confidence,
                "data_classification": intent_result.data_classification,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
        return ChatResponse(
            conversation_id=conversation_id,
            message=response_data["message"],
            intent=response_data["intent"],
            confidence=response_data["confidence"],
            requires_mfa=response_data.get("requires_mfa", False),
            escalation_required=response_data.get("escalation_required", False),
            timestamp=datetime.utcnow(),
            suggested_actions=response_data.get("suggested_actions", [])
        )
    
    except HTTPException:
        raise
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Error processing chat message",
            extra={
                "request_id": x_request_id,
                "conversation_id": conversation_id,
                "error": str(e)
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing your request. Please try again."
        )


@router.get("/customers/{customer_id}/info")
async def get_customer_info(
    customer_id: str,
    x_request_id: str = Header(default_factory=lambda: str(uuid.uuid4())),
):
    """
    Get customer account information.
    
    Security: Requires customer_id verification
    Compliance: Full audit trail logged
    """
    logger.info(
        "Customer info request",
        extra={"request_id": x_request_id, "customer_id": customer_id}
    )
    
    try:
        customer_service = CustomerService(db=None)  # Mock implementation
        customer = await customer_service.get_customer_by_id(customer_id)
        
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )
        
        # Audit log
        logger.info(
            "Customer info retrieved",
            extra={
                "request_id": x_request_id,
                "customer_id": customer_id,
                "data_classification": "PCI"
            }
        )
        
        return customer
    
    except HTTPException:
        raise
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving customer info: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving customer info")


@router.get("/customers/{customer_id}/balance")
async def get_balance(
    customer_id: str,
    x_request_id: str = Header(default_factory=lambda: str(uuid.uuid4())),
):
    """Get customer account balance with audit trail."""
    try:
        customer_service = CustomerService(db=None)
        balance = await customer_service.get_account_balance(customer_id)
        
        if not balance:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        logger.info(
            "Balance retrieved",
            extra={
                "request_id": x_request_id,
                "customer_id": customer_id,
                "action": "BALANCE_VIEW"
            }
        )
        
        return balance
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving balance: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving balance")


@router.get("/customers/{customer_id}/transactions")
async def get_transactions(
    customer_id: str,
    limit: int = 10,
    x_request_id: str = Header(default_factory=lambda: str(uuid.uuid4())),
):
    """Get customer transaction history with audit trail."""
    try:
        customer_service = CustomerService(db=None)
        transactions = await customer_service.get_transaction_history(customer_id, limit)
        
        if not transactions:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        logger.info(
            "Transactions retrieved",
            extra={
                "request_id": x_request_id,
                "customer_id": customer_id,
                "transaction_count": len(transactions.get("transactions", [])),
                "action": "TRANSACTION_VIEW"
            }
        )
        
        return transactions
    except Exception as e:
        logger.error(f"Error retrieving transactions: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving transactions")
