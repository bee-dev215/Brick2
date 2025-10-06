"""Orchestration session schemas."""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class OrchestrationSessionBase(BaseModel):
    """Base orchestration session schema."""
    
    session_type: str = Field(..., description="Type of orchestration session")
    priority: int = Field(default=1, ge=1, le=4, description="Priority level (1-4)")
    context_data: Optional[Dict[str, Any]] = Field(None, description="Session context data")
    input_data: Optional[Dict[str, Any]] = Field(None, description="Input data for the session")
    ai_model: Optional[str] = Field(None, description="AI model used for this session")
    estimated_duration: Optional[int] = Field(None, description="Estimated duration in seconds")


class OrchestrationSessionCreate(OrchestrationSessionBase):
    """Schema for creating an orchestration session."""
    
    user_id: int = Field(..., description="User ID")
    campaign_id: Optional[int] = Field(None, description="Campaign ID if applicable")


class OrchestrationSessionUpdate(BaseModel):
    """Schema for updating an orchestration session."""
    
    status: Optional[str] = Field(None, description="Session status")
    context_data: Optional[Dict[str, Any]] = Field(None, description="Updated context data")
    output_data: Optional[Dict[str, Any]] = Field(None, description="Session output data")
    confidence_score: Optional[int] = Field(None, ge=0, le=100, description="AI confidence score")
    processing_steps: Optional[Dict[str, Any]] = Field(None, description="Processing steps taken")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    retry_count: Optional[int] = Field(None, ge=0, description="Number of retries attempted")
    completed_at: Optional[datetime] = Field(None, description="Completion timestamp")


class OrchestrationSessionResponse(OrchestrationSessionBase):
    """Schema for orchestration session response."""
    
    id: int
    user_id: int
    campaign_id: Optional[int]
    status: str
    confidence_score: Optional[int]
    processing_steps: Optional[Dict[str, Any]]
    error_message: Optional[str]
    retry_count: int
    max_retries: int
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class OrchestrationSessionList(BaseModel):
    """Schema for orchestration session list response."""
    
    sessions: list[OrchestrationSessionResponse]
    total: int
    skip: int
    limit: int
