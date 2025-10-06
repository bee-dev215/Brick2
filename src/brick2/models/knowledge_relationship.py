"""Knowledge relationship model for BRICK 1 integration."""

from sqlalchemy import Column, String, Integer, ForeignKey, Float, DateTime, Boolean
from sqlalchemy.orm import relationship

from .base import BaseModel


class KnowledgeRelationship(BaseModel):
    """Knowledge relationship model for connecting nodes in the knowledge graph."""
    
    __tablename__ = "knowledge_relationships"
    
    # Relationship endpoints
    source_node_id = Column(Integer, ForeignKey("knowledge_nodes.id"), nullable=False, index=True)
    target_node_id = Column(Integer, ForeignKey("knowledge_nodes.id"), nullable=False, index=True)
    
    # Relationship properties
    relationship_type = Column(String(50), nullable=False, index=True)  # 'improves', 'conflicts_with', 'similar_to', 'depends_on', 'causes', 'influences'
    strength = Column(Float, default=1.0)  # Relationship strength (0.0-1.0)
    weight = Column(Float, default=1.0)  # Relationship weight for graph algorithms
    
    # Relationship metadata
    description = Column(String(500), nullable=True)
    confidence = Column(Float, nullable=True)  # 0.0-1.0 confidence in this relationship
    
    # Relationship lifecycle
    is_active = Column(Boolean, default=True, index=True)
    is_symmetric = Column(Boolean, default=False)  # Whether this relationship works both ways
    
    # Usage and validation
    evidence_count = Column(Integer, default=1)  # How many times this relationship has been observed
    last_observed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    source_node = relationship("KnowledgeNode", foreign_keys=[source_node_id], backref="outgoing_relationships")
    target_node = relationship("KnowledgeNode", foreign_keys=[target_node_id], backref="incoming_relationships")
