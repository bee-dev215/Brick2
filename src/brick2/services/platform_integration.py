"""Platform integration service for external API connections."""

import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
import httpx

from ..models.campaign import Campaign
from ..models.ad import Ad
from ..models.performance import Performance
from .platform import PlatformServiceFactory


class PlatformIntegrationService:
    """Service for integrating with external advertising platform APIs."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.api_clients = {
            "Google": GoogleAdsAPIClient(),
            "Facebook": FacebookAdsAPIClient(),
            "LinkedIn": LinkedInAdsAPIClient(),
        }
    
    async def sync_all_platforms(self, user_id: Optional[int] = None) -> Dict[str, Any]:
        """Sync data from all supported platforms."""
        sync_results = {}
        
        for platform in PlatformServiceFactory.get_supported_platforms():
            try:
                result = await self.sync_platform(platform, user_id)
                sync_results[platform] = result
            except Exception as e:
                sync_results[platform] = {
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
        
        return {
            "sync_results": sync_results,
            "total_platforms": len(sync_results),
            "successful_syncs": len([r for r in sync_results.values() if r.get("status") == "success"]),
            "failed_syncs": len([r for r in sync_results.values() if r.get("status") == "error"]),
            "sync_timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    async def sync_platform(self, platform: str, user_id: Optional[int] = None) -> Dict[str, Any]:
        """Sync data from a specific platform."""
        if platform not in self.api_clients:
            raise ValueError(f"Unsupported platform: {platform}")
        
        client = self.api_clients[platform]
        
        # Get campaigns for the platform
        from ..campaign_service import CampaignService
        campaign_service = CampaignService(self.db)
        
        if user_id:
            campaigns = await campaign_service.get_by_owner(user_id)
            platform_campaigns = [c for c in campaigns if c.platform.lower() == platform.lower()]
        else:
            all_campaigns = await campaign_service.get_all()
            platform_campaigns = [c for c in all_campaigns if c.platform.lower() == platform.lower()]
        
        sync_result = {
            "platform": platform,
            "status": "success",
            "campaigns_synced": 0,
            "ads_synced": 0,
            "performance_records_synced": 0,
            "errors": [],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        for campaign in platform_campaigns:
            try:
                # Sync campaign data
                campaign_data = await client.get_campaign_data(campaign.external_id)
                if campaign_data:
                    sync_result["campaigns_synced"] += 1
                
                # Sync ads data
                ads_data = await client.get_ads_data(campaign.external_id)
                if ads_data:
                    sync_result["ads_synced"] += len(ads_data)
                
                # Sync performance data
                performance_data = await client.get_performance_data(campaign.external_id)
                if performance_data:
                    sync_result["performance_records_synced"] += len(performance_data)
                    
                    # Store performance data in database
                    await self._store_performance_data(campaign.id, performance_data)
                
            except Exception as e:
                sync_result["errors"].append(f"Campaign {campaign.id}: {str(e)}")
        
        return sync_result
    
    async def _store_performance_data(self, campaign_id: int, performance_data: List[Dict[str, Any]]):
        """Store performance data in the database."""
        from ..performance_service import PerformanceService
        performance_service = PerformanceService(self.db)
        
        for data in performance_data:
            performance_create = {
                "campaign_id": campaign_id,
                "metric_type": data.get("metric_type", "unknown"),
                "value": data.get("value", 0),
                "cost": data.get("cost", 0.0),
                "date": datetime.fromisoformat(data.get("date", datetime.now(timezone.utc).isoformat())),
                "metadata": data.get("metadata", {})
            }
            
            # Create performance record
            from ..schemas.performance import PerformanceCreate
            performance = PerformanceCreate(**performance_create)
            await performance_service.create(performance)


class GoogleAdsAPIClient:
    """Google Ads API client."""
    
    def __init__(self):
        self.base_url = "https://googleads.googleapis.com/v14"
        self.access_token = None  # Would be set from OAuth flow
    
    async def get_campaign_data(self, campaign_id: str) -> Optional[Dict[str, Any]]:
        """Get campaign data from Google Ads API."""
        # Simulate Google Ads API call
        return {
            "id": campaign_id,
            "name": "Google Ads Campaign",
            "status": "active",
            "budget": 100000,
            "daily_budget": 10000,
            "campaign_type": "search",
            "bidding_strategy": "manual_cpc",
            "quality_score": 8.5,
            "last_updated": datetime.now(timezone.utc).isoformat()
        }
    
    async def get_ads_data(self, campaign_id: str) -> List[Dict[str, Any]]:
        """Get ads data from Google Ads API."""
        # Simulate Google Ads API call
        return [
            {
                "id": f"ad_{i}",
                "campaign_id": campaign_id,
                "title": f"Google Ad {i}",
                "description": f"Google Ad description {i}",
                "ad_type": "search",
                "status": "active",
                "quality_score": 8.0 + i * 0.1,
                "headlines": [f"Headline {i}-1", f"Headline {i}-2"],
                "descriptions": [f"Description {i}-1", f"Description {i}-2"],
                "final_urls": [f"https://example.com/ad{i}"],
                "keywords": [f"keyword{i}-1", f"keyword{i}-2"]
            }
            for i in range(1, 4)
        ]
    
    async def get_performance_data(self, campaign_id: str) -> List[Dict[str, Any]]:
        """Get performance data from Google Ads API."""
        # Simulate Google Ads API call
        return [
            {
                "campaign_id": campaign_id,
                "metric_type": "impressions",
                "value": 10000,
                "cost": 500.0,
                "date": datetime.now(timezone.utc).isoformat(),
                "metadata": {
                    "quality_score": 8.5,
                    "search_impression_share": 0.75,
                    "click_share": 0.68
                }
            },
            {
                "campaign_id": campaign_id,
                "metric_type": "clicks",
                "value": 500,
                "cost": 500.0,
                "date": datetime.now(timezone.utc).isoformat(),
                "metadata": {
                    "ctr": 0.05,
                    "average_cpc": 1.0,
                    "conversion_rate": 0.025
                }
            },
            {
                "campaign_id": campaign_id,
                "metric_type": "conversions",
                "value": 25,
                "cost": 500.0,
                "date": datetime.now(timezone.utc).isoformat(),
                "metadata": {
                    "cost_per_conversion": 20.0,
                    "conversion_value": 1000.0,
                    "roas": 2.0
                }
            }
        ]


class FacebookAdsAPIClient:
    """Facebook Ads API client."""
    
    def __init__(self):
        self.base_url = "https://graph.facebook.com/v18.0"
        self.access_token = None  # Would be set from OAuth flow
    
    async def get_campaign_data(self, campaign_id: str) -> Optional[Dict[str, Any]]:
        """Get campaign data from Facebook Ads API."""
        # Simulate Facebook Ads API call
        return {
            "id": campaign_id,
            "name": "Facebook Ads Campaign",
            "status": "active",
            "budget": 150000,
            "daily_budget": 15000,
            "campaign_objective": "traffic",
            "buying_type": "auction",
            "relevance_score": 8.2,
            "last_updated": datetime.now(timezone.utc).isoformat()
        }
    
    async def get_ads_data(self, campaign_id: str) -> List[Dict[str, Any]]:
        """Get ads data from Facebook Ads API."""
        # Simulate Facebook Ads API call
        return [
            {
                "id": f"fb_ad_{i}",
                "campaign_id": campaign_id,
                "name": f"Facebook Ad {i}",
                "ad_type": "image",
                "status": "active",
                "relevance_score": 8.0 + i * 0.1,
                "call_to_action": "learn_more",
                "image_hash": f"image_hash_{i}",
                "link_url": f"https://example.com/fb-ad{i}",
                "primary_text": f"Facebook Ad primary text {i}",
                "headline": f"Facebook Ad headline {i}",
                "description": f"Facebook Ad description {i}"
            }
            for i in range(1, 4)
        ]
    
    async def get_performance_data(self, campaign_id: str) -> List[Dict[str, Any]]:
        """Get performance data from Facebook Ads API."""
        # Simulate Facebook Ads API call
        return [
            {
                "campaign_id": campaign_id,
                "metric_type": "impressions",
                "value": 15000,
                "cost": 750.0,
                "date": datetime.now(timezone.utc).isoformat(),
                "metadata": {
                    "frequency": 2.1,
                    "reach": 15000,
                    "social_impressions": 1200
                }
            },
            {
                "campaign_id": campaign_id,
                "metric_type": "clicks",
                "value": 750,
                "cost": 750.0,
                "date": datetime.now(timezone.utc).isoformat(),
                "metadata": {
                    "ctr": 0.05,
                    "cpc": 1.0,
                    "engagement_rate": 0.045
                }
            },
            {
                "campaign_id": campaign_id,
                "metric_type": "conversions",
                "value": 30,
                "cost": 750.0,
                "date": datetime.now(timezone.utc).isoformat(),
                "metadata": {
                    "cost_per_conversion": 25.0,
                    "conversion_rate": 0.04,
                    "video_views": 850
                }
            }
        ]


class LinkedInAdsAPIClient:
    """LinkedIn Ads API client."""
    
    def __init__(self):
        self.base_url = "https://api.linkedin.com/v2"
        self.access_token = None  # Would be set from OAuth flow
    
    async def get_campaign_data(self, campaign_id: str) -> Optional[Dict[str, Any]]:
        """Get campaign data from LinkedIn Ads API."""
        # Simulate LinkedIn Ads API call
        return {
            "id": campaign_id,
            "name": "LinkedIn Ads Campaign",
            "status": "active",
            "budget": 200000,
            "daily_budget": 20000,
            "campaign_format": "single_image",
            "unit_cost": {"amount": 500, "currency": "USD"},
            "click_through_rate": 0.85,
            "last_updated": datetime.now(timezone.utc).isoformat()
        }
    
    async def get_ads_data(self, campaign_id: str) -> List[Dict[str, Any]]:
        """Get ads data from LinkedIn Ads API."""
        # Simulate LinkedIn Ads API call
        return [
            {
                "id": f"li_ad_{i}",
                "campaign_id": campaign_id,
                "name": f"LinkedIn Ad {i}",
                "ad_type": "single_image",
                "status": "active",
                "click_through_rate": 0.8 + i * 0.05,
                "call_to_action": "learn_more",
                "company_page_id": f"company_page_{i}",
                "text": f"LinkedIn Ad text {i}",
                "headline": f"LinkedIn Ad headline {i}",
                "landing_page_url": f"https://example.com/li-ad{i}",
                "image_creative": {
                    "image_url": f"https://example.com/li-ad{i}-image.jpg",
                    "alt_text": f"LinkedIn Ad {i} image"
                }
            }
            for i in range(1, 4)
        ]
    
    async def get_performance_data(self, campaign_id: str) -> List[Dict[str, Any]]:
        """Get performance data from LinkedIn Ads API."""
        # Simulate LinkedIn Ads API call
        return [
            {
                "campaign_id": campaign_id,
                "metric_type": "impressions",
                "value": 20000,
                "cost": 1000.0,
                "date": datetime.now(timezone.utc).isoformat(),
                "metadata": {
                    "cost_per_impression": 0.05,
                    "cost_per_member": 0.08,
                    "video_completion_rate": 0.65
                }
            },
            {
                "campaign_id": campaign_id,
                "metric_type": "clicks",
                "value": 1000,
                "cost": 1000.0,
                "date": datetime.now(timezone.utc).isoformat(),
                "metadata": {
                    "ctr": 0.05,
                    "cost_per_click": 1.0,
                    "engagement_rate": 0.035
                }
            },
            {
                "campaign_id": campaign_id,
                "metric_type": "conversions",
                "value": 50,
                "cost": 1000.0,
                "date": datetime.now(timezone.utc).isoformat(),
                "metadata": {
                    "cost_per_conversion": 20.0,
                    "cost_per_lead": 45.0,
                    "cost_per_send": 0.45
                }
            }
        ]


class PlatformAnalyticsService:
    """Service for platform-specific analytics and reporting."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_cross_platform_analytics(self, user_id: Optional[int] = None) -> Dict[str, Any]:
        """Get analytics across all platforms."""
        from ..campaign_service import CampaignService
        from ..performance_service import PerformanceService
        
        campaign_service = CampaignService(self.db)
        performance_service = PerformanceService(self.db)
        
        # Get all campaigns
        if user_id:
            campaigns = await campaign_service.get_by_owner(user_id)
        else:
            campaigns = await campaign_service.get_all()
        
        platform_analytics = {}
        
        for platform in PlatformServiceFactory.get_supported_platforms():
            platform_campaigns = [c for c in campaigns if c.platform.lower() == platform.lower()]
            
            if not platform_campaigns:
                continue
            
            total_impressions = 0
            total_clicks = 0
            total_conversions = 0
            total_cost = 0.0
            total_budget = 0
            
            for campaign in platform_campaigns:
                # Get performance summary
                summary = await performance_service.get_campaign_summary(campaign.id)
                total_impressions += summary.get("total_impressions", 0)
                total_clicks += summary.get("total_clicks", 0)
                total_conversions += summary.get("total_conversions", 0)
                total_cost += summary.get("total_cost", 0.0)
                total_budget += campaign.budget or 0
            
            # Calculate platform-specific metrics
            ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
            cpc = (total_cost / total_clicks) if total_clicks > 0 else 0
            cpa = (total_cost / total_conversions) if total_conversions > 0 else 0
            roas = (total_budget / total_cost) if total_cost > 0 else 0
            
            platform_analytics[platform] = {
                "campaigns_count": len(platform_campaigns),
                "total_impressions": total_impressions,
                "total_clicks": total_clicks,
                "total_conversions": total_conversions,
                "total_cost": total_cost,
                "total_budget": total_budget,
                "ctr": ctr,
                "cpc": cpc,
                "cpa": cpa,
                "roas": roas,
                "budget_utilization": (total_cost / total_budget * 100) if total_budget > 0 else 0
            }
        
        # Calculate cross-platform insights
        total_platforms = len(platform_analytics)
        best_performing_platform = max(platform_analytics.items(), key=lambda x: x[1]["ctr"]) if platform_analytics else None
        most_cost_effective_platform = min(platform_analytics.items(), key=lambda x: x[1]["cpa"]) if platform_analytics else None
        
        return {
            "platform_analytics": platform_analytics,
            "cross_platform_insights": {
                "total_platforms": total_platforms,
                "best_performing_platform": best_performing_platform[0] if best_performing_platform else None,
                "best_performing_ctr": best_performing_platform[1]["ctr"] if best_performing_platform else 0,
                "most_cost_effective_platform": most_cost_effective_platform[0] if most_cost_effective_platform else None,
                "most_cost_effective_cpa": most_cost_effective_platform[1]["cpa"] if most_cost_effective_platform else 0,
            },
            "generated_at": datetime.now(timezone.utc).isoformat()
        }
    
    async def get_platform_recommendations(self, platform: str, campaign_id: int) -> Dict[str, Any]:
        """Get platform-specific recommendations."""
        if not PlatformServiceFactory.is_platform_supported(platform):
            raise ValueError(f"Unsupported platform: {platform}")
        
        service = PlatformServiceFactory.create_service(platform, self.db)
        metrics = await service.get_platform_metrics(campaign_id)
        
        # Generate recommendations based on platform-specific metrics
        recommendations = []
        
        if platform == "Google":
            if metrics["metrics"].get("quality_score", 0) < 7:
                recommendations.append("Improve Quality Score by optimizing ad relevance and landing page experience")
            if metrics["metrics"].get("search_impression_share", 0) < 0.8:
                recommendations.append("Increase bid to improve impression share and visibility")
            if metrics["metrics"].get("click_share", 0) < 0.7:
                recommendations.append("Optimize ad copy and keywords to improve click share")
        
        elif platform == "Facebook":
            if metrics["metrics"].get("relevance_score", 0) < 7:
                recommendations.append("Improve relevance score by refining targeting and ad creative")
            if metrics["metrics"].get("frequency", 0) > 3:
                recommendations.append("Reduce frequency to avoid ad fatigue and improve performance")
            if metrics["metrics"].get("engagement_rate", 0) < 0.03:
                recommendations.append("Test different creative formats to improve engagement")
        
        elif platform == "LinkedIn":
            if metrics["metrics"].get("click_through_rate", 0) < 0.5:
                recommendations.append("Optimize for professional targeting and B2B messaging")
            if metrics["metrics"].get("cost_per_click", 0) > 5:
                recommendations.append("Refine targeting to reduce cost per click")
            if metrics["metrics"].get("engagement_rate", 0) < 0.02:
                recommendations.append("Use LinkedIn-specific content formats and professional messaging")
        
        return {
            "platform": platform,
            "campaign_id": campaign_id,
            "recommendations": recommendations,
            "metrics_analyzed": list(metrics["metrics"].keys()),
            "generated_at": datetime.now(timezone.utc).isoformat()
        }
