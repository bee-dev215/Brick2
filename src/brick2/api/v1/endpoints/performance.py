"""Performance API endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ....api.deps import get_db
from ....models.performance import Performance
from ....schemas.performance import PerformanceCreate, PerformanceUpdate, PerformanceResponse
from ....services.performance import PerformanceService

router = APIRouter()


@router.get("/", response_model=List[PerformanceResponse])
async def get_performances(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    """Get all performances."""
    performance = PerformanceService(db)
    performances = await performance.get_all(skip=skip, limit=limit)
    return performances


@router.get("/campaign/{campaign_id}", response_model=List[PerformanceResponse])
async def get_campaign_performances(
    campaign_id: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    """Get performances by campaign ID."""
    performance = PerformanceService(db)
    performances = await performance.get_by_campaign(campaign_id, skip=skip, limit=limit)
    return performances


@router.get("/{performance_id}", response_model=PerformanceResponse)
async def get_performance(
    performance_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get performance by ID."""
    performance = PerformanceService(db)
    performance = await performance.get_by_id(performance_id)
    if not performance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Performance not found"
        )
    return performance


@router.post("/", response_model=PerformanceResponse, status_code=status.HTTP_201_CREATED)
async def create_performance(
    performance_data: PerformanceCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new performance record."""
    performance = PerformanceService(db)
    performance = await performance.create(performance_data)
    return performance


@router.put("/{performance_id}", response_model=PerformanceResponse)
async def update_performance(
    performance_id: int,
    performance_data: PerformanceUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update performance."""
    performance = PerformanceService(db)
    performance = await performance.update(performance_id, performance_data)
    if not performance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Performance not found"
        )
    return performance


@router.delete("/{performance_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_performance(
    performance_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Delete performance."""
    performance = PerformanceService(db)
    success = await performance.delete(performance_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Performance not found"
        )
