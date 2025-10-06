"""Knowledge node service."""

from typing import List, Optional
from datetime import datetime
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models.knowledge_node import KnowledgeNode
from ..models.knowledge_relationship import KnowledgeRelationship
from ..schemas.knowledge_node import KnowledgeNodeCreate, KnowledgeNodeUpdate


class KnowledgeNodeService:
    """Service for managing knowledge nodes."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_all(
        self, 
        skip: int = 0, 
        limit: int = 100,
        node_type: str = None,
        category: str = None,
        is_active: bool = None
    ) -> List[KnowledgeNode]:
        """Get all knowledge nodes with optional filtering."""
        query = select(KnowledgeNode)
        
        conditions = []
        if node_type:
            conditions.append(KnowledgeNode.node_type == node_type)
        if category:
            conditions.append(KnowledgeNode.category == category)
        if is_active is not None:
            conditions.append(KnowledgeNode.is_active == is_active)
        
        if conditions:
            query = query.where(and_(*conditions))
        
        query = query.offset(skip).limit(limit).order_by(KnowledgeNode.importance_score.desc(), KnowledgeNode.created_at.desc())
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_by_id(self, node_id: int) -> Optional[KnowledgeNode]:
        """Get knowledge node by ID."""
        query = select(KnowledgeNode).where(KnowledgeNode.id == node_id)
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_type(
        self, 
        node_type: str,
        skip: int = 0, 
        limit: int = 100,
        category: str = None
    ) -> List[KnowledgeNode]:
        """Get knowledge nodes by type."""
        query = select(KnowledgeNode).where(KnowledgeNode.node_type == node_type)
        
        conditions = [KnowledgeNode.node_type == node_type, KnowledgeNode.is_active == True]
        if category:
            conditions.append(KnowledgeNode.category == category)
        
        query = query.where(and_(*conditions))
        query = query.offset(skip).limit(limit).order_by(KnowledgeNode.importance_score.desc(), KnowledgeNode.created_at.desc())
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_by_external_id(self, external_id: str) -> Optional[KnowledgeNode]:
        """Get knowledge node by external ID."""
        query = select(KnowledgeNode).where(KnowledgeNode.external_id == external_id)
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def search(self, query_text: str, node_type: str = None) -> List[KnowledgeNode]:
        """Search knowledge nodes by name or description."""
        query = select(KnowledgeNode).where(
            and_(
                or_(
                    KnowledgeNode.name.ilike(f"%{query_text}%"),
                    KnowledgeNode.description.ilike(f"%{query_text}%")
                ),
                KnowledgeNode.is_active == True
            )
        )
        
        if node_type:
            query = query.where(KnowledgeNode.node_type == node_type)
        
        query = query.order_by(KnowledgeNode.importance_score.desc(), KnowledgeNode.created_at.desc())
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def create(self, node_data: KnowledgeNodeCreate) -> KnowledgeNode:
        """Create a new knowledge node."""
        db_node = KnowledgeNode(
            node_type=node_data.node_type,
            node_id=node_data.node_id,
            external_id=node_data.external_id,
            name=node_data.name,
            description=node_data.description,
            properties=node_data.properties,
            category=node_data.category,
            tags=node_data.tags,
            importance_score=node_data.importance_score,
            relevance_score=node_data.relevance_score,
            confidence_score=node_data.confidence_score
        )
        
        self.db.add(db_node)
        await self.db.commit()
        await self.db.refresh(db_node)
        
        return db_node
    
    async def update(self, node_id: int, node_data: KnowledgeNodeUpdate) -> Optional[KnowledgeNode]:
        """Update knowledge node."""
        db_node = await self.get_by_id(node_id)
        if not db_node:
            return None
        
        update_data = node_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_node, field, value)
        
        db_node.updated_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(db_node)
        
        return db_node
    
    async def delete(self, node_id: int) -> bool:
        """Delete knowledge node."""
        db_node = await self.get_by_id(node_id)
        if not db_node:
            return False
        
        # First, delete all relationships involving this node
        await self.db.execute(
            select(KnowledgeRelationship).where(
                or_(
                    KnowledgeRelationship.source_node_id == node_id,
                    KnowledgeRelationship.target_node_id == node_id
                )
            )
        )
        
        await self.db.delete(db_node)
        await self.db.commit()
        
        return True
    
    async def get_neighbors(
        self, 
        node_id: int, 
        max_depth: int = 1,
        relationship_types: List[str] = None
    ) -> List[KnowledgeNode]:
        """Get neighboring nodes in the knowledge graph."""
        # This is a simplified implementation for depth=1
        # For deeper traversal, you'd need a recursive query or use a graph database
        
        if max_depth > 1:
            # For now, limit to depth 1
            max_depth = 1
        
        # Get relationships where this node is either source or target
        relationship_query = select(KnowledgeRelationship).where(
            and_(
                or_(
                    KnowledgeRelationship.source_node_id == node_id,
                    KnowledgeRelationship.target_node_id == node_id
                ),
                KnowledgeRelationship.is_active == True
            )
        )
        
        if relationship_types:
            relationship_query = relationship_query.where(
                KnowledgeRelationship.relationship_type.in_(relationship_types)
            )
        
        relationships_result = await self.db.execute(relationship_query)
        relationships = relationships_result.scalars().all()
        
        # Collect all neighbor node IDs
        neighbor_ids = set()
        for rel in relationships:
            if rel.source_node_id == node_id:
                neighbor_ids.add(rel.target_node_id)
            else:
                neighbor_ids.add(rel.source_node_id)
        
        # Get the actual nodes
        if neighbor_ids:
            nodes_query = select(KnowledgeNode).where(
                and_(
                    KnowledgeNode.id.in_(neighbor_ids),
                    KnowledgeNode.is_active == True
                )
            ).order_by(KnowledgeNode.importance_score.desc())
            
            nodes_result = await self.db.execute(nodes_query)
            return nodes_result.scalars().all()
        
        return []
    
    async def find_path(
        self, 
        source_node_id: int, 
        target_node_id: int, 
        max_depth: int = 5,
        relationship_types: List[str] = None
    ) -> List[KnowledgeNode]:
        """Find a path between two nodes in the knowledge graph."""
        # This is a simplified BFS implementation
        # In a production system, you might want to use a proper graph traversal library
        
        if source_node_id == target_node_id:
            source_node = await self.get_by_id(source_node_id)
            return [source_node] if source_node else []
        
        visited = set()
        queue = [(source_node_id, [source_node_id])]
        
        while queue and len(queue[0][1]) <= max_depth:
            current_id, path = queue.pop(0)
            
            if current_id in visited:
                continue
            
            visited.add(current_id)
            
            # Get neighbors of current node
            neighbors = await self.get_neighbors(current_id, max_depth=1, relationship_types=relationship_types)
            
            for neighbor in neighbors:
                if neighbor.id == target_node_id:
                    # Found the target! Build the full path
                    full_path = []
                    for node_id in path:
                        node = await self.get_by_id(node_id)
                        if node:
                            full_path.append(node)
                    
                    target_node = await self.get_by_id(target_node_id)
                    if target_node:
                        full_path.append(target_node)
                    
                    return full_path
                
                if neighbor.id not in visited:
                    queue.append((neighbor.id, path + [neighbor.id]))
        
        return []  # No path found
    
    async def get_node_statistics(self, node_id: int) -> dict:
        """Get statistics for a specific node."""
        node = await self.get_by_id(node_id)
        if not node:
            return {}
        
        # Count relationships
        outgoing_count = await self.db.execute(
            select(KnowledgeRelationship).where(
                and_(
                    KnowledgeRelationship.source_node_id == node_id,
                    KnowledgeRelationship.is_active == True
                )
            )
        )
        
        incoming_count = await self.db.execute(
            select(KnowledgeRelationship).where(
                and_(
                    KnowledgeRelationship.target_node_id == node_id,
                    KnowledgeRelationship.is_active == True
                )
            )
        )
        
        return {
            "node_id": node_id,
            "node_name": node.name,
            "node_type": node.node_type,
            "outgoing_relationships": len(outgoing_count.scalars().all()),
            "incoming_relationships": len(incoming_count.scalars().all()),
            "importance_score": node.importance_score,
            "relevance_score": node.relevance_score,
            "confidence_score": node.confidence_score,
            "created_at": node.created_at,
            "updated_at": node.updated_at
        }
    
    async def update_node_data(self, node_id: int, data_timestamp: datetime = None) -> Optional[KnowledgeNode]:
        """Update the last_updated_data timestamp for a node."""
        db_node = await self.get_by_id(node_id)
        if not db_node:
            return None
        
        db_node.last_updated_data = data_timestamp or datetime.utcnow()
        db_node.updated_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(db_node)
        
        return db_node
