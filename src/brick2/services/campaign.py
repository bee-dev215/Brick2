"""Campaign service for database operations."""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from sqlalchemy.orm import selectinload

from ..models.campaign import Campaign
from ..schemas.campaign import CampaignCreate, CampaignUpdate


class CampaignService:
    """Campaign service for database operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Campaign]:
        """Get all campaigns with pagination."""
        result = await self.db.execute(
            select(Campaign)
            .offset(skip)
            .limit(limit)
            .order_by(Campaign.created_at.desc())
        )
        return result.scalars().all()
    
    async def get_by_id(self, campaign_id: int) -> Optional[Campaign]:
        """Get campaign by ID."""
        result = await self.db.execute(
            select(Campaign).where(Campaign.id == campaign_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_owner(self, owner_id: int, skip: int = 0, limit: int = 100) -> List[Campaign]:
        """Get campaigns by owner ID."""
        result = await self.db.execute(
            select(Campaign)
            .where(Campaign.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .order_by(Campaign.created_at.desc())
        )
        return result.scalars().all()
    
    async def get_by_external_id(self, external_id: str) -> Optional[Campaign]:
        """Get campaign by external ID."""
        result = await self.db.execute(
            select(Campaign).where(Campaign.external_id == external_id)
        )
        return result.scalar_one_or_none()
    
    async def create(self, campaign_data: CampaignCreate) -> Campaign:
        """Create a new campaign."""
        db_campaign = Campaign(
            platform=campaign_data.platform,
            name=campaign_data.name,
            external_id=campaign_data.external_id,
            description=campaign_data.description,
            budget=campaign_data.budget,
            daily_budget=campaign_data.daily_budget,
            start_date=campaign_data.start_date,
            end_date=campaign_data.end_date,
            is_active=campaign_data.is_active,
            owner_id=owner_id,
        )
        self.db.add(db_campaign)
        await self.db.commit()
        await self.db.refresh(db_campaign)
        return db_campaign
    
    async def update(self, campaign_id: int, campaign_data: CampaignUpdate) -> Optional[Campaign]:
        """Update campaign."""
        db_campaign = await self.get_by_id(campaign_id)
        if not db_campaign:
            return None
        
        update_data = campaign_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(db_campaign, field) and value is not None:
                setattr(db_campaign, field, value)
        
        await self.db.commit()
        await self.db.refresh(db_campaign)
        return db_campaign
    
    async def delete(self, campaign_id: int) -> bool:
        """Delete campaign."""
        db_campaign = await self.get_by_id(campaign_id)
        if not db_campaign:
            return False
        
        await self.db.delete(db_campaign)
        await self.db.commit()
        return True
    
    async def count(self) -> int:
        """Get total count of campaigns."""
        from sqlalchemy import func
        result = await self.db.execute(select(func.count(Campaign.id)))
        return result.scalar()
