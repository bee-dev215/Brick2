"""Ad Pydantic schemas."""

from __future__ import annotations

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel


class AdCreate(BaseModel):
    """Schema for creating an ad."""
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    ad_type: str
    target_audience: Optional[Dict[str, Any]] = None
    demographics: Optional[Dict[str, Any]] = None
    interests: Optional[Dict[str, Any]] = None
    bid_amount: Optional[float] = None
    bid_type: Optional[str] = None
    media_urls: Optional[Dict[str, Any]] = None
    landing_page_url: Optional[str] = None
    campaign_id: int


class AdUpdate(BaseModel):
    """Schema for updating an ad."""
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    status: Optional[str] = None
    ad_type: Optional[str] = None
    target_audience: Optional[Dict[str, Any]] = None
    demographics: Optional[Dict[str, Any]] = None
    interests: Optional[Dict[str, Any]] = None
    bid_amount: Optional[float] = None
    bid_type: Optional[str] = None
    media_urls: Optional[Dict[str, Any]] = None
    landing_page_url: Optional[str] = None


class AdResponse(BaseModel):
    """Schema for ad response."""
    id: int
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    status: str
    ad_type: str
    target_audience: Optional[Dict[str, Any]] = None
    demographics: Optional[Dict[str, Any]] = None
    interests: Optional[Dict[str, Any]] = None
    bid_amount: Optional[float] = None
    bid_type: Optional[str] = None
    impressions: int
    clicks: int
    conversions: int
    spend: float
    media_urls: Optional[Dict[str, Any]] = None
    landing_page_url: Optional[str] = None
    campaign_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AdWithCampaign(AdResponse):
    """Schema for ad with campaign."""
    campaign: Optional["CampaignResponse"] = None
