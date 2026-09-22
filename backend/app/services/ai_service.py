"""AI Service for intent classification and response generation."""

import logging
from typing import Optional, Dict, Any
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
import openai
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class IntentType(str, Enum):
    """Classification of customer intents."""
    ACCOUNT_BALANCE = "account_balance"
    TRANSACTION_HISTORY = "transaction_history"
    TRANSFER_FUNDS = "transfer_funds"
    CARD_MANAGEMENT = "card_management"
    ACCOUNT_SETTINGS = "account_settings"
    FRAUD_REPORT = "fraud_report"
    GENERAL_INQUIRY = "general_inquiry"
    COMPLAINT = "complaint"
    ESCALATION_REQUIRED = "escalation_required"
    UNKNOWN = "unknown"


@dataclass
class IntentClassificationResult:
    """Result of intent classification."""
    intent: IntentType
    confidence: float  # 0.0-1.0
    requires_mfa: bool
    data_classification: str  # PUBLIC, CONFIDENTIAL, PCI
    escalation_required: bool
    reasoning: str


class AIService:
    """Service for AI-powered intent classification and response generation."""
    
    def __init__(self):
        """Initialize AI service."""
        self.openai_api_key = settings.OPENAI_API_KEY
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
        
        # Knowledge base for common queries
        self.knowledge_base = self._load_knowledge_base()
    
    def _load_knowledge_base(self) -> Dict[str, Dict[str, Any]]:
        """Load knowledge base for FAQ responses."""
        return {
            "account_balance": {
                "patterns": [
                    "what is my balance",
                    "how much money do i have",
                    "check my account balance",
                    "current balance",
                    "account balance"
                ],
                "response": "I can help you check your account balance. Let me retrieve that for you.",
                "requires_auth": True,
                "requires_mfa": True,
                "data_classification": "PCI"
            },
            "transaction_history": {
                "patterns": [
                    "show my transactions",
                    "recent transactions",
                    "transaction history",
                    "what did i spend",
                    "where's my money",
                    "view past transactions"
                ],
                "response": "I can show you your recent transactions. Retrieving your history now.",
                "requires_auth": True,
                "requires_mfa": False,
                "data_classification": "PCI"
            },
            "transfer_funds": {
                "patterns": [
                    "send money",
                    "transfer funds",
                    "pay someone",
                    "i want to transfer",
                    "make a payment"
                ],
                "response": "I can help you transfer funds. I'll need to verify your identity first.",
                "requires_auth": True,
                "requires_mfa": True,
                "data_classification": "PCI"
            },
            "card_management": {
                "patterns": [
                    "block my card",
                    "lost card",
                    "replace my card",
                    "card replacement",
                    "freeze card"
                ],
                "response": "I can help you manage your card. What would you like to do?",
                "requires_auth": True,
                "requires_mfa": False,
                "data_classification": "PCI"
            },
            "fraud_report": {
                "patterns": [
                    "fraudulent transaction",
                    "didn't make this transaction",
                    "unauthorized charge",
                    "someone stole my money",
                    "hacked my account"
                ],
                "response": "I'm taking this seriously. Let me connect you with a fraud specialist immediately.",
                "requires_auth": True,
                "requires_mfa": False,
                "data_classification": "PCI",
                "escalate_immediately": True
            }
        }
    
    async def classify_intent(self, query: str, user_context: Optional[Dict] = None) -> IntentClassificationResult:
        """
        Classify customer query into intent type.
        
        Args:
            query: Customer's natural language query
            user_context: User account and session context
            
        Returns:
            IntentClassificationResult with intent, confidence, and requirements
        """
        logger.info(f"Classifying intent for query: {query[:100]}...")
        
        # Check for fraud/urgent indicators first
        urgent_keywords = ["fraud", "hacked", "stolen", "compromised", "emergency", "urgent"]
        if any(keyword in query.lower() for keyword in urgent_keywords):
            logger.warning(f"Fraud/urgent keywords detected: {query}")
            return IntentClassificationResult(
                intent=IntentType.ESCALATION_REQUIRED,
                confidence=1.0,
                requires_mfa=False,
                data_classification="PCI",
                escalation_required=True,
                reasoning="Fraud or urgent keywords detected - immediate escalation required"
            )
        
        # Try knowledge base matching first (faster, no API call needed)
        for kb_key, kb_entry in self.knowledge_base.items():
            for pattern in kb_entry.get("patterns", []):
                if pattern.lower() in query.lower():
                    intent_type = IntentType(kb_key) if kb_key in [e.value for e in IntentType] else IntentType.GENERAL_INQUIRY
                    
                    if kb_entry.get("escalate_immediately"):
                        intent_type = IntentType.ESCALATION_REQUIRED
                    
                    return IntentClassificationResult(
                        intent=intent_type,
                        confidence=0.92,
                        requires_mfa=kb_entry.get("requires_mfa", False),
                        data_classification=kb_entry.get("data_classification", "CONFIDENTIAL"),
                        escalation_required=kb_entry.get("escalate_immediately", False),
                        reasoning=f"Matched pattern: '{pattern}' from knowledge base"
                    )
        
        # Fall back to OpenAI if available
        if self.openai_api_key:
            try:
                return await self._classify_with_openai(query, user_context)
            except Exception as e:
                logger.error(f"OpenAI classification failed: {str(e)}")
        
        # Default fallback
        logger.info(f"No specific intent matched, defaulting to GENERAL_INQUIRY")
        return IntentClassificationResult(
            intent=IntentType.GENERAL_INQUIRY,
            confidence=0.6,
            requires_mfa=False,
            data_classification="PUBLIC",
            escalation_required=False,
            reasoning="No specific pattern matched, treating as general inquiry"
        )
    
    async def _classify_with_openai(self, query: str, user_context: Optional[Dict] = None) -> IntentClassificationResult:
        """Classify intent using OpenAI GPT-4."""
        try:
            prompt = f"""
Classify the following customer banking query into one of these categories:
- account_balance: Customer asking about their current balance
- transaction_history: Customer asking to see past transactions
- transfer_funds: Customer wants to transfer money
- card_management: Customer wants to manage their card (block, replace, etc)
- account_settings: Customer wants to change account settings
- fraud_report: Customer reporting fraud or unauthorized transactions
- general_inquiry: Other informational queries
- escalation_required: Query requires human specialist

Query: "{query}"

Respond with JSON format:
{{
    "intent": "<intent_type>",
    "confidence": <0.0-1.0>,
    "requires_mfa": <true/false>,
    "reasoning": "<brief explanation>"
}}
"""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=200
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            
            intent_str = result.get("intent", "unknown").upper()
            # Handle conversion to enum
            try:
                intent = IntentType[intent_str]
            except KeyError:
                intent = IntentType.GENERAL_INQUIRY
            
            return IntentClassificationResult(
                intent=intent,
                confidence=min(max(float(result.get("confidence", 0.5)), 0.0), 1.0),
                requires_mfa=result.get("requires_mfa", False),
                data_classification="PCI" if intent in [IntentType.TRANSFER_FUNDS, IntentType.ACCOUNT_BALANCE] else "CONFIDENTIAL",
                escalation_required=intent == IntentType.ESCALATION_REQUIRED,
                reasoning=result.get("reasoning", "OpenAI classification")
            )
        
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise
    
    async def generate_response(
        self, 
        query: str, 
        intent: IntentClassificationResult,
        user_context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Generate response based on intent classification.
        
        Args:
            query: Customer query
            intent: Classification result
            user_context: User account context
            
        Returns:
            Response dict with message, actions, and escalation info
        """
        logger.info(f"Generating response for intent: {intent.intent}")
        
        # If escalation required, return escalation response
        if intent.escalation_required:
            return {
                "message": "Thank you for contacting us. I'm connecting you with a specialist who can best assist you.",
                "intent": intent.intent.value,
                "confidence": intent.confidence,
                "escalation_required": True,
                "escalation_priority": "HIGH" if "fraud" in query.lower() else "MEDIUM",
                "suggested_specialist": "Fraud Investigation Team" if "fraud" in query.lower() else "General Support Specialist",
                "wait_time_estimate": "< 2 minutes",
                "requires_action": "escalate"
            }
        
        # Generate automated response based on intent
        response_templates = {
            IntentType.ACCOUNT_BALANCE: {
                "message": "I can help you check your account balance. Please verify your identity with MFA to proceed.",
                "actions": ["verify_mfa", "retrieve_balance"],
                "requires_mfa": True
            },
            IntentType.TRANSACTION_HISTORY: {
                "message": "I'll show you your recent transactions. Let me retrieve that for you.",
                "actions": ["retrieve_transactions"],
                "requires_mfa": False
            },
            IntentType.CARD_MANAGEMENT: {
                "message": "I can help you manage your card. What would you like to do? (Block, Replace, or Check Status)",
                "actions": ["show_card_options"],
                "requires_mfa": True
            },
            IntentType.GENERAL_INQUIRY: {
                "message": "Thank you for your question. I'll help you find the answer.",
                "actions": ["search_kb"],
                "requires_mfa": False
            }
        }
        
        template = response_templates.get(intent.intent, {
            "message": "How can I assist you today?",
            "actions": [],
            "requires_mfa": False
        })
        
        return {
            "message": template["message"],
            "intent": intent.intent.value,
            "confidence": intent.confidence,
            "data_classification": intent.data_classification,
            "requires_mfa": intent.requires_mfa,
            "escalation_required": False,
            "suggested_actions": template["actions"],
            "requires_action": "mfa_verify" if intent.requires_mfa else "proceed"
        }
