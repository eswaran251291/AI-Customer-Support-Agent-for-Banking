"""Customer service for account and customer operations."""

import logging
from typing import Optional, Dict, Any
from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class CustomerService:
    """Service for customer operations."""
    
    def __init__(self, db: Session):
        """Initialize customer service with database session."""
        self.db = db
    
    async def get_customer_by_id(self, customer_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve customer information (masked for privacy).
        
        Args:
            customer_id: Customer identifier
            
        Returns:
            Customer info dict or None
        """
        logger.info(f"Fetching customer: {customer_id}")
        
        # Mock customer data (in production, query from database)
        mock_customers = {
            "CUST_001": {
                "id": "CUST_001",
                "name": "John Doe",
                "email": "john.doe@example.com",
                "account_status": "ACTIVE",
                "account_type": "Checking",
                "balance": Decimal("2547.89"),
                "last_4_digits": "5678",
                "created_at": datetime(2015, 3, 20)
            },
            "CUST_002": {
                "id": "CUST_002",
                "name": "Jane Smith",
                "email": "jane.smith@example.com",
                "account_status": "ACTIVE",
                "account_type": "Savings",
                "balance": Decimal("15234.50"),
                "last_4_digits": "1234",
                "created_at": datetime(2018, 6, 15)
            }
        }
        
        customer = mock_customers.get(customer_id)
        
        if customer:
            # Log access for audit trail (PCI-DSS requirement)
            logger.info(
                "Customer lookup",
                extra={
                    "customer_id": customer_id,
                    "action": "VIEW",
                    "data_classification": "PCI",
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
        else:
            logger.warning(f"Customer not found: {customer_id}")
        
        return customer
    
    async def get_account_balance(self, customer_id: str) -> Optional[Dict[str, Any]]:
        """Get customer's account balance."""
        logger.info(f"Fetching balance for customer: {customer_id}")
        
        customer = await self.get_customer_by_id(customer_id)
        if not customer:
            return None
        
        return {
            "customer_id": customer_id,
            "balance": str(customer["balance"]),
            "account_number_masked": f"****{customer['last_4_digits']}",
            "status": customer["account_status"],
            "last_updated": datetime.utcnow().isoformat()
        }
    
    async def get_transaction_history(
        self, 
        customer_id: str, 
        limit: int = 10
    ) -> Optional[Dict[str, Any]]:
        """Get recent transaction history for customer."""
        logger.info(f"Fetching transaction history for customer: {customer_id}")
        
        customer = await self.get_customer_by_id(customer_id)
        if not customer:
            return None
        
        # Mock transaction data
        mock_transactions = {
            "CUST_001": [
                {
                    "id": "TXN_001",
                    "date": "2024-01-15",
                    "description": "Online Purchase - Amazon",
                    "amount": "-$45.99",
                    "balance": "$2,547.89"
                },
                {
                    "id": "TXN_002",
                    "date": "2024-01-14",
                    "description": "Direct Deposit - Employer",
                    "amount": "+$2,500.00",
                    "balance": "$2,593.88"
                },
                {
                    "id": "TXN_003",
                    "date": "2024-01-13",
                    "description": "ATM Withdrawal",
                    "amount": "-$200.00",
                    "balance": "$93.88"
                },
            ],
            "CUST_002": [
                {
                    "id": "TXN_101",
                    "date": "2024-01-15",
                    "description": "Transfer to Checking",
                    "amount": "-$1,000.00",
                    "balance": "$15,234.50"
                }
            ]
        }
        
        transactions = mock_transactions.get(customer_id, [])[:limit]
        
        return {
            "customer_id": customer_id,
            "transaction_count": len(transactions),
            "transactions": transactions,
            "period": "Last 30 days"
        }
    
    async def can_transfer_funds(
        self, 
        customer_id: str, 
        amount: Decimal
    ) -> Dict[str, Any]:
        """
        Check if customer can transfer funds.
        
        Validates against daily/monthly limits and account status.
        """
        logger.info(f"Checking transfer eligibility for {customer_id}: ${amount}")
        
        customer = await self.get_customer_by_id(customer_id)
        if not customer:
            return {"eligible": False, "reason": "Customer not found"}
        
        # Check account status
        if customer["account_status"] != "ACTIVE":
            return {"eligible": False, "reason": "Account is not active"}
        
        # Check balance
        if customer["balance"] < amount:
            return {"eligible": False, "reason": f"Insufficient funds. Available: ${customer['balance']}"}
        
        # Check daily limit
        daily_limit = Decimal("10000.00")
        if amount > daily_limit:
            return {"eligible": False, "reason": f"Amount exceeds daily limit of ${daily_limit}"}
        
        # Mock check for daily usage
        daily_usage = Decimal("1500.00")  # Mock: customer already transferred $1500 today
        if daily_usage + amount > daily_limit:
            remaining = daily_limit - daily_usage
            return {
                "eligible": False, 
                "reason": f"Daily limit would be exceeded. Remaining today: ${remaining}"
            }
        
        return {
            "eligible": True,
            "available_balance": str(customer["balance"]),
            "daily_remaining": str(daily_limit - daily_usage - amount),
            "monthly_remaining": str(Decimal("50000.00") - daily_usage)
        }
