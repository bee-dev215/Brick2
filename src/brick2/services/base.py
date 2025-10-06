"""Base service class."""

from abc import ABC
from typing import Generic, TypeVar, Type, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from ..models.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseService(Generic[ModelType], ABC):
    """Base service class with common CRUD operations."""
    
    def __init__(self, db: AsyncSession, model: Type[ModelType]):
        self.db = db
        self.model = model
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Get all records with pagination."""
        result = await self.db.execute(
            select(self.model)
            .offset(skip)
            .limit(limit)
            .order_by(self.model.created_at.desc())
        )
        return result.scalars().all()
    
    async def get_by_id(self, record_id: int) -> Optional[ModelType]:
        """Get record by ID."""
        result = await self.db.execute(
            select(self.model).where(self.model.id == record_id)
        )
        return result.scalar_one_or_none()
    
    async def create(self, **kwargs) -> ModelType:
        """Create a new record."""
        db_record = self.model(**kwargs)
        self.db.add(db_record)
        await self.db.commit()
        await self.db.refresh(db_record)
        return db_record
    
    async def update(self, record_id: int, **kwargs) -> Optional[ModelType]:
        """Update a record."""
        db_record = await self.get_by_id(record_id)
        if not db_record:
            return None
        
        for field, value in kwargs.items():
            if hasattr(db_record, field) and value is not None:
                setattr(db_record, field, value)
        
        await self.db.commit()
        await self.db.refresh(db_record)
        return db_record
    
    async def delete(self, record_id: int) -> bool:
        """Delete a record."""
        db_record = await self.get_by_id(record_id)
        if not db_record:
            return False
        
        await self.db.delete(db_record)
        await self.db.commit()
        return True
    
    async def count(self) -> int:
        """Count total records."""
        result = await self.db.execute(select(self.model))
        return len(result.scalars().all())
