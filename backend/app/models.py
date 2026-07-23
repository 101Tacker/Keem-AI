"""
Data models for Keem-AI API
Pydantic models for request/response validation
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum


class RoleEnum(str, Enum):
    """User roles"""
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class MessageRole(str, Enum):
    """Chat message roles"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


# ============ User Models ============
class UserBase(BaseModel):
    """Base user model"""
    email: EmailStr
    full_name: Optional[str] = None
    role: RoleEnum = RoleEnum.USER


class UserCreate(UserBase):
    """User creation model"""
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """User update model"""
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserResponse(UserBase):
    """User response model"""
    id: int
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


# ============ Chat Models ============
class ChatMessage(BaseModel):
    """Single chat message"""
    role: MessageRole
    content: str
    timestamp: Optional[datetime] = None


class ChatRequest(BaseModel):
    """Chat request model"""
    message: str = Field(..., min_length=1, max_length=2000)
    conversation_id: Optional[str] = None
    model: str = Field(default="gpt-4")


class ChatResponse(BaseModel):
    """Chat response model"""
    id: str
    conversation_id: str
    message: str
    tokens_used: int
    timestamp: datetime


class ConversationCreate(BaseModel):
    """Create new conversation"""
    title: Optional[str] = None


class ConversationResponse(BaseModel):
    """Conversation response"""
    id: str
    user_id: int
    title: str
    messages: List[ChatMessage]
    created_at: datetime
    updated_at: datetime
    message_count: int

    class Config:
        from_attributes = True


class ConversationHistory(BaseModel):
    """Conversation history with pagination"""
    total: int
    page: int
    page_size: int
    conversations: List[ConversationResponse]


# ============ Auth Models ============
class TokenData(BaseModel):
    """JWT token data"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class LoginRequest(BaseModel):
    """Login request"""
    email: EmailStr
    password: str


# ============ Analytics Models ============
class UsageMetrics(BaseModel):
    """Usage metrics for analytics"""
    total_conversations: int
    total_messages: int
    total_tokens_used: int
    avg_response_time: float
    date: datetime


class UserAnalytics(BaseModel):
    """User analytics"""
    user_id: int
    total_conversations: int
    total_messages: int
    most_active_hour: int
    favorite_topics: List[str]


# ============ Error Models ============
class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: str
    status_code: int
    timestamp: datetime
