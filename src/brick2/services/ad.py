"""Ad service for database operations."""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..models.ad import Ad
from ..schemas.ad import AdCreate, AdUpdate


class AdService:
    """Ad service for database operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Ad]:
        """Get all ads with pagination."""
        result = await self.db.execute(
            select(Ad)
            .offset(skip)
            .limit(limit)
            .order_by(Ad.created_at.desc())
        )
        return result.scalars().all()
    
    async def get_by_id(self, ad_id: int) -> Optional[Ad]:
        """Get ad by ID."""
        result = await self.db.execute(
            select(Ad).where(Ad.id == ad_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_campaign(self, campaign_id: int, skip: int = 0, limit: int = 100) -> List[Ad]:
        """Get ads by campaign ID."""
        result = await self.db.execute(
            select(Ad)
            .where(Ad.campaign_id == campaign_id)
            .offset(skip)
            .limit(limit)
            .order_by(Ad.created_at.desc())
        )
        return result.scalars().all()
    
    async def create(self, ad_data: AdCreate) -> Ad:
        """Create a new ad."""
        db_ad = Ad(
            title=ad_data.title,
            description=ad_data.description,
            content=ad_data.content,
            ad_type=ad_data.ad_type,
            target_audience=ad_data.target_audience,
            demographics=ad_data.demographics,
            interests=ad_data.interests,
            bid_amount=ad_data.bid_amount,
            bid_type=ad_data.bid_type,
            media_urls=ad_data.media_urls,
            landing_page_url=ad_data.landing_page_url,
            campaign_id=ad_data.campaign_id,
        )
        self.db.add(db_ad)
        await self.db.commit()
        await self.db.refresh(db_ad)
        return db_ad
    
    async def update(self, ad_id: int, ad_data: AdUpdate) -> Optional[Ad]:
        """Update ad."""
        db_ad = await self.get_by_id(ad_id)
        if not db_ad:
            return None
        
        update_data = ad_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(db_ad, field) and value is not None:
                setattr(db_ad, field, value)
        
        await self.db.commit()
        await self.db.refresh(db_ad)
        return db_ad
    
    async def delete(self, ad_id: int) -> bool:
        """Delete ad."""
        db_ad = await self.get_by_id(ad_id)
        if not db_ad:
            return False
        
        await self.db.delete(db_ad)
        await self.db.commit()
        return True
    
    async def count(self) -> int:
        """Get total count of ads."""
        result = await self.db.execute(select(Ad).count())
        return result.scalar()
