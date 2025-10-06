"""Knowledge relationship service."""

from typing import List, Optional
from datetime import datetime
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models.knowledge_relationship import KnowledgeRelationship
from ..models.knowledge_node import KnowledgeNode
from ..schemas.knowledge_relationship import KnowledgeRelationshipCreate, KnowledgeRelationshipUpdate


class KnowledgeRelationshipService:
    """Service for managing knowledge relationships."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_all(
        self, 
        skip: int = 0, 
        limit: int = 100,
        relationship_type: str = None,
        source_node_id: int = None,
        target_node_id: int = None,
        is_active: bool = None
    ) -> List[KnowledgeRelationship]:
        """Get all knowledge relationships with optional filtering."""
        query = select(KnowledgeRelationship).options(
            selectinload(KnowledgeRelationship.source_node),
            selectinload(KnowledgeRelationship.target_node)
        )
        
        conditions = []
        if relationship_type:
            conditions.append(KnowledgeRelationship.relationship_type == relationship_type)
        if source_node_id:
            conditions.append(KnowledgeRelationship.source_node_id == source_node_id)
        if target_node_id:
            conditions.append(KnowledgeRelationship.target_node_id == target_node_id)
        if is_active is not None:
            conditions.append(KnowledgeRelationship.is_active == is_active)
        
        if conditions:
            query = query.where(and_(*conditions))
        
        query = query.offset(skip).limit(limit).order_by(KnowledgeRelationship.strength.desc(), KnowledgeRelationship.created_at.desc())
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_by_id(self, relationship_id: int) -> Optional[KnowledgeRelationship]:
        """Get knowledge relationship by ID."""
        query = select(KnowledgeRelationship).options(
            selectinload(KnowledgeRelationship.source_node),
            selectinload(KnowledgeRelationship.target_node)
        ).where(KnowledgeRelationship.id == relationship_id)
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_node(
        self, 
        node_id: int,
        skip: int = 0, 
        limit: int = 100,
        relationship_type: str = None,
        direction: str = "both"  # "incoming", "outgoing", "both"
    ) -> List[KnowledgeRelationship]:
        """Get relationships for a specific node."""
        query = select(KnowledgeRelationship).options(
            selectinload(KnowledgeRelationship.source_node),
            selectinload(KnowledgeRelationship.target_node)
        )
        
        # Build conditions based on direction
        if direction == "incoming":
            conditions = [KnowledgeRelationship.target_node_id == node_id]
        elif direction == "outgoing":
            conditions = [KnowledgeRelationship.source_node_id == node_id]
        else:  # both
            conditions = [
                or_(
                    KnowledgeRelationship.source_node_id == node_id,
                    KnowledgeRelationship.target_node_id == node_id
                )
            ]
        
        conditions.append(KnowledgeRelationship.is_active == True)
        
        if relationship_type:
            conditions.append(KnowledgeRelationship.relationship_type == relationship_type)
        
        query = query.where(and_(*conditions))
        query = query.offset(skip).limit(limit).order_by(KnowledgeRelationship.strength.desc(), KnowledgeRelationship.created_at.desc())
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_by_nodes(self, source_node_id: int, target_node_id: int) -> List[KnowledgeRelationship]:
        """Get relationships between two specific nodes."""
        query = select(KnowledgeRelationship).options(
            selectinload(KnowledgeRelationship.source_node),
            selectinload(KnowledgeRelationship.target_node)
        ).where(
            and_(
                KnowledgeRelationship.source_node_id == source_node_id,
                KnowledgeRelationship.target_node_id == target_node_id,
                KnowledgeRelationship.is_active == True
            )
        )
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def create(self, relationship_data: KnowledgeRelationshipCreate) -> KnowledgeRelationship:
        """Create a new knowledge relationship."""
        # Check if both nodes exist
        source_node = await self.db.execute(
            select(KnowledgeNode).where(KnowledgeNode.id == relationship_data.source_node_id)
        )
        source_node = source_node.scalar_one_or_none()
        
        target_node = await self.db.execute(
            select(KnowledgeNode).where(KnowledgeNode.id == relationship_data.target_node_id)
        )
        target_node = target_node.scalar_one_or_none()
        
        if not source_node or not target_node:
            raise ValueError("Source or target node not found")
        
        db_relationship = KnowledgeRelationship(
            source_node_id=relationship_data.source_node_id,
            target_node_id=relationship_data.target_node_id,
            relationship_type=relationship_data.relationship_type,
            strength=relationship_data.strength,
            weight=relationship_data.weight,
            description=relationship_data.description,
            confidence=relationship_data.confidence,
            is_symmetric=relationship_data.is_symmetric
        )
        
        self.db.add(db_relationship)
        await self.db.commit()
        await self.db.refresh(db_relationship)
        
        # If the relationship is symmetric, create the reverse relationship
        if relationship_data.is_symmetric:
            reverse_relationship = KnowledgeRelationship(
                source_node_id=relationship_data.target_node_id,
                target_node_id=relationship_data.source_node_id,
                relationship_type=relationship_data.relationship_type,
                strength=relationship_data.strength,
                weight=relationship_data.weight,
                description=relationship_data.description,
                confidence=relationship_data.confidence,
                is_symmetric=relationship_data.is_symmetric
            )
            
            self.db.add(reverse_relationship)
            await self.db.commit()
        
        return db_relationship
    
    async def update(self, relationship_id: int, relationship_data: KnowledgeRelationshipUpdate) -> Optional[KnowledgeRelationship]:
        """Update knowledge relationship."""
        db_relationship = await self.get_by_id(relationship_id)
        if not db_relationship:
            return None
        
        update_data = relationship_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_relationship, field, value)
        
        db_relationship.updated_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(db_relationship)
        
        return db_relationship
    
    async def delete(self, relationship_id: int) -> bool:
        """Delete knowledge relationship."""
        db_relationship = await self.get_by_id(relationship_id)
        if not db_relationship:
            return False
        
        await self.db.delete(db_relationship)
        await self.db.commit()
        
        return True
    
    async def strengthen_relationship(self, relationship_id: int, increment: float = 0.1) -> Optional[KnowledgeRelationship]:
        """Strengthen a relationship by incrementing its strength."""
        db_relationship = await self.get_by_id(relationship_id)
        if not db_relationship:
            return None
        
        new_strength = min(1.0, db_relationship.strength + increment)
        db_relationship.strength = new_strength
        db_relationship.evidence_count += 1
        db_relationship.last_observed_at = datetime.utcnow()
        db_relationship.updated_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(db_relationship)
        
        return db_relationship
    
    async def weaken_relationship(self, relationship_id: int, decrement: float = 0.1) -> Optional[KnowledgeRelationship]:
        """Weaken a relationship by decrementing its strength."""
        db_relationship = await self.get_by_id(relationship_id)
        if not db_relationship:
            return None
        
        new_strength = max(0.0, db_relationship.strength - decrement)
        db_relationship.strength = new_strength
        db_relationship.updated_at = datetime.utcnow()
        
        # If strength becomes 0, deactivate the relationship
        if new_strength == 0:
            db_relationship.is_active = False
        
        await self.db.commit()
        await self.db.refresh(db_relationship)
        
        return db_relationship
    
    async def find_strongest_relationships(
        self, 
        node_id: int, 
        limit: int = 10,
        relationship_type: str = None
    ) -> List[KnowledgeRelationship]:
        """Find the strongest relationships for a node."""
        query = select(KnowledgeRelationship).options(
            selectinload(KnowledgeRelationship.source_node),
            selectinload(KnowledgeRelationship.target_node)
        ).where(
            and_(
                or_(
                    KnowledgeRelationship.source_node_id == node_id,
                    KnowledgeRelationship.target_node_id == node_id
                ),
                KnowledgeRelationship.is_active == True
            )
        )
        
        if relationship_type:
            query = query.where(KnowledgeRelationship.relationship_type == relationship_type)
        
        query = query.order_by(KnowledgeRelationship.strength.desc()).limit(limit)
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_relationship_statistics(self) -> dict:
        """Get relationship statistics."""
        # Count by type
        type_query = select(
            KnowledgeRelationship.relationship_type,
            KnowledgeRelationship.id
        ).where(KnowledgeRelationship.is_active == True)
        
        type_result = await self.db.execute(type_query)
        relationships = type_result.fetchall()
        
        type_counts = {}
        total_strength = 0
        total_relationships = 0
        
        for rel_type, rel_id in relationships:
            type_counts[rel_type] = type_counts.get(rel_type, 0) + 1
            total_relationships += 1
        
        # Get average strength
        strength_query = select(KnowledgeRelationship.strength).where(
            KnowledgeRelationship.is_active == True
        )
        strength_result = await self.db.execute(strength_query)
        strengths = strength_result.scalars().all()
        
        if strengths:
            avg_strength = sum(strengths) / len(strengths)
        else:
            avg_strength = 0
        
        return {
            "total_relationships": total_relationships,
            "by_type": type_counts,
            "average_strength": avg_strength
        }
    
    async def get_most_connected_nodes(self, limit: int = 10) -> List[dict]:
        """Get nodes with the most connections."""
        # This is a simplified implementation
        # In a production system, you'd want to use a proper graph query
        
        # Get all active relationships
        query = select(KnowledgeRelationship).where(KnowledgeRelationship.is_active == True)
        result = await self.db.execute(query)
        relationships = result.scalars().all()
        
        # Count connections per node
        node_connections = {}
        for rel in relationships:
            node_connections[rel.source_node_id] = node_connections.get(rel.source_node_id, 0) + 1
            node_connections[rel.target_node_id] = node_connections.get(rel.target_node_id, 0) + 1
        
        # Sort by connection count and get top nodes
        sorted_nodes = sorted(node_connections.items(), key=lambda x: x[1], reverse=True)[:limit]
        
        # Get node details
        node_ids = [node_id for node_id, _ in sorted_nodes]
        if node_ids:
            nodes_query = select(KnowledgeNode).where(KnowledgeNode.id.in_(node_ids))
            nodes_result = await self.db.execute(nodes_query)
            nodes = {node.id: node for node in nodes_result.scalars().all()}
            
            return [
                {
                    "node_id": node_id,
                    "node_name": nodes[node_id].name,
                    "node_type": nodes[node_id].node_type,
                    "connection_count": connection_count
                }
                for node_id, connection_count in sorted_nodes
                if node_id in nodes
            ]
        
        return []
