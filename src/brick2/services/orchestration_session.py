"""Orchestration session service."""

from typing import List, Optional
from datetime import datetime
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models.orchestration_session import OrchestrationSession
from ..schemas.orchestration_session import OrchestrationSessionCreate, OrchestrationSessionUpdate


class OrchestrationSessionService:
    """Service for managing orchestration sessions."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_all(
        self, 
        skip: int = 0, 
        limit: int = 100,
        status: str = None,
        session_type: str = None,
        user_id: int = None
    ) -> List[OrchestrationSession]:
        """Get all orchestration sessions with optional filtering."""
        query = select(OrchestrationSession).options(
            selectinload(OrchestrationSession.user),
            selectinload(OrchestrationSession.campaign)
        )
        
        conditions = []
        if status:
            conditions.append(OrchestrationSession.status == status)
        if session_type:
            conditions.append(OrchestrationSession.session_type == session_type)
        if user_id:
            conditions.append(OrchestrationSession.user_id == user_id)
        
        if conditions:
            query = query.where(and_(*conditions))
        
        query = query.offset(skip).limit(limit).order_by(OrchestrationSession.created_at.desc())
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_by_id(self, session_id: int) -> Optional[OrchestrationSession]:
        """Get orchestration session by ID."""
        query = select(OrchestrationSession).options(
            selectinload(OrchestrationSession.user),
            selectinload(OrchestrationSession.campaign)
        ).where(OrchestrationSession.id == session_id)
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_user(
        self, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 100,
        status: str = None,
        session_type: str = None
    ) -> List[OrchestrationSession]:
        """Get orchestration sessions by user ID."""
        query = select(OrchestrationSession).options(
            selectinload(OrchestrationSession.user),
            selectinload(OrchestrationSession.campaign)
        ).where(OrchestrationSession.user_id == user_id)
        
        conditions = [OrchestrationSession.user_id == user_id]
        if status:
            conditions.append(OrchestrationSession.status == status)
        if session_type:
            conditions.append(OrchestrationSession.session_type == session_type)
        
        query = query.where(and_(*conditions))
        query = query.offset(skip).limit(limit).order_by(OrchestrationSession.created_at.desc())
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_by_campaign(
        self, 
        campaign_id: int, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[OrchestrationSession]:
        """Get orchestration sessions by campaign ID."""
        query = select(OrchestrationSession).options(
            selectinload(OrchestrationSession.user),
            selectinload(OrchestrationSession.campaign)
        ).where(OrchestrationSession.campaign_id == campaign_id)
        
        query = query.offset(skip).limit(limit).order_by(OrchestrationSession.created_at.desc())
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def create(self, session_data: OrchestrationSessionCreate) -> OrchestrationSession:
        """Create a new orchestration session."""
        db_session = OrchestrationSession(
            user_id=session_data.user_id,
            campaign_id=session_data.campaign_id,
            session_type=session_data.session_type,
            priority=session_data.priority,
            context_data=session_data.context_data,
            input_data=session_data.input_data,
            ai_model=session_data.ai_model,
            estimated_duration=session_data.estimated_duration,
            status="pending"
        )
        
        self.db.add(db_session)
        await self.db.commit()
        await self.db.refresh(db_session)
        
        return db_session
    
    async def update(self, session_id: int, session_data: OrchestrationSessionUpdate) -> Optional[OrchestrationSession]:
        """Update orchestration session."""
        db_session = await self.get_by_id(session_id)
        if not db_session:
            return None
        
        update_data = session_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_session, field, value)
        
        db_session.updated_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(db_session)
        
        return db_session
    
    async def delete(self, session_id: int) -> bool:
        """Delete orchestration session."""
        db_session = await self.get_by_id(session_id)
        if not db_session:
            return False
        
        await self.db.delete(db_session)
        await self.db.commit()
        
        return True
    
    async def start_session(self, session_id: int) -> Optional[OrchestrationSession]:
        """Start an orchestration session."""
        db_session = await self.get_by_id(session_id)
        if not db_session:
            return None
        
        db_session.status = "active"
        db_session.started_at = datetime.utcnow()
        db_session.updated_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(db_session)
        
        return db_session
    
    async def complete_session(self, session_id: int, output_data: dict = None) -> Optional[OrchestrationSession]:
        """Complete an orchestration session."""
        db_session = await self.get_by_id(session_id)
        if not db_session:
            return None
        
        db_session.status = "completed"
        db_session.completed_at = datetime.utcnow()
        db_session.output_data = output_data
        db_session.updated_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(db_session)
        
        return db_session
    
    async def fail_session(self, session_id: int, error_message: str) -> Optional[OrchestrationSession]:
        """Mark an orchestration session as failed."""
        db_session = await self.get_by_id(session_id)
        if not db_session:
            return None
        
        db_session.status = "failed"
        db_session.error_message = error_message
        db_session.completed_at = datetime.utcnow()
        db_session.updated_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(db_session)
        
        return db_session
    
    async def retry_session(self, session_id: int) -> Optional[OrchestrationSession]:
        """Retry a failed orchestration session."""
        db_session = await self.get_by_id(session_id)
        if not db_session:
            return None
        
        if db_session.retry_count >= db_session.max_retries:
            return None  # Max retries exceeded
        
        db_session.status = "pending"
        db_session.retry_count += 1
        db_session.error_message = None
        db_session.started_at = None
        db_session.completed_at = None
        db_session.updated_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(db_session)
        
        return db_session
