"""Campaign API endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ....api.deps import get_db, get_current_active_user
from ....models.campaign import Campaign
from ....schemas.campaign import CampaignCreate, CampaignUpdate, CampaignResponse
from ....services.campaign import CampaignService

router = APIRouter()


@router.get("/", response_model=List[CampaignResponse])
async def get_campaigns(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    """Get all campaigns."""
    campaign = CampaignService(db)
    campaigns = await campaign.get_all(skip=skip, limit=limit)
    return campaigns


@router.get("/user/{user_id}", response_model=List[CampaignResponse])
async def get_user_campaigns(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    """Get campaigns by user ID."""
    campaign = CampaignService(db)
    campaigns = await campaign.get_by_owner(user_id, skip=skip, limit=limit)
    return campaigns


@router.get("/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(
    campaign_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get campaign by ID."""
    campaign = CampaignService(db)
    campaign = await campaign.get_by_id(campaign_id)
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    return campaign


@router.post("/", response_model=CampaignResponse, status_code=status.HTTP_201_CREATED)
async def create_campaign(
    campaign_data: CampaignCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new campaign."""
    campaign = CampaignService(db)
    campaign = await campaign.create(campaign_data, campaign_data.owner_id)
    return campaign


@router.put("/{campaign_id}", response_model=CampaignResponse)
async def update_campaign(
    campaign_id: int,
    campaign_data: CampaignUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update campaign."""
    campaign = CampaignService(db)
    campaign = await campaign.update(campaign_id, campaign_data)
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    return campaign


@router.delete("/{campaign_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_campaign(
    campaign_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Delete campaign."""
    campaign = CampaignService(db)
    success = await campaign.delete(campaign_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
