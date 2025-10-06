"""Platform-specific services for different advertising platforms."""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.campaign import Campaign
from ..models.ad import Ad
from ..models.performance import Performance
from ..schemas.campaign import CampaignCreate, CampaignUpdate
from ..schemas.ad import AdCreate, AdUpdate
from ..schemas.performance import PerformanceCreate


class PlatformService(ABC):
    """Abstract base class for platform-specific services."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.platform_name = self.get_platform_name()
    
    @abstractmethod
    def get_platform_name(self) -> str:
        """Get the platform name."""
        pass
    
    @abstractmethod
    async def validate_campaign_data(self, campaign_data: CampaignCreate) -> Dict[str, Any]:
        """Validate platform-specific campaign data."""
        pass
    
    @abstractmethod
    async def validate_ad_data(self, ad_data: AdCreate) -> Dict[str, Any]:
        """Validate platform-specific ad data."""
        pass
    
    @abstractmethod
    async def create_campaign(self, campaign_data: CampaignCreate, owner_id: int) -> Campaign:
        """Create a platform-specific campaign."""
        pass
    
    @abstractmethod
    async def create_ad(self, ad_data: AdCreate) -> Ad:
        """Create a platform-specific ad."""
        pass
    
    @abstractmethod
    async def get_platform_metrics(self, campaign_id: int) -> Dict[str, Any]:
        """Get platform-specific metrics."""
        pass
    
    @abstractmethod
    async def sync_external_data(self, campaign_id: int) -> Dict[str, Any]:
        """Sync data with external platform API."""
        pass


class GoogleAdsService(PlatformService):
    """Google Ads platform service."""
    
    def get_platform_name(self) -> str:
        return "Google"
    
    async def validate_campaign_data(self, campaign_data: CampaignCreate) -> Dict[str, Any]:
        """Validate Google Ads campaign data."""
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "platform_specific": {}
        }
        
        # Google Ads specific validations
        if campaign_data.budget and campaign_data.budget < 1000:  # $10 minimum
            validation_result["errors"].append("Google Ads minimum budget is $10.00")
            validation_result["valid"] = False
        
        if campaign_data.daily_budget and campaign_data.daily_budget < 100:  # $1 minimum
            validation_result["errors"].append("Google Ads minimum daily budget is $1.00")
            validation_result["valid"] = False
        
        # Google Ads campaign types
        if hasattr(campaign_data, 'campaign_type'):
            valid_types = ["search", "display", "video", "shopping", "app", "smart"]
            if campaign_data.campaign_type not in valid_types:
                validation_result["errors"].append(f"Invalid Google Ads campaign type. Must be one of: {valid_types}")
                validation_result["valid"] = False
        
        validation_result["platform_specific"] = {
            "google_ads_account_id": getattr(campaign_data, 'google_ads_account_id', None),
            "campaign_type": getattr(campaign_data, 'campaign_type', 'search'),
            "bidding_strategy": getattr(campaign_data, 'bidding_strategy', 'manual_cpc'),
        }
        
        return validation_result
    
    async def validate_ad_data(self, ad_data: AdCreate) -> Dict[str, Any]:
        """Validate Google Ads ad data."""
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "platform_specific": {}
        }
        
        # Google Ads specific validations
        valid_ad_types = ["search", "display", "video", "shopping", "app", "responsive_search", "responsive_display"]
        if ad_data.ad_type not in valid_ad_types:
            validation_result["errors"].append(f"Invalid Google Ads ad type. Must be one of: {valid_ad_types}")
            validation_result["valid"] = False
        
        # Google Ads text limits
        if ad_data.title and len(ad_data.title) > 30:
            validation_result["warnings"].append("Google Ads headlines should be 30 characters or less")
        
        if ad_data.description and len(ad_data.description) > 90:
            validation_result["warnings"].append("Google Ads descriptions should be 90 characters or less")
        
        # Google Ads bidding
        valid_bid_types = ["cpc", "cpm", "cpa", "target_cpa", "target_roas", "maximize_clicks", "maximize_conversions"]
        if ad_data.bid_type and ad_data.bid_type not in valid_bid_types:
            validation_result["errors"].append(f"Invalid Google Ads bid type. Must be one of: {valid_bid_types}")
            validation_result["valid"] = False
        
        validation_result["platform_specific"] = {
            "final_urls": getattr(ad_data, 'final_urls', []),
            "headlines": getattr(ad_data, 'headlines', []),
            "descriptions": getattr(ad_data, 'descriptions', []),
            "keywords": getattr(ad_data, 'keywords', []),
            "ad_group_id": getattr(ad_data, 'ad_group_id', None),
        }
        
        return validation_result
    
    async def create_campaign(self, campaign_data: CampaignCreate, owner_id: int) -> Campaign:
        """Create a Google Ads campaign."""
        # Add Google Ads specific fields
        campaign = Campaign(
            platform="Google",
            name=campaign_data.name,
            external_id=campaign_data.external_id,
            description=campaign_data.description,
            budget=campaign_data.budget,
            daily_budget=campaign_data.daily_budget,
            start_date=campaign_data.start_date,
            end_date=campaign_data.end_date,
            is_active=campaign_data.is_active,
            owner_id=owner_id,
        )
        
        self.db.add(campaign)
        await self.db.commit()
        await self.db.refresh(campaign)
        return campaign
    
    async def create_ad(self, ad_data: AdCreate) -> Ad:
        """Create a Google Ads ad."""
        ad = Ad(
            title=ad_data.title,
            description=ad_data.description,
            content=ad_data.content,
            ad_type=ad_data.ad_type,
            target_audience=ad_data.target_audience,
            demographics=ad_data.demographics,
            interests=ad_data.interests,
            bid_amount=ad_data.bid_amount,
            bid_type=ad_data.bid_type,
            campaign_id=ad_data.campaign_id,
            media_urls=ad_data.media_urls,
            landing_page_url=ad_data.landing_page_url,
        )
        
        self.db.add(ad)
        await self.db.commit()
        await self.db.refresh(ad)
        return ad
    
    async def get_platform_metrics(self, campaign_id: int) -> Dict[str, Any]:
        """Get Google Ads specific metrics."""
        return {
            "platform": "Google",
            "metrics": {
                "quality_score": 8.5,
                "search_impression_share": 0.75,
                "search_absolute_top_impression_share": 0.45,
                "click_share": 0.68,
                "conversion_rate": 0.025,
                "cost_per_conversion": 45.50,
                "return_on_ad_spend": 3.2,
            },
            "recommendations": [
                "Improve Quality Score by optimizing ad relevance",
                "Increase bid to improve impression share",
                "Add negative keywords to reduce irrelevant clicks"
            ]
        }
    
    async def sync_external_data(self, campaign_id: int) -> Dict[str, Any]:
        """Sync with Google Ads API."""
        # Simulate Google Ads API sync
        return {
            "platform": "Google",
            "sync_status": "success",
            "last_sync": datetime.now(timezone.utc).isoformat(),
            "data_synced": {
                "campaigns": 1,
                "ads": 5,
                "keywords": 25,
                "performance_data": 150
            }
        }


class FacebookAdsService(PlatformService):
    """Facebook Ads platform service."""
    
    def get_platform_name(self) -> str:
        return "Facebook"
    
    async def validate_campaign_data(self, campaign_data: CampaignCreate) -> Dict[str, Any]:
        """Validate Facebook Ads campaign data."""
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "platform_specific": {}
        }
        
        # Facebook Ads specific validations
        if campaign_data.budget and campaign_data.budget < 100:  # $1 minimum
            validation_result["errors"].append("Facebook Ads minimum budget is $1.00")
            validation_result["valid"] = False
        
        # Facebook Ads campaign objectives
        if hasattr(campaign_data, 'campaign_objective'):
            valid_objectives = [
                "awareness", "traffic", "engagement", "leads", "app_promotion", 
                "sales", "reach", "store_visits", "video_views", "messages"
            ]
            if campaign_data.campaign_objective not in valid_objectives:
                validation_result["errors"].append(f"Invalid Facebook Ads objective. Must be one of: {valid_objectives}")
                validation_result["valid"] = False
        
        validation_result["platform_specific"] = {
            "facebook_ad_account_id": getattr(campaign_data, 'facebook_ad_account_id', None),
            "campaign_objective": getattr(campaign_data, 'campaign_objective', 'traffic'),
            "buying_type": getattr(campaign_data, 'buying_type', 'auction'),
            "special_ad_categories": getattr(campaign_data, 'special_ad_categories', []),
        }
        
        return validation_result
    
    async def validate_ad_data(self, ad_data: AdCreate) -> Dict[str, Any]:
        """Validate Facebook Ads ad data."""
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "platform_specific": {}
        }
        
        # Facebook Ads specific validations
        valid_ad_types = ["image", "video", "carousel", "collection", "slideshow", "canvas", "dynamic_product"]
        if ad_data.ad_type not in valid_ad_types:
            validation_result["errors"].append(f"Invalid Facebook Ads ad type. Must be one of: {valid_ad_types}")
            validation_result["valid"] = False
        
        # Facebook Ads text limits
        if ad_data.title and len(ad_data.title) > 27:
            validation_result["warnings"].append("Facebook Ads primary text should be 27 characters or less")
        
        if ad_data.description and len(ad_data.description) > 125:
            validation_result["warnings"].append("Facebook Ads description should be 125 characters or less")
        
        # Facebook Ads bidding
        valid_bid_types = ["cpc", "cpm", "cpa", "oCPM", "oCPC", "lowest_cost", "cost_cap", "bid_cap"]
        if ad_data.bid_type and ad_data.bid_type not in valid_bid_types:
            validation_result["errors"].append(f"Invalid Facebook Ads bid type. Must be one of: {valid_bid_types}")
            validation_result["valid"] = False
        
        validation_result["platform_specific"] = {
            "ad_set_id": getattr(ad_data, 'ad_set_id', None),
            "creative_id": getattr(ad_data, 'creative_id', None),
            "call_to_action": getattr(ad_data, 'call_to_action', 'learn_more'),
            "image_hash": getattr(ad_data, 'image_hash', None),
            "video_id": getattr(ad_data, 'video_id', None),
        }
        
        return validation_result
    
    async def create_campaign(self, campaign_data: CampaignCreate, owner_id: int) -> Campaign:
        """Create a Facebook Ads campaign."""
        campaign = Campaign(
            platform="Facebook",
            name=campaign_data.name,
            external_id=campaign_data.external_id,
            description=campaign_data.description,
            budget=campaign_data.budget,
            daily_budget=campaign_data.daily_budget,
            start_date=campaign_data.start_date,
            end_date=campaign_data.end_date,
            is_active=campaign_data.is_active,
            owner_id=owner_id,
        )
        
        self.db.add(campaign)
        await self.db.commit()
        await self.db.refresh(campaign)
        return campaign
    
    async def create_ad(self, ad_data: AdCreate) -> Ad:
        """Create a Facebook Ads ad."""
        ad = Ad(
            title=ad_data.title,
            description=ad_data.description,
            content=ad_data.content,
            ad_type=ad_data.ad_type,
            target_audience=ad_data.target_audience,
            demographics=ad_data.demographics,
            interests=ad_data.interests,
            bid_amount=ad_data.bid_amount,
            bid_type=ad_data.bid_type,
            campaign_id=ad_data.campaign_id,
            media_urls=ad_data.media_urls,
            landing_page_url=ad_data.landing_page_url,
        )
        
        self.db.add(ad)
        await self.db.commit()
        await self.db.refresh(ad)
        return ad
    
    async def get_platform_metrics(self, campaign_id: int) -> Dict[str, Any]:
        """Get Facebook Ads specific metrics."""
        return {
            "platform": "Facebook",
            "metrics": {
                "relevance_score": 8.2,
                "frequency": 2.1,
                "reach": 15000,
                "social_impressions": 1200,
                "video_views": 850,
                "video_view_rate": 0.12,
                "engagement_rate": 0.045,
                "cost_per_engagement": 2.15,
            },
            "recommendations": [
                "Improve relevance score by refining targeting",
                "Reduce frequency to avoid ad fatigue",
                "Test different creative formats"
            ]
        }
    
    async def sync_external_data(self, campaign_id: int) -> Dict[str, Any]:
        """Sync with Facebook Ads API."""
        # Simulate Facebook Ads API sync
        return {
            "platform": "Facebook",
            "sync_status": "success",
            "last_sync": datetime.now(timezone.utc).isoformat(),
            "data_synced": {
                "campaigns": 1,
                "ad_sets": 3,
                "ads": 8,
                "insights": 200
            }
        }


class LinkedInAdsService(PlatformService):
    """LinkedIn Ads platform service."""
    
    def get_platform_name(self) -> str:
        return "LinkedIn"
    
    async def validate_campaign_data(self, campaign_data: CampaignCreate) -> Dict[str, Any]:
        """Validate LinkedIn Ads campaign data."""
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "platform_specific": {}
        }
        
        # LinkedIn Ads specific validations
        if campaign_data.budget and campaign_data.budget < 1000:  # $10 minimum
            validation_result["errors"].append("LinkedIn Ads minimum budget is $10.00")
            validation_result["valid"] = False
        
        # LinkedIn Ads campaign formats
        if hasattr(campaign_data, 'campaign_format'):
            valid_formats = ["single_image", "carousel", "video", "text", "follower", "spotlight"]
            if campaign_data.campaign_format not in valid_formats:
                validation_result["errors"].append(f"Invalid LinkedIn Ads format. Must be one of: {valid_formats}")
                validation_result["valid"] = False
        
        validation_result["platform_specific"] = {
            "linkedin_ad_account_id": getattr(campaign_data, 'linkedin_ad_account_id', None),
            "campaign_format": getattr(campaign_data, 'campaign_format', 'single_image'),
            "campaign_group_id": getattr(campaign_data, 'campaign_group_id', None),
            "unit_cost": getattr(campaign_data, 'unit_cost', None),
        }
        
        return validation_result
    
    async def validate_ad_data(self, ad_data: AdCreate) -> Dict[str, Any]:
        """Validate LinkedIn Ads ad data."""
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "platform_specific": {}
        }
        
        # LinkedIn Ads specific validations
        valid_ad_types = ["single_image", "carousel", "video", "text", "follower", "spotlight", "message"]
        if ad_data.ad_type not in valid_ad_types:
            validation_result["errors"].append(f"Invalid LinkedIn Ads ad type. Must be one of: {valid_ad_types}")
            validation_result["valid"] = False
        
        # LinkedIn Ads text limits
        if ad_data.title and len(ad_data.title) > 150:
            validation_result["warnings"].append("LinkedIn Ads headline should be 150 characters or less")
        
        if ad_data.description and len(ad_data.description) > 70:
            validation_result["warnings"].append("LinkedIn Ads description should be 70 characters or less")
        
        # LinkedIn Ads bidding
        valid_bid_types = ["cpc", "cpm", "cpa", "auto_bid", "manual_bid"]
        if ad_data.bid_type and ad_data.bid_type not in valid_bid_types:
            validation_result["errors"].append(f"Invalid LinkedIn Ads bid type. Must be one of: {valid_bid_types}")
            validation_result["valid"] = False
        
        validation_result["platform_specific"] = {
            "creative_id": getattr(ad_data, 'creative_id', None),
            "sponsored_content": getattr(ad_data, 'sponsored_content', None),
            "call_to_action": getattr(ad_data, 'call_to_action', 'learn_more'),
            "company_page_id": getattr(ad_data, 'company_page_id', None),
            "text": getattr(ad_data, 'text', None),
        }
        
        return validation_result
    
    async def create_campaign(self, campaign_data: CampaignCreate, owner_id: int) -> Campaign:
        """Create a LinkedIn Ads campaign."""
        campaign = Campaign(
            platform="LinkedIn",
            name=campaign_data.name,
            external_id=campaign_data.external_id,
            description=campaign_data.description,
            budget=campaign_data.budget,
            daily_budget=campaign_data.daily_budget,
            start_date=campaign_data.start_date,
            end_date=campaign_data.end_date,
            is_active=campaign_data.is_active,
            owner_id=owner_id,
        )
        
        self.db.add(campaign)
        await self.db.commit()
        await self.db.refresh(campaign)
        return campaign
    
    async def create_ad(self, ad_data: AdCreate) -> Ad:
        """Create a LinkedIn Ads ad."""
        ad = Ad(
            title=ad_data.title,
            description=ad_data.description,
            content=ad_data.content,
            ad_type=ad_data.ad_type,
            target_audience=ad_data.target_audience,
            demographics=ad_data.demographics,
            interests=ad_data.interests,
            bid_amount=ad_data.bid_amount,
            bid_type=ad_data.bid_type,
            campaign_id=ad_data.campaign_id,
            media_urls=ad_data.media_urls,
            landing_page_url=ad_data.landing_page_url,
        )
        
        self.db.add(ad)
        await self.db.commit()
        await self.db.refresh(ad)
        return ad
    
    async def get_platform_metrics(self, campaign_id: int) -> Dict[str, Any]:
        """Get LinkedIn Ads specific metrics."""
        return {
            "platform": "LinkedIn",
            "metrics": {
                "click_through_rate": 0.85,
                "cost_per_click": 5.25,
                "cost_per_impression": 0.12,
                "cost_per_send": 0.45,
                "cost_per_lead": 45.00,
                "cost_per_member": 0.08,
                "engagement_rate": 0.035,
                "video_completion_rate": 0.65,
            },
            "recommendations": [
                "Optimize for professional targeting",
                "Use LinkedIn-specific content formats",
                "Focus on B2B messaging and value propositions"
            ]
        }
    
    async def sync_external_data(self, campaign_id: int) -> Dict[str, Any]:
        """Sync with LinkedIn Ads API."""
        # Simulate LinkedIn Ads API sync
        return {
            "platform": "LinkedIn",
            "sync_status": "success",
            "last_sync": datetime.now(timezone.utc).isoformat(),
            "data_synced": {
                "campaigns": 1,
                "creatives": 4,
                "targeting_criteria": 15,
                "performance_data": 120
            }
        }


class PlatformServiceFactory:
    """Factory for creating platform-specific services."""
    
    _services = {
        "Google": GoogleAdsService,
        "Facebook": FacebookAdsService,
        "LinkedIn": LinkedInAdsService,
    }
    
    @classmethod
    def create_service(cls, platform: str, db: AsyncSession) -> PlatformService:
        """Create a platform-specific service."""
        platform = platform.capitalize()
        if platform not in cls._services:
            raise ValueError(f"Unsupported platform: {platform}")
        
        return cls._services[platform](db)
    
    @classmethod
    def get_supported_platforms(cls) -> List[str]:
        """Get list of supported platforms."""
        return list(cls._services.keys())
    
    @classmethod
    def is_platform_supported(cls, platform: str) -> bool:
        """Check if platform is supported."""
        return platform.capitalize() in cls._services
