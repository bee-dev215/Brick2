"""Memory service."""

from typing import List, Optional
from datetime import datetime
from sqlalchemy import select, and_, or_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models.memory import Memory
from ..schemas.memory import MemoryCreate, MemoryUpdate


class MemoryService:
    """Service for managing memories."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_all(
        self, 
        skip: int = 0, 
        limit: int = 100,
        memory_type: str = None,
        category: str = None,
        user_id: int = None,
        campaign_id: int = None,
        is_active: bool = None
    ) -> List[Memory]:
        """Get all memories with optional filtering."""
        query = select(Memory).options(
            selectinload(Memory.user),
            selectinload(Memory.campaign),
            selectinload(Memory.orchestration_session)
        )
        
        conditions = []
        if memory_type:
            conditions.append(Memory.memory_type == memory_type)
        if category:
            conditions.append(Memory.category == category)
        if user_id:
            conditions.append(Memory.user_id == user_id)
        if campaign_id:
            conditions.append(Memory.campaign_id == campaign_id)
        if is_active is not None:
            conditions.append(Memory.is_active == is_active)
        
        if conditions:
            query = query.where(and_(*conditions))
        
        query = query.offset(skip).limit(limit).order_by(Memory.importance_score.desc(), Memory.created_at.desc())
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_by_id(self, memory_id: int) -> Optional[Memory]:
        """Get memory by ID."""
        query = select(Memory).options(
            selectinload(Memory.user),
            selectinload(Memory.campaign),
            selectinload(Memory.orchestration_session)
        ).where(Memory.id == memory_id)
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_user(
        self, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 100,
        memory_type: str = None,
        category: str = None
    ) -> List[Memory]:
        """Get memories by user ID."""
        query = select(Memory).options(
            selectinload(Memory.user),
            selectinload(Memory.campaign),
            selectinload(Memory.orchestration_session)
        ).where(Memory.user_id == user_id)
        
        conditions = [Memory.user_id == user_id, Memory.is_active == True]
        if memory_type:
            conditions.append(Memory.memory_type == memory_type)
        if category:
            conditions.append(Memory.category == category)
        
        query = query.where(and_(*conditions))
        query = query.offset(skip).limit(limit).order_by(Memory.importance_score.desc(), Memory.created_at.desc())
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_by_campaign(
        self, 
        campaign_id: int, 
        skip: int = 0, 
        limit: int = 100,
        memory_type: str = None
    ) -> List[Memory]:
        """Get memories by campaign ID."""
        query = select(Memory).options(
            selectinload(Memory.user),
            selectinload(Memory.campaign),
            selectinload(Memory.orchestration_session)
        ).where(Memory.campaign_id == campaign_id)
        
        conditions = [Memory.campaign_id == campaign_id, Memory.is_active == True]
        if memory_type:
            conditions.append(Memory.memory_type == memory_type)
        
        query = query.where(and_(*conditions))
        query = query.offset(skip).limit(limit).order_by(Memory.importance_score.desc(), Memory.created_at.desc())
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def search(
        self,
        query: str,
        skip: int = 0,
        limit: int = 100,
        memory_type: str = None,
        user_id: int = None
    ) -> List[Memory]:
        """Search memories by content or title."""
        search_query = select(Memory).options(
            selectinload(Memory.user),
            selectinload(Memory.campaign),
            selectinload(Memory.orchestration_session)
        )
        
        # Search in title and content
        search_conditions = or_(
            Memory.title.ilike(f"%{query}%"),
            Memory.content.ilike(f"%{query}%"),
            Memory.summary.ilike(f"%{query}%")
        )
        
        conditions = [search_conditions, Memory.is_active == True]
        if memory_type:
            conditions.append(Memory.memory_type == memory_type)
        if user_id:
            conditions.append(Memory.user_id == user_id)
        
        search_query = search_query.where(and_(*conditions))
        search_query = search_query.offset(skip).limit(limit).order_by(Memory.importance_score.desc(), Memory.created_at.desc())
        
        result = await self.db.execute(search_query)
        return result.scalars().all()
    
    async def create(self, memory_data: MemoryCreate) -> Memory:
        """Create a new memory."""
        db_memory = Memory(
            user_id=memory_data.user_id,
            campaign_id=memory_data.campaign_id,
            orchestration_session_id=memory_data.orchestration_session_id,
            memory_type=memory_data.memory_type,
            category=memory_data.category,
            title=memory_data.title,
            content=memory_data.content,
            summary=memory_data.summary,
            importance_score=memory_data.importance_score,
            confidence_score=memory_data.confidence_score,
            source=memory_data.source,
            context_data=memory_data.context_data,
            related_entities=memory_data.related_entities,
            expires_at=memory_data.expires_at
        )
        
        self.db.add(db_memory)
        await self.db.commit()
        await self.db.refresh(db_memory)
        
        return db_memory
    
    async def update(self, memory_id: int, memory_data: MemoryUpdate) -> Optional[Memory]:
        """Update memory."""
        db_memory = await self.get_by_id(memory_id)
        if not db_memory:
            return None
        
        update_data = memory_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_memory, field, value)
        
        db_memory.updated_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(db_memory)
        
        return db_memory
    
    async def delete(self, memory_id: int) -> bool:
        """Delete memory."""
        db_memory = await self.get_by_id(memory_id)
        if not db_memory:
            return False
        
        await self.db.delete(db_memory)
        await self.db.commit()
        
        return True
    
    async def archive(self, memory_id: int) -> Optional[Memory]:
        """Archive a memory (deactivate it)."""
        db_memory = await self.get_by_id(memory_id)
        if not db_memory:
            return None
        
        db_memory.is_active = False
        db_memory.updated_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(db_memory)
        
        return db_memory
    
    async def activate(self, memory_id: int) -> Optional[Memory]:
        """Activate a memory."""
        db_memory = await self.get_by_id(memory_id)
        if not db_memory:
            return None
        
        db_memory.is_active = True
        db_memory.updated_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(db_memory)
        
        return db_memory
    
    async def update_access(self, memory_id: int) -> Optional[Memory]:
        """Update memory access count and timestamp."""
        db_memory = await self.get_by_id(memory_id)
        if not db_memory:
            return None
        
        db_memory.access_count += 1
        db_memory.last_accessed_at = datetime.utcnow()
        db_memory.updated_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(db_memory)
        
        return db_memory
    
    async def get_expired_memories(self) -> List[Memory]:
        """Get memories that have expired."""
        query = select(Memory).where(
            and_(
                Memory.expires_at.isnot(None),
                Memory.expires_at < datetime.utcnow(),
                Memory.is_active == True
            )
        )
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def cleanup_expired_memories(self) -> int:
        """Archive expired memories and return count of cleaned memories."""
        expired_memories = await self.get_expired_memories()
        
        count = 0
        for memory in expired_memories:
            memory.is_active = False
            memory.updated_at = datetime.utcnow()
            count += 1
        
        await self.db.commit()
        return count
    
    async def get_memory_statistics(self, user_id: int = None) -> dict:
        """Get memory statistics."""
        query = select(
            Memory.memory_type,
            func.count(Memory.id).label('count'),
            func.avg(Memory.importance_score).label('avg_importance')
        ).where(Memory.is_active == True)
        
        if user_id:
            query = query.where(Memory.user_id == user_id)
        
        query = query.group_by(Memory.memory_type)
        
        result = await self.db.execute(query)
        stats = result.fetchall()
        
        return {
            "total_memories": sum(stat.count for stat in stats),
            "by_type": {
                stat.memory_type: {
                    "count": stat.count,
                    "avg_importance": float(stat.avg_importance) if stat.avg_importance else 0
                }
                for stat in stats
            }
        }
