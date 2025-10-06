"""Ad API endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ....api.deps import get_db
from ....models.ad import Ad
from ....schemas.ad import AdCreate, AdUpdate, AdResponse
from ....services.ad import AdService

router = APIRouter()


@router.get("/", response_model=List[AdResponse])
async def get_ads(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    """Get all ads."""
    ad = AdService(db)
    ads = await ad.get_all(skip=skip, limit=limit)
    return ads


@router.get("/campaign/{campaign_id}", response_model=List[AdResponse])
async def get_campaign_ads(
    campaign_id: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    """Get ads by campaign ID."""
    ad = AdService(db)
    ads = await ad.get_by_campaign(campaign_id, skip=skip, limit=limit)
    return ads


@router.get("/{ad_id}", response_model=AdResponse)
async def get_ad(
    ad_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get ad by ID."""
    ad = AdService(db)
    ad = await ad.get_by_id(ad_id)
    if not ad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ad not found"
        )
    return ad


@router.post("/", response_model=AdResponse, status_code=status.HTTP_201_CREATED)
async def create_ad(
    ad_data: AdCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new ad."""
    ad = AdService(db)
    ad = await ad.create(ad_data)
    return ad


@router.put("/{ad_id}", response_model=AdResponse)
async def update_ad(
    ad_id: int,
    ad_data: AdUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update ad."""
    ad = AdService(db)
    ad = await ad.update(ad_id, ad_data)
    if not ad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ad not found"
        )
    return ad


@router.delete("/{ad_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ad(
    ad_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Delete ad."""
    ad = AdService(db)
    success = await ad.delete(ad_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ad not found"
        )
