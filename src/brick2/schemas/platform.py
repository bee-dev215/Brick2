"""Platform-specific Pydantic schemas for different advertising platforms."""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from datetime import datetime

from ..schemas.campaign import CampaignCreate, CampaignUpdate
from ..schemas.ad import AdCreate, AdUpdate


class GoogleAdsCampaignCreate(CampaignCreate):
    """Google Ads specific campaign creation schema."""
    
    # Google Ads specific fields
    google_ads_account_id: Optional[str] = Field(None, description="Google Ads account ID")
    campaign_type: str = Field("search", description="Google Ads campaign type")
    bidding_strategy: str = Field("manual_cpc", description="Google Ads bidding strategy")
    ad_schedule: Optional[Dict[str, Any]] = Field(None, description="Ad schedule configuration")
    location_targeting: Optional[Dict[str, Any]] = Field(None, description="Location targeting settings")
    language_targeting: Optional[List[str]] = Field(None, description="Language targeting")
    device_targeting: Optional[Dict[str, Any]] = Field(None, description="Device targeting settings")
    conversion_tracking: Optional[Dict[str, Any]] = Field(None, description="Conversion tracking setup")


class GoogleAdsCampaignUpdate(CampaignUpdate):
    """Google Ads specific campaign update schema."""
    
    campaign_type: Optional[str] = None
    bidding_strategy: Optional[str] = None
    ad_schedule: Optional[Dict[str, Any]] = None
    location_targeting: Optional[Dict[str, Any]] = None
    language_targeting: Optional[List[str]] = None
    device_targeting: Optional[Dict[str, Any]] = None


class GoogleAdsAdCreate(AdCreate):
    """Google Ads specific ad creation schema."""
    
    # Google Ads specific fields
    ad_group_id: Optional[str] = Field(None, description="Google Ads ad group ID")
    final_urls: Optional[List[str]] = Field(None, description="Final URLs for the ad")
    headlines: Optional[List[str]] = Field(None, description="Ad headlines")
    descriptions: Optional[List[str]] = Field(None, description="Ad descriptions")
    keywords: Optional[List[str]] = Field(None, description="Keywords for search ads")
    negative_keywords: Optional[List[str]] = Field(None, description="Negative keywords")
    extensions: Optional[Dict[str, Any]] = Field(None, description="Ad extensions")
    quality_score: Optional[float] = Field(None, description="Ad quality score")


class GoogleAdsAdUpdate(AdUpdate):
    """Google Ads specific ad update schema."""
    
    final_urls: Optional[List[str]] = None
    headlines: Optional[List[str]] = None
    descriptions: Optional[List[str]] = None
    keywords: Optional[List[str]] = None
    negative_keywords: Optional[List[str]] = None
    extensions: Optional[Dict[str, Any]] = None


class FacebookAdsCampaignCreate(CampaignCreate):
    """Facebook Ads specific campaign creation schema."""
    
    # Facebook Ads specific fields
    facebook_ad_account_id: Optional[str] = Field(None, description="Facebook Ad Account ID")
    campaign_objective: str = Field("traffic", description="Facebook Ads campaign objective")
    buying_type: str = Field("auction", description="Facebook Ads buying type")
    special_ad_categories: Optional[List[str]] = Field(None, description="Special ad categories")
    optimization_goal: Optional[str] = Field(None, description="Optimization goal")
    bid_strategy: Optional[str] = Field(None, description="Bid strategy")
    attribution_window: Optional[Dict[str, Any]] = Field(None, description="Attribution window settings")
    pixel_id: Optional[str] = Field(None, description="Facebook Pixel ID")


class FacebookAdsCampaignUpdate(CampaignUpdate):
    """Facebook Ads specific campaign update schema."""
    
    campaign_objective: Optional[str] = None
    buying_type: Optional[str] = None
    special_ad_categories: Optional[List[str]] = None
    optimization_goal: Optional[str] = None
    bid_strategy: Optional[str] = None
    attribution_window: Optional[Dict[str, Any]] = None


class FacebookAdsAdCreate(AdCreate):
    """Facebook Ads specific ad creation schema."""
    
    # Facebook Ads specific fields
    ad_set_id: Optional[str] = Field(None, description="Facebook Ads ad set ID")
    creative_id: Optional[str] = Field(None, description="Facebook Ads creative ID")
    call_to_action: str = Field("learn_more", description="Call to action button")
    image_hash: Optional[str] = Field(None, description="Image hash for the ad")
    video_id: Optional[str] = Field(None, description="Video ID for video ads")
    link_url: Optional[str] = Field(None, description="Link URL for the ad")
    name: Optional[str] = Field(None, description="Ad name")
    status: Optional[str] = Field("active", description="Ad status")
    tracking_specs: Optional[Dict[str, Any]] = Field(None, description="Tracking specifications")


class FacebookAdsAdUpdate(AdUpdate):
    """Facebook Ads specific ad update schema."""
    
    call_to_action: Optional[str] = None
    image_hash: Optional[str] = None
    video_id: Optional[str] = None
    link_url: Optional[str] = None
    name: Optional[str] = None
    status: Optional[str] = None
    tracking_specs: Optional[Dict[str, Any]] = None


