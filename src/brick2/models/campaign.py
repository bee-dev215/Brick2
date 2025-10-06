"""Campaign model."""

from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from .base import BaseModel


class Campaign(BaseModel):
    """Campaign model."""
    
    __tablename__ = "campaigns"
    
    platform = Column(String(100), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    external_id = Column(String(255), nullable=True, index=True)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="draft")  # draft, active, paused, completed
    budget = Column(Integer, nullable=True)  # Budget in cents
    daily_budget = Column(Integer, nullable=True)  # Daily budget in cents
    start_date = Column(DateTime(timezone=True), nullable=True)
    end_date = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Foreign keys
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="campaigns")
    ads = relationship("Ad", back_populates="campaign", cascade="all, delete-orphan")
    leads = relationship("Lead", back_populates="campaign", cascade="all, delete-orphan")
    performances = relationship("Performance", back_populates="campaign", cascade="all, delete-orphan")
