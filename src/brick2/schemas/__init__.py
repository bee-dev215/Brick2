"""Pydantic schemas."""

from .user import UserCreate, UserUpdate, UserResponse
from .campaign import CampaignCreate, CampaignUpdate, CampaignResponse
from .ad import AdCreate, AdUpdate, AdResponse
from .performance import PerformanceCreate, PerformanceUpdate, PerformanceResponse
from .lead import LeadCreate, LeadUpdate, LeadResponse
from .orchestration_session import (
    OrchestrationSessionCreate, 
    OrchestrationSessionUpdate, 
    OrchestrationSessionResponse
)
from .memory import MemoryCreate, MemoryUpdate, MemoryResponse
from .knowledge_node import KnowledgeNodeCreate, KnowledgeNodeUpdate, KnowledgeNodeResponse
from .knowledge_relationship import (
    KnowledgeRelationshipCreate, 
    KnowledgeRelationshipUpdate, 
    KnowledgeRelationshipResponse
)
from .platform import (
    GoogleAdsCampaignCreate, FacebookAdsCampaignCreate, LinkedInAdsCampaignCreate,
    GoogleAdsAdCreate, FacebookAdsAdCreate, LinkedInAdsAdCreate,
    PlatformValidationResult, PlatformMetrics, PlatformSyncResult
)

__all__ = [
    # User schemas
    "UserCreate", "UserUpdate", "UserResponse", "UserInDB",
    # Campaign schemas
    "CampaignCreate", "CampaignUpdate", "CampaignResponse", "CampaignInDB",
    # Ad schemas
    "AdCreate", "AdUpdate", "AdResponse", "AdInDB",
    # Performance schemas
    "PerformanceCreate", "PerformanceUpdate", "PerformanceResponse", "PerformanceInDB",
    # Lead schemas
    "LeadCreate", "LeadUpdate", "LeadResponse", "LeadInDB",
    # Orchestration session schemas
    "OrchestrationSessionCreate", "OrchestrationSessionUpdate", "OrchestrationSessionResponse", "OrchestrationSessionInDB",
    # Memory schemas
    "MemoryCreate", "MemoryUpdate", "MemoryResponse", "MemoryInDB",
    # Knowledge schemas
    "KnowledgeNodeCreate", "KnowledgeNodeUpdate", "KnowledgeNodeResponse", "KnowledgeNodeInDB",
    "KnowledgeRelationshipCreate", "KnowledgeRelationshipUpdate", "KnowledgeRelationshipResponse", "KnowledgeRelationshipInDB",
    # Platform schemas
    "GoogleAdsCampaignCreate", "FacebookAdsCampaignCreate", "LinkedInAdsCampaignCreate",
    "GoogleAdsAdCreate", "FacebookAdsAdCreate", "LinkedInAdsAdCreate",
    "PlatformValidationResult", "PlatformMetrics", "PlatformSyncResult",
]
