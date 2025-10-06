"""Orchestration session model for BRICK 1 integration."""

from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship

from .base import BaseModel


class OrchestrationSession(BaseModel):
    """Orchestration session model for managing AI-driven campaign orchestration."""
    
    __tablename__ = "orchestration_sessions"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=True, index=True)
    
    # Session metadata
    session_type = Column(String(50), nullable=False, index=True)  # 'campaign_creation', 'optimization', 'analysis', 'lead_processing'
    status = Column(String(50), default="active", index=True)  # 'active', 'completed', 'failed', 'paused'
    priority = Column(Integer, default=1)  # 1=low, 2=medium, 3=high, 4=critical
    
    # Session context and state
    context_data = Column(JSON, nullable=True)  # Session context, parameters, current state
    input_data = Column(JSON, nullable=True)  # Initial input data for the session
    output_data = Column(JSON, nullable=True)  # Results/output from the session
    
    # AI/Orchestration specific fields
    ai_model = Column(String(100), nullable=True)  # AI model used for this session
    confidence_score = Column(Integer, nullable=True)  # AI confidence score (0-100)
    processing_steps = Column(JSON, nullable=True)  # Steps taken during processing
    
    # Error handling
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    
    # Timing
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    estimated_duration = Column(Integer, nullable=True)  # Estimated duration in seconds
    
    # Relationships
    user = relationship("User", backref="orchestration_sessions")
    campaign = relationship("Campaign", backref="orchestration_sessions")
