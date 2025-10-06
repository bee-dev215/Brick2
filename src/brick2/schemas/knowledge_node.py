"""Knowledge node schemas."""

from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class KnowledgeNodeBase(BaseModel):
    """Base knowledge node schema."""
    
    node_type: str = Field(..., description="Type of knowledge node")
    node_id: Optional[str] = Field(None, description="Reference to actual entity")
    external_id: Optional[str] = Field(None, description="External system reference")
    name: str = Field(..., description="Node name")
    description: Optional[str] = Field(None, description="Node description")
    properties: Optional[Dict[str, Any]] = Field(None, description="Node properties")
    category: Optional[str] = Field(None, description="Node category")
    tags: Optional[List[str]] = Field(None, description="Node tags")
    importance_score: int = Field(default=50, ge=1, le=100, description="Importance score")
    relevance_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Relevance score")
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Confidence score")


class KnowledgeNodeCreate(KnowledgeNodeBase):
    """Schema for creating a knowledge node."""
    pass


class KnowledgeNodeUpdate(BaseModel):
    """Schema for updating a knowledge node."""
    
    name: Optional[str] = Field(None, description="Updated name")
    description: Optional[str] = Field(None, description="Updated description")
    properties: Optional[Dict[str, Any]] = Field(None, description="Updated properties")
    category: Optional[str] = Field(None, description="Updated category")
    tags: Optional[List[str]] = Field(None, description="Updated tags")
    importance_score: Optional[int] = Field(None, ge=1, le=100, description="Updated importance score")
    relevance_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Updated relevance score")
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Updated confidence score")
    is_active: Optional[bool] = Field(None, description="Node active status")


class KnowledgeNodeResponse(KnowledgeNodeBase):
    """Schema for knowledge node response."""
    
    id: int
    is_active: bool
    last_updated_data: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class KnowledgeNodeList(BaseModel):
    """Schema for knowledge node list response."""
    
    nodes: list[KnowledgeNodeResponse]
    total: int
    skip: int
    limit: int
