"""Memory model for BRICK 1 integration."""

from sqlalchemy import Column, String, Text, Integer, ForeignKey, JSON, Float, DateTime, Boolean
from sqlalchemy.orm import relationship

from .base import BaseModel


class Memory(BaseModel):
    """Memory model for storing AI-driven insights and learnings."""
    
    __tablename__ = "memories"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=True, index=True)
    orchestration_session_id = Column(Integer, ForeignKey("orchestration_sessions.id"), nullable=True, index=True)
    
    # Memory classification
    memory_type = Column(String(50), nullable=False, index=True)  # 'campaign_insight', 'performance_pattern', 'user_preference', 'audience_behavior', 'creative_insight'
    category = Column(String(50), nullable=True, index=True)  # 'positive', 'negative', 'neutral', 'warning', 'opportunity'
    
    # Memory content
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)  # AI-generated summary
    
    # Memory metadata
    importance_score = Column(Integer, default=50)  # 1-100 importance rating
    confidence_score = Column(Float, nullable=True)  # 0.0-1.0 confidence in this memory
    source = Column(String(100), nullable=True)  # How this memory was generated
    
    # Context and relationships
    context_data = Column(JSON, nullable=True)  # Additional context information
    related_entities = Column(JSON, nullable=True)  # Related campaigns, ads, leads, etc.
    
    # Memory lifecycle
    is_active = Column(Boolean, default=True, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)  # When this memory becomes stale
    
    # Usage tracking
    access_count = Column(Integer, default=0)  # How often this memory has been accessed
    last_accessed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", backref="memories")
    campaign = relationship("Campaign", backref="memories")
    orchestration_session = relationship("OrchestrationSession", backref="memories")
