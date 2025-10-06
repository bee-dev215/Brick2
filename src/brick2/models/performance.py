"""Performance metrics model."""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship

from .base import BaseModel


class Performance(BaseModel):
    """Performance metrics model."""
    
    __tablename__ = "performances"
    
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False, index=True)
    date = Column(DateTime(timezone=True), nullable=False, index=True)
    metric_type = Column(String(50), nullable=False, index=True)  # impressions, clicks, conversions, etc.
    value = Column(Float, nullable=False)
    cost = Column(Float, default=0.0)
    meta_data = Column(Text, nullable=True)  # JSON string for additional metrics
    
    # Relationships
    campaign = relationship("Campaign", back_populates="performances")
