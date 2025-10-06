"""Memory schemas."""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class MemoryBase(BaseModel):
    """Base memory schema."""
    
    memory_type: str = Field(..., description="Type of memory")
    category: Optional[str] = Field(None, description="Memory category")
    title: str = Field(..., description="Memory title")
    content: str = Field(..., description="Memory content")
    summary: Optional[str] = Field(None, description="AI-generated summary")
    importance_score: int = Field(default=50, ge=1, le=100, description="Importance score (1-100)")
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Confidence score")
    source: Optional[str] = Field(None, description="Memory source")
    context_data: Optional[Dict[str, Any]] = Field(None, description="Context data")
    related_entities: Optional[Dict[str, Any]] = Field(None, description="Related entities")
    expires_at: Optional[datetime] = Field(None, description="Memory expiration time")


class MemoryCreate(MemoryBase):
    """Schema for creating a memory."""
    
    user_id: int = Field(..., description="User ID")
    campaign_id: Optional[int] = Field(None, description="Campaign ID if applicable")
    orchestration_session_id: Optional[int] = Field(None, description="Orchestration session ID if applicable")


class MemoryUpdate(BaseModel):
    """Schema for updating a memory."""
    
    title: Optional[str] = Field(None, description="Updated title")
    content: Optional[str] = Field(None, description="Updated content")
    summary: Optional[str] = Field(None, description="Updated summary")
    importance_score: Optional[int] = Field(None, ge=1, le=100, description="Updated importance score")
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Updated confidence score")
    context_data: Optional[Dict[str, Any]] = Field(None, description="Updated context data")
    related_entities: Optional[Dict[str, Any]] = Field(None, description="Updated related entities")
    is_active: Optional[bool] = Field(None, description="Memory active status")
    expires_at: Optional[datetime] = Field(None, description="Updated expiration time")


class MemoryResponse(MemoryBase):
    """Schema for memory response."""
    
    id: int
    user_id: int
    campaign_id: Optional[int]
    orchestration_session_id: Optional[int]
    is_active: bool
    access_count: int
    last_accessed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class MemoryList(BaseModel):
    """Schema for memory list response."""
    
    memories: list[MemoryResponse]
    total: int
    skip: int
    limit: int
