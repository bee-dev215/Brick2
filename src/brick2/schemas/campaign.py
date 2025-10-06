"""Campaign Pydantic schemas."""

from __future__ import annotations

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class CampaignCreate(BaseModel):
    """Schema for creating a campaign."""
    platform: str
    name: str
    external_id: Optional[str] = None
    description: Optional[str] = None
    budget: float = 0.0
    daily_budget: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: bool = True
    owner_id: int = 1  # Default to user 1 for testing


class CampaignUpdate(BaseModel):
    """Schema for updating a campaign."""
    platform: Optional[str] = None
    name: Optional[str] = None
    external_id: Optional[str] = None
    description: Optional[str] = None
    budget: Optional[float] = None
    daily_budget: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: Optional[bool] = None


class CampaignResponse(BaseModel):
    """Schema for campaign response."""
    id: int
    platform: str
    name: str
    external_id: Optional[str] = None
    description: Optional[str] = None
    status: str
    budget: float
    daily_budget: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: bool
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CampaignWithAds(CampaignResponse):
    """Schema for campaign with ads."""
    ads: List["AdResponse"] = []
