"""Lead model."""

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from .base import BaseModel


class Lead(BaseModel):
    """Lead model."""
    
    __tablename__ = "leads"
    
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False, index=True)
    external_id = Column(String(255), nullable=True, index=True)
    email = Column(String(255), nullable=True, index=True)
    phone = Column(String(50), nullable=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    company = Column(String(255), nullable=True)
    title = Column(String(255), nullable=True)
    source = Column(String(100), nullable=True)
    status = Column(String(50), default="new", index=True)
    score = Column(Integer, nullable=True)  # Lead scoring 1-100
    notes = Column(Text, nullable=True)
    
    # Relationships
    campaign = relationship("Campaign", back_populates="leads")
