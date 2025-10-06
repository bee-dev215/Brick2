"""Knowledge node model for BRICK 1 integration."""

from sqlalchemy import Column, String, Text, Integer, JSON, Float, DateTime, Boolean
from sqlalchemy.orm import relationship

from .base import BaseModel


class KnowledgeNode(BaseModel):
    """Knowledge node model for building a knowledge graph."""
    
    __tablename__ = "knowledge_nodes"
    
    # Node identification
    node_type = Column(String(50), nullable=False, index=True)  # 'campaign', 'audience', 'creative', 'strategy', 'platform', 'metric', 'concept'
    node_id = Column(String(255), nullable=True, index=True)  # Reference to actual entity (campaign ID, etc.)
    external_id = Column(String(255), nullable=True, index=True)  # External system reference
    
    # Node properties
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    properties = Column(JSON, nullable=True)  # Flexible properties for different node types
    
    # Node classification
    category = Column(String(50), nullable=True, index=True)  # Sub-category within node_type
    tags = Column(JSON, nullable=True)  # Array of tags for flexible categorization
    
    # Node metrics and scoring
    importance_score = Column(Integer, default=50)  # 1-100 importance in the knowledge graph
    relevance_score = Column(Float, nullable=True)  # 0.0-1.0 relevance score
    confidence_score = Column(Float, nullable=True)  # 0.0-1.0 confidence in this node's data
    
    # Node lifecycle
    is_active = Column(Boolean, default=True, index=True)
    last_updated_data = Column(DateTime(timezone=True), nullable=True)  # When the underlying data was last updated
    
    # Relationships (handled by separate KnowledgeRelationship model)
    # incoming_relationships = relationship("KnowledgeRelationship", foreign_keys="KnowledgeRelationship.target_node_id")
    # outgoing_relationships = relationship("KnowledgeRelationship", foreign_keys="KnowledgeRelationship.source_node_id")
