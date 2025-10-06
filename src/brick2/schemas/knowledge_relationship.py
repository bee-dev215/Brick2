"""Knowledge relationship schemas."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class KnowledgeRelationshipBase(BaseModel):
    """Base knowledge relationship schema."""
    
    relationship_type: str = Field(..., description="Type of relationship")
    strength: float = Field(default=1.0, ge=0.0, le=1.0, description="Relationship strength")
    weight: float = Field(default=1.0, description="Relationship weight")
    description: Optional[str] = Field(None, description="Relationship description")
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="Relationship confidence")
    is_symmetric: bool = Field(default=False, description="Whether relationship is symmetric")


class KnowledgeRelationshipCreate(KnowledgeRelationshipBase):
    """Schema for creating a knowledge relationship."""
    
    source_node_id: int = Field(..., description="Source node ID")
    target_node_id: int = Field(..., description="Target node ID")


class KnowledgeRelationshipUpdate(BaseModel):
    """Schema for updating a knowledge relationship."""
    
    relationship_type: Optional[str] = Field(None, description="Updated relationship type")
    strength: Optional[float] = Field(None, ge=0.0, le=1.0, description="Updated strength")
    weight: Optional[float] = Field(None, description="Updated weight")
    description: Optional[str] = Field(None, description="Updated description")
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="Updated confidence")
    is_active: Optional[bool] = Field(None, description="Relationship active status")


class KnowledgeRelationshipResponse(KnowledgeRelationshipBase):
    """Schema for knowledge relationship response."""
    
    id: int
    source_node_id: int
    target_node_id: int
    is_active: bool
    evidence_count: int
    last_observed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class KnowledgeRelationshipList(BaseModel):
    """Schema for knowledge relationship list response."""
    
    relationships: list[KnowledgeRelationshipResponse]
    total: int
    skip: int
    limit: int
