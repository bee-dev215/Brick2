"""Platform-specific API endpoints for different advertising platforms."""

from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db
from app.services.platforms import PlatformServiceFactory
from app.schemas.platform_schemas import (
    GoogleAdsCampaignCreate, GoogleAdsCampaignUpdate, GoogleAdsAdCreate, GoogleAdsAdUpdate,
    FacebookAdsCampaignCreate, FacebookAdsCampaignUpdate, FacebookAdsAdCreate, FacebookAdsAdUpdate,
    LinkedInAdsCampaignCreate, LinkedInAdsCampaignUpdate, LinkedInAdsAdCreate, LinkedInAdsAdUpdate,
    PlatformValidationResult, PlatformMetrics, PlatformSyncResult
)

router = APIRouter()


@router.get("/platforms", response_model=List[str])
async def get_supported_platforms():
    """Get list of supported advertising platforms."""
    return PlatformServiceFactory.get_supported_platforms()


@router.get("/platforms/{platform}/validate-campaign", response_model=PlatformValidationResult)
async def validate_platform_campaign(
    platform: str,
    campaign_data: Dict[str, Any],
    db: AsyncSession = Depends(get_db),
):
    """Validate platform-specific campaign data."""
    if not PlatformServiceFactory.is_platform_supported(platform):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported platform: {platform}"
        )
    
    try:
        service = PlatformServiceFactory.create(platform, db)
        validation_result = await service.validate_campaign_data(campaign_data)
        return PlatformValidationResult(**validation_result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Validation failed: {str(e)}"
        )


@router.get("/platforms/{platform}/validate-ad", response_model=PlatformValidationResult)
async def validate_platform_ad(
    platform: str,
    ad_data: Dict[str, Any],
    db: AsyncSession = Depends(get_db),
):
    """Validate platform-specific ad data."""
    if not PlatformServiceFactory.is_platform_supported(platform):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported platform: {platform}"
        )
    
    try:
        service = PlatformServiceFactory.create(platform, db)
        validation_result = await service.validate_ad_data(ad_data)
        return PlatformValidationResult(**validation_result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Validation failed: {str(e)}"
        )


@router.get("/platforms/{platform}/campaigns/{campaign_id}/metrics", response_model=PlatformMetrics)
async def get_platform_metrics(
    platform: str,
    campaign_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get platform-specific metrics for a campaign."""
    if not PlatformServiceFactory.is_platform_supported(platform):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported platform: {platform}"
        )
    
    try:
        service = PlatformServiceFactory.create(platform, db)
        metrics = await service.get_platform_metrics(campaign_id)
        return PlatformMetrics(**metrics)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get metrics: {str(e)}"
        )


@router.post("/platforms/{platform}/campaigns/{campaign_id}/sync", response_model=PlatformSyncResult)
async def sync_platform_data(
    platform: str,
    campaign_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Sync data with external platform API."""
    if not PlatformServiceFactory.is_platform_supported(platform):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported platform: {platform}"
        )
    
    try:
        service = PlatformServiceFactory.create(platform, db)
        sync_result = await service.sync_external_data(campaign_id)
        return PlatformSyncResult(**sync_result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Sync failed: {str(e)}"
        )


# Google Ads specific endpoints
@router.post("/google/campaigns", status_code=status.HTTP_201_CREATED)
async def create_google_campaign(
    campaign_data: GoogleAdsCampaignCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a Google Ads campaign with platform-specific validation."""
    try:
        service = PlatformServiceFactory.create("Google", db)
        
        # Validate campaign data
        validation_result = await service.validate_campaign_data(campaign_data)
        if not validation_result["valid"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"validation_errors": validation_result["errors"]}
            )
        
        # Create campaign
        campaign = await service.create_campaign(campaign_data, campaign_data.owner_id)
        return campaign
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create Google Ads campaign: {str(e)}"
        )


@router.post("/google/ads", status_code=status.HTTP_201_CREATED)
async def create_google_ad(
    ad_data: GoogleAdsAdCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a Google Ads ad with platform-specific validation."""
    try:
        service = PlatformServiceFactory.create("Google", db)
        
        # Validate ad data
        validation_result = await service.validate_ad_data(ad_data)
        if not validation_result["valid"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"validation_errors": validation_result["errors"]}
            )
        
        # Create ad
        ad = await service.create_ad(ad_data)
        return ad
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create Google Ads ad: {str(e)}"
        )


