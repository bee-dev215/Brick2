"""Lead Pydantic schemas."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class LeadCreate(BaseModel):
    """Schema for creating a lead."""
    campaign_id: int
    external_id: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company: Optional[str] = None
    title: Optional[str] = None
    source: Optional[str] = None
    score: Optional[int] = None
    notes: Optional[str] = None


class LeadUpdate(BaseModel):
    """Schema for updating a lead."""
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company: Optional[str] = None
    title: Optional[str] = None
    source: Optional[str] = None
    status: Optional[str] = None
    score: Optional[int] = None
    notes: Optional[str] = None


class LeadResponse(BaseModel):
    """Schema for lead response."""
    id: int
    campaign_id: int
    external_id: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company: Optional[str] = None
    title: Optional[str] = None
    source: Optional[str] = None
    status: str
    score: Optional[int] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LeadWithCampaign(LeadResponse):
    """Schema for lead with campaign."""
    campaign: Optional["CampaignResponse"] = None
