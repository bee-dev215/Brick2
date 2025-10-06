"""Performance Pydantic schemas."""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel


class PerformanceCreate(BaseModel):
    """Schema for creating performance data."""
    campaign_id: int
    date: datetime
    metric_type: str
    value: float
    cost: float = 0.0
    metadata: Optional[Dict[str, Any]] = None


class PerformanceUpdate(BaseModel):
    """Schema for updating performance data."""
    metric_type: Optional[str] = None
    value: Optional[float] = None
    cost: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None


class PerformanceResponse(BaseModel):
    """Schema for performance response."""
    id: int
    campaign_id: int
    date: datetime
    metric_type: str
    value: float
    cost: float
    meta_data: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PerformanceWithCampaign(PerformanceResponse):
    """Schema for performance with campaign."""
    campaign: Optional["CampaignResponse"] = None


class PerformanceSummary(BaseModel):
    """Schema for performance summary."""
    campaign_id: int
    date: datetime
    impressions: int = 0
    clicks: int = 0
    conversions: int = 0
    spend: float = 0.0
    ctr: float = 0.0  # Click-through rate
    cpc: float = 0.0  # Cost per click
    cpa: float = 0.0  # Cost per acquisition


class PerformanceStats(BaseModel):
    """Schema for aggregated performance statistics."""
    total_impressions: int = 0
    total_clicks: int = 0
    total_conversions: int = 0
    total_spend: float = 0.0
    average_ctr: float = 0.0
    average_cpc: float = 0.0
    average_cpa: float = 0.0
    period_start: datetime
    period_end: datetime