# Facebook Ads specific endpoints
@router.post("/facebook/campaigns", status_code=status.HTTP_201_CREATED)
async def create_facebook_campaign(
    campaign_data: FacebookAdsCampaignCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a Facebook Ads campaign with platform-specific validation."""
    try:
        service = PlatformServiceFactory.create("Facebook", db)
        
        # Validate campaign data
        validation_result = await service.validate_campaign_data(campaign_data)
        if not validation_result["valid"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"validation_errors": validation_result["errors"]}
            )
        
        # Create campaign
        campaign = await service.create_campaign(campaign_data, campaign_data.owner_id)
        return campaign
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create Facebook Ads campaign: {str(e)}"
        )


@router.post("/facebook/ads", status_code=status.HTTP_201_CREATED)
async def create_facebook_ad(
    ad_data: FacebookAdsAdCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a Facebook Ads ad with platform-specific validation."""
    try:
        service = PlatformServiceFactory.create("Facebook", db)
        
        # Validate ad data
        validation_result = await service.validate_ad_data(ad_data)
        if not validation_result["valid"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"validation_errors": validation_result["errors"]}
            )
        
        # Create ad
        ad = await service.create_ad(ad_data)
        return ad
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create Facebook Ads ad: {str(e)}"
        )


# LinkedIn Ads specific endpoints
@router.post("/linkedin/campaigns", status_code=status.HTTP_201_CREATED)
async def create_linkedin_campaign(
    campaign_data: LinkedInAdsCampaignCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a LinkedIn Ads campaign with platform-specific validation."""
    try:
        service = PlatformServiceFactory.create("LinkedIn", db)
        
        # Validate campaign data
        validation_result = await service.validate_campaign_data(campaign_data)
        if not validation_result["valid"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"validation_errors": validation_result["errors"]}
            )
        
        # Create campaign
        campaign = await service.create_campaign(campaign_data, campaign_data.owner_id)
        return campaign
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create LinkedIn Ads campaign: {str(e)}"
        )


@router.post("/linkedin/ads", status_code=status.HTTP_201_CREATED)
async def create_linkedin_ad(
    ad_data: LinkedInAdsAdCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a LinkedIn Ads ad with platform-specific validation."""
    try:
        service = PlatformServiceFactory.create("LinkedIn", db)
        
        # Validate ad data
        validation_result = await service.validate_ad_data(ad_data)
        if not validation_result["valid"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"validation_errors": validation_result["errors"]}
            )
        
        # Create ad
        ad = await service.create_ad(ad_data)
        return ad
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create LinkedIn Ads ad: {str(e)}"
        )


# Platform comparison endpoints
@router.get("/platforms/compare-metrics")
async def compare_platform_metrics(
    campaign_ids: List[int] = Query(..., description="List of campaign IDs to compare"),
    db: AsyncSession = Depends(get_db),
):
    """Compare metrics across different platforms."""
    try:
        comparison_results = {}
        
        for campaign_id in campaign_ids:
            # Get campaign to determine platform
            from app.services.campaign import CampaignService
            campaign = CampaignService(db)
            campaign = await campaign.get_by_id(campaign_id)
            
            if not campaign:
                continue
            
            platform = campaign.platform
            if PlatformServiceFactory.is_platform_supported(platform):
                service = PlatformServiceFactory.create(platform, db)
                metrics = await service.get_platform_metrics(campaign_id)
                comparison_results[platform] = metrics
        
        return {
            "comparison_results": comparison_results,
            "total_platforms": len(comparison_results),
            "campaigns_analyzed": len(campaign_ids)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to compare platform metrics: {str(e)}"
        )


@router.get("/platforms/features")
async def get_platform_features():
    """Get platform-specific features and capabilities."""
    return {
        "Google": {
            "campaign_types": ["search", "display", "video", "shopping", "app", "smart"],
            "ad_formats": ["text", "image", "video", "responsive", "shopping", "app"],
            "bidding_strategies": ["cpc", "cpm", "cpa", "target_cpa", "target_roas", "maximize_clicks", "maximize_conversions"],
            "targeting_options": ["keywords", "demographics", "interests", "locations", "devices", "audiences"],
            "unique_features": ["Quality Score", "Ad Extensions", "Keyword Planner", "Search Terms Report"]
        },
        "Facebook": {
            "campaign_types": ["awareness", "traffic", "engagement", "leads", "app_promotion", "sales", "reach", "store_visits", "video_views", "messages"],
            "ad_formats": ["image", "video", "carousel", "collection", "slideshow", "canvas", "dynamic_product"],
            "bidding_strategies": ["cpc", "cpm", "cpa", "oCPM", "oCPC", "lowest_cost", "cost_cap", "bid_cap"],
            "targeting_options": ["demographics", "interests", "behaviors", "custom_audiences", "lookalike_audiences", "pixel_data"],
            "unique_features": ["Facebook Pixel", "Custom Audiences", "Lookalike Audiences", "Dynamic Product Ads"]
        },
        "LinkedIn": {
            "campaign_types": ["awareness", "traffic", "engagement", "leads", "video_views", "website_conversions"],
            "ad_formats": ["single_image", "carousel", "video", "text", "follower", "spotlight", "message"],
            "bidding_strategies": ["cpc", "cpm", "cpa", "auto_bid", "manual_bid"],
            "targeting_options": ["job_titles", "job_functions", "seniorities", "company_names", "company_industries", "skills", "schools", "degrees"],
            "unique_features": ["Professional Targeting", "Company Page Integration", "Lead Gen Forms", "Message Ads"]
        }
    }
