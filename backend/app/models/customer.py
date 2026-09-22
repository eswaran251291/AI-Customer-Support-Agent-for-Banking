"""Pydantic models for API request/response validation."""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, EmailStr


class CustomerBase(BaseModel):
    """Base customer model."""
    
    name: str
    email: EmailStr
    phone: str
    account_status: str


class CustomerCreate(CustomerBase):
    """Create customer request model."""
    
    pass


class CustomerResponse(CustomerBase):
    """Customer response model."""
    
    id: int
    customer_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class MessageBase(BaseModel):
    """Base message model."""
    
    content: str
    sender: str  # "user" or "assistant"


class ConversationBase(BaseModel):
    """Base conversation model."""
    
    customer_id: str
    messages: list[MessageBase]


class ConversationCreate(ConversationBase):
    """Create conversation request model."""
    
    pass


class ConversationResponse(ConversationBase):
    """Conversation response model."""
    
    id: int
    session_id: str
    sentiment: Optional[str] = None
    resolved: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AnalyticsResponse(BaseModel):
    """Analytics response model."""
    
    metric_name: str
    metric_value: Any
    timestamp: datetime
    
    class Config:
        from_attributes = True