class LinkedInAdsCampaignCreate(CampaignCreate):
    """LinkedIn Ads specific campaign creation schema."""
    
    # LinkedIn Ads specific fields
    linkedin_ad_account_id: Optional[str] = Field(None, description="LinkedIn Ad Account ID")
    campaign_format: str = Field("single_image", description="LinkedIn Ads campaign format")
    campaign_group_id: Optional[str] = Field(None, description="LinkedIn Ads campaign group ID")
    unit_cost: Optional[Dict[str, Any]] = Field(None, description="Unit cost configuration")
    targeting_criteria: Optional[Dict[str, Any]] = Field(None, description="Targeting criteria")
    creative_selection: Optional[str] = Field(None, description="Creative selection method")
    optimization_goal: Optional[str] = Field(None, description="Optimization goal")
    conversion_tracking: Optional[Dict[str, Any]] = Field(None, description="Conversion tracking setup")


class LinkedInAdsCampaignUpdate(CampaignUpdate):
    """LinkedIn Ads specific campaign update schema."""
    
    campaign_format: Optional[str] = None
    campaign_group_id: Optional[str] = None
    unit_cost: Optional[Dict[str, Any]] = None
    targeting_criteria: Optional[Dict[str, Any]] = None
    creative_selection: Optional[str] = None
    optimization_goal: Optional[str] = None


class LinkedInAdsAdCreate(AdCreate):
    """LinkedIn Ads specific ad creation schema."""
    
    # LinkedIn Ads specific fields
    creative_id: Optional[str] = Field(None, description="LinkedIn Ads creative ID")
    sponsored_content: Optional[Dict[str, Any]] = Field(None, description="Sponsored content configuration")
    call_to_action: str = Field("learn_more", description="Call to action button")
    company_page_id: Optional[str] = Field(None, description="LinkedIn company page ID")
    text: Optional[str] = Field(None, description="Ad text content")
    headline: Optional[str] = Field(None, description="Ad headline")
    landing_page_url: Optional[str] = Field(None, description="Landing page URL")
    image_creative: Optional[Dict[str, Any]] = Field(None, description="Image creative configuration")
    video_creative: Optional[Dict[str, Any]] = Field(None, description="Video creative configuration")


class LinkedInAdsAdUpdate(AdUpdate):
    """LinkedIn Ads specific ad update schema."""
    
    sponsored_content: Optional[Dict[str, Any]] = None
    call_to_action: Optional[str] = None
    company_page_id: Optional[str] = None
    text: Optional[str] = None
    headline: Optional[str] = None
    landing_page_url: Optional[str] = None
    image_creative: Optional[Dict[str, Any]] = None
    video_creative: Optional[Dict[str, Any]] = None


class PlatformValidationResult(BaseModel):
    """Platform validation result schema."""
    
    valid: bool
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    platform_specific: Dict[str, Any] = Field(default_factory=dict)


class PlatformMetrics(BaseModel):
    """Platform-specific metrics schema."""
    
    platform: str
    metrics: Dict[str, Any]
    recommendations: List[str] = Field(default_factory=list)
    last_updated: Optional[datetime] = None


class PlatformSyncResult(BaseModel):
    """Platform sync result schema."""
    
    platform: str
    sync_status: str
    last_sync: str
    data_synced: Dict[str, int]
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)


# Platform-specific targeting schemas
class GoogleAdsTargeting(BaseModel):
    """Google Ads targeting configuration."""
    
    locations: Optional[List[str]] = None
    languages: Optional[List[str]] = None
    devices: Optional[List[str]] = None
    demographics: Optional[Dict[str, Any]] = None
    interests: Optional[List[str]] = None
    keywords: Optional[List[str]] = None
    negative_keywords: Optional[List[str]] = None


class FacebookAdsTargeting(BaseModel):
    """Facebook Ads targeting configuration."""
    
    age_min: Optional[int] = Field(None, ge=13, le=65)
    age_max: Optional[int] = Field(None, ge=13, le=65)
    genders: Optional[List[int]] = None  # 1=male, 2=female
    geo_locations: Optional[Dict[str, Any]] = None
    interests: Optional[List[Dict[str, Any]]] = None
    behaviors: Optional[List[Dict[str, Any]]] = None
    demographics: Optional[List[Dict[str, Any]]] = None
    custom_audiences: Optional[List[str]] = None
    lookalike_audiences: Optional[List[str]] = None


class LinkedInAdsTargeting(BaseModel):
    """LinkedIn Ads targeting configuration."""
    
    locations: Optional[List[Dict[str, Any]]] = None
    job_titles: Optional[List[Dict[str, Any]]] = None
    job_functions: Optional[List[Dict[str, Any]]] = None
    seniorities: Optional[List[Dict[str, Any]]] = None
    company_names: Optional[List[Dict[str, Any]]] = None
    company_industries: Optional[List[Dict[str, Any]]] = None
    company_sizes: Optional[List[Dict[str, Any]]] = None
    skills: Optional[List[Dict[str, Any]]] = None
    schools: Optional[List[Dict[str, Any]]] = None
    degrees: Optional[List[Dict[str, Any]]] = None
    member_groups: Optional[List[Dict[str, Any]]] = None
    years_of_experience: Optional[List[Dict[str, Any]]] = None
