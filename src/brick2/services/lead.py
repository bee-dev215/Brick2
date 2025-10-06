"""Lead service for database operations."""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..models.lead import Lead
from ..schemas.lead import LeadCreate, LeadUpdate


class LeadService:
    """Lead service for database operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Lead]:
        """Get all leads with pagination."""
        result = await self.db.execute(
            select(Lead)
            .offset(skip)
            .limit(limit)
            .order_by(Lead.created_at.desc())
        )
        return result.scalars().all()
    
    async def get_by_id(self, lead_id: int) -> Optional[Lead]:
        """Get lead by ID."""
        result = await self.db.execute(
            select(Lead).where(Lead.id == lead_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_campaign(self, campaign_id: int, skip: int = 0, limit: int = 100) -> List[Lead]:
        """Get leads by campaign ID."""
        result = await self.db.execute(
            select(Lead)
            .where(Lead.campaign_id == campaign_id)
            .offset(skip)
            .limit(limit)
            .order_by(Lead.created_at.desc())
        )
        return result.scalars().all()
    
    async def get_by_email(self, email: str) -> Optional[Lead]:
        """Get lead by email."""
        result = await self.db.execute(
            select(Lead).where(Lead.email == email)
        )
        return result.scalar_one_or_none()
    
    async def create(self, lead_data: LeadCreate) -> Lead:
        """Create a new lead."""
        db_lead = Lead(
            campaign_id=lead_data.campaign_id,
            external_id=lead_data.external_id,
            email=lead_data.email,
            phone=lead_data.phone,
            first_name=lead_data.first_name,
            last_name=lead_data.last_name,
            company=lead_data.company,
            title=lead_data.title,
            source=lead_data.source,
            score=lead_data.score,
            notes=lead_data.notes,
        )
        self.db.add(db_lead)
        await self.db.commit()
        await self.db.refresh(db_lead)
        return db_lead
    
    async def update(self, lead_id: int, lead_data: LeadUpdate) -> Optional[Lead]:
        """Update lead."""
        db_lead = await self.get_by_id(lead_id)
        if not db_lead:
            return None
        
        update_data = lead_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(db_lead, field) and value is not None:
                setattr(db_lead, field, value)
        
        await self.db.commit()
        await self.db.refresh(db_lead)
        return db_lead
    
    async def delete(self, lead_id: int) -> bool:
        """Delete lead."""
        db_lead = await self.get_by_id(lead_id)
        if not db_lead:
            return False
        
        await self.db.delete(db_lead)
        await self.db.commit()
        return True
    
    async def count(self) -> int:
        """Get total count of leads."""
        result = await self.db.execute(select(Lead).count())
        return result.scalar()
