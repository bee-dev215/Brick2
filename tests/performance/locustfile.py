"""
Load testing with Locust for BRICK 2 API endpoints.
"""

from locust import HttpUser, task, between
import json
import random


class BRICK2User(HttpUser):
    """Simulate user interactions with BRICK 2 API."""
    
    wait_time = between(1, 3)
    
    def on_start(self):
        """Set up user session."""
        self.client.verify = False
        self.user_id = None
        self.campaign_id = None
        
        # Create a test user
        user_data = {
            "username": f"testuser_{random.randint(1000, 9999)}",
            "email": f"test_{random.randint(1000, 9999)}@example.com",
            "password": "testpassword123",
            "full_name": "Test User"
        }
        
        response = self.client.post("/api/v1/users/", json=user_data)
        if response.status_code == 201:
            self.user_id = response.json().get("id")
    
    @task(3)
    def health_check(self):
        """Check application health."""
        self.client.get("/health")
    
    @task(2)
    def get_root(self):
        """Get root endpoint."""
        self.client.get("/")
    
    @task(5)
    def create_campaign(self):
        """Create a new campaign."""
        if not self.user_id:
            return
            
        campaign_data = {
            "platform": random.choice(["Google", "Facebook", "LinkedIn"]),
            "name": f"Test Campaign {random.randint(1000, 9999)}",
            "budget": random.uniform(100, 10000),
            "owner_id": self.user_id
        }
        
        response = self.client.post("/api/v1/campaigns/", json=campaign_data)
        if response.status_code == 201:
            self.campaign_id = response.json().get("id")
    
    @task(4)
    def get_campaigns(self):
        """Get campaigns list."""
        self.client.get("/api/v1/campaigns/")
    
    @task(3)
    def get_campaign_by_id(self):
        """Get specific campaign."""
        if self.campaign_id:
            self.client.get(f"/api/v1/campaigns/{self.campaign_id}")
    
    @task(2)
    def create_ad(self):
        """Create a new ad."""
        if not self.campaign_id:
            return
            
        ad_data = {
            "title": f"Test Ad {random.randint(1000, 9999)}",
            "ad_type": random.choice(["banner", "video", "text"]),
            "campaign_id": self.campaign_id
        }
        
        self.client.post("/api/v1/ads/", json=ad_data)
    
    @task(3)
    def get_ads(self):
        """Get ads list."""
        self.client.get("/api/v1/ads/")
    
    @task(2)
    def create_performance(self):
        """Create performance data."""
        if not self.campaign_id:
            return
            
        performance_data = {
            "campaign_id": self.campaign_id,
            "date": "2024-01-01T00:00:00",
            "metric_type": random.choice(["impressions", "clicks", "conversions"]),
            "value": random.uniform(10, 1000),
            "cost": random.uniform(1, 100)
        }
        
        self.client.post("/api/v1/performance/", json=performance_data)
    
    @task(3)
    def get_performance(self):
        """Get performance data."""
        self.client.get("/api/v1/performance/")
    
    @task(1)
    def create_lead(self):
        """Create a lead."""
        if not self.campaign_id:
            return
            
        lead_data = {
            "campaign_id": self.campaign_id,
            "email": f"lead_{random.randint(1000, 9999)}@example.com",
            "first_name": "John",
            "last_name": "Doe"
        }
        
        self.client.post("/api/v1/leads/", json=lead_data)
    
    @task(2)
    def get_leads(self):
        """Get leads list."""
        self.client.get("/api/v1/leads/")


class APIStressUser(HttpUser):
    """Stress test user for API endpoints."""
    
    wait_time = between(0.1, 0.5)
    weight = 1
    
    @task(10)
    def rapid_health_checks(self):
        """Rapid health check requests."""
        self.client.get("/health")
    
    @task(5)
    def rapid_campaign_requests(self):
        """Rapid campaign requests."""
        self.client.get("/api/v1/campaigns/")
    
    @task(3)
    def rapid_performance_requests(self):
        """Rapid performance requests."""
        self.client.get("/api/v1/performance/")


class DatabaseLoadUser(HttpUser):
    """Database load test user."""
    
    wait_time = between(2, 5)
    weight = 2
    
    def on_start(self):
        """Set up database test data."""
        self.campaign_ids = []
        
        # Get existing campaigns
        response = self.client.get("/api/v1/campaigns/")
        if response.status_code == 200:
            campaigns = response.json()
            self.campaign_ids = [c["id"] for c in campaigns[:10]]
    
    @task(5)
    def complex_queries(self):
        """Execute complex database queries."""
        if self.campaign_ids:
            campaign_id = random.choice(self.campaign_ids)
            
            # Get campaign with related data
            self.client.get(f"/api/v1/campaigns/{campaign_id}")
            
            # Get campaign ads
            self.client.get(f"/api/v1/ads/?campaign_id={campaign_id}")
            
            # Get campaign performance
            self.client.get(f"/api/v1/performance/?campaign_id={campaign_id}")
    
    @task(3)
    def bulk_operations(self):
        """Test bulk operations."""
        # Get all campaigns
        self.client.get("/api/v1/campaigns/?limit=100")
        
        # Get all ads
        self.client.get("/api/v1/ads/?limit=100")
        
        # Get all performance data
        self.client.get("/api/v1/performance/?limit=100")
