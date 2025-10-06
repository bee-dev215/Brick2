"""Ad model."""

from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship

from .base import BaseModel


class Ad(BaseModel):
    """Ad model."""
    
    __tablename__ = "ads"
    
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    status = Column(String(50), default="draft")  # draft, active, paused, rejected
    ad_type = Column(String(50), nullable=False)  # banner, video, native, search
    
    # Targeting
    target_audience = Column(JSON, nullable=True)  # JSON field for targeting criteria
    demographics = Column(JSON, nullable=True)  # Age, gender, location, etc.
    interests = Column(JSON, nullable=True)  # Interest categories
    
    # Bidding
    bid_amount = Column(Float, nullable=True)  # Bid amount in currency unit
    bid_type = Column(String(50), nullable=True)  # cpc, cpm, cpa
    
    # Performance metrics
    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    conversions = Column(Integer, default=0)
    spend = Column(Float, default=0.0)
    
    # Media
    media_urls = Column(JSON, nullable=True)  # URLs to ad creative assets
    landing_page_url = Column(String(500), nullable=True)
    
    # Foreign keys
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    
    # Relationships
    campaign = relationship("Campaign", back_populates="ads")
