"""Performance service for database operations."""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..models.performance import Performance
from ..schemas.performance import PerformanceCreate, PerformanceUpdate


class PerformanceService:
    """Performance service for database operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Performance]:
        """Get all performance records with pagination."""
        result = await self.db.execute(
            select(Performance)
            .offset(skip)
            .limit(limit)
            .order_by(Performance.created_at.desc())
        )
        return result.scalars().all()
    
    async def get_by_id(self, performance_id: int) -> Optional[Performance]:
        """Get performance record by ID."""
        result = await self.db.execute(
            select(Performance).where(Performance.id == performance_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_campaign(self, campaign_id: int, skip: int = 0, limit: int = 100) -> List[Performance]:
        """Get performance records by campaign ID."""
        result = await self.db.execute(
            select(Performance)
            .where(Performance.campaign_id == campaign_id)
            .offset(skip)
            .limit(limit)
            .order_by(Performance.date.desc())
        )
        return result.scalars().all()
    
    async def create(self, performance_data: PerformanceCreate) -> Performance:
        """Create a new performance record."""
        db_performance = Performance(
            campaign_id=performance_data.campaign_id,
            date=performance_data.date,
            metric_type=performance_data.metric_type,
            value=performance_data.value,
            cost=performance_data.cost,
            meta_data=str(performance_data.metadata) if performance_data.metadata else None,
        )
        self.db.add(db_performance)
        await self.db.commit()
        await self.db.refresh(db_performance)
        return db_performance
    
    async def update(self, performance_id: int, performance_data: PerformanceUpdate) -> Optional[Performance]:
        """Update performance record."""
        db_performance = await self.get_by_id(performance_id)
        if not db_performance:
            return None
        
        update_data = performance_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(db_performance, field) and value is not None:
                if field == "metadata":
                    setattr(db_performance, "meta_data", str(value))
                else:
                    setattr(db_performance, field, value)
        
        await self.db.commit()
        await self.db.refresh(db_performance)
        return db_performance
    
    async def delete(self, performance_id: int) -> bool:
        """Delete performance record."""
        db_performance = await self.get_by_id(performance_id)
        if not db_performance:
            return False
        
        await self.db.delete(db_performance)
        await self.db.commit()
        return True
    
    async def count(self) -> int:
        """Get total count of performance records."""
        result = await self.db.execute(select(Performance).count())
        return result.scalar()
