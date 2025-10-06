"""
Benchmark tests for BRICK 2 performance.
"""

import pytest
import asyncio
import time
from datetime import datetime
from typing import List, Dict, Any

from brick2.core.database import get_async_session
from brick2.services import (
    UserService, CampaignService, AdService, 
    PerformanceService, LeadService
)
from brick2.schemas import (
    UserCreate, CampaignCreate, AdCreate, 
    PerformanceCreate, LeadCreate
)


class TestDatabasePerformance:
    """Test database operation performance."""
    
    @pytest.fixture
    async def db_session(self):
        """Get database session."""
        async for session in get_async_session():
            yield session
            break
    
    @pytest.mark.benchmark
    async def test_user_creation_performance(self, db_session, benchmark):
        """Benchmark user creation performance."""
        user_service = UserService(db_session)
        
        def create_user():
            user_data = UserCreate(
                username=f"benchmark_user_{int(time.time())}",
                email=f"benchmark_{int(time.time())}@example.com",
                password="benchmarkpassword123",
                full_name="Benchmark User"
            )
            return asyncio.run(user_service.create(user_data))
        
        result = benchmark(create_user)
        assert result is not None
    
    @pytest.mark.benchmark
    async def test_campaign_creation_performance(self, db_session, benchmark):
        """Benchmark campaign creation performance."""
        campaign_service = CampaignService(db_session)
        
        # Create a test user first
        user_service = UserService(db_session)
        user_data = UserCreate(
            username=f"benchmark_user_{int(time.time())}",
            email=f"benchmark_{int(time.time())}@example.com",
            password="benchmarkpassword123",
            full_name="Benchmark User"
        )
        user = await user_service.create(user_data)
        
        def create_campaign():
            campaign_data = CampaignCreate(
                platform="Google",
                name=f"Benchmark Campaign {int(time.time())}",
                budget=1000.0,
                owner_id=user.id
            )
            return asyncio.run(campaign_service.create(campaign_data))
        
        result = benchmark(create_campaign)
        assert result is not None
    
    @pytest.mark.benchmark
    async def test_bulk_user_queries(self, db_session, benchmark):
        """Benchmark bulk user queries."""
        user_service = UserService(db_session)
        
        def query_users():
            return asyncio.run(user_service.get_all(limit=100))
        
        result = benchmark(query_users)
        assert isinstance(result, list)
    
    @pytest.mark.benchmark
    async def test_complex_joins_performance(self, db_session, benchmark):
        """Benchmark complex join queries."""
        campaign_service = CampaignService(db_session)
        
        def get_campaigns_with_owner():
            return asyncio.run(campaign_service.get_all(limit=50))
        
        result = benchmark(get_campaigns_with_owner)
        assert isinstance(result, list)


class TestAPIPerformance:
    """Test API endpoint performance."""
    
    @pytest.mark.benchmark
    def test_health_endpoint_performance(self, benchmark):
        """Benchmark health endpoint performance."""
        import requests
        
        def check_health():
            response = requests.get("http://localhost:8000/health")
            return response.status_code == 200
        
        result = benchmark(check_health)
        assert result is True
    
    @pytest.mark.benchmark
    def test_campaigns_endpoint_performance(self, benchmark):
        """Benchmark campaigns endpoint performance."""
        import requests
        
        def get_campaigns():
            response = requests.get("http://localhost:8000/api/v1/campaigns/")
            return response.status_code == 200
        
        result = benchmark(get_campaigns)
        assert result is True


class TestMemoryUsage:
    """Test memory usage patterns."""
    
    @pytest.mark.benchmark
    async def test_memory_usage_user_creation(self, db_session, benchmark):
        """Test memory usage during user creation."""
        user_service = UserService(db_session)
        
        def create_multiple_users():
            async def create_users():
                users = []
                for i in range(100):
                    user_data = UserCreate(
                        username=f"memory_test_user_{i}",
                        email=f"memory_test_{i}@example.com",
                        password="memorytestpassword123",
                        full_name=f"Memory Test User {i}"
                    )
                    user = await user_service.create(user_data)
                    users.append(user)
                return users
            
            return asyncio.run(create_users())
        
        result = benchmark(create_multiple_users)
        assert len(result) == 100
    
    @pytest.mark.benchmark
    async def test_memory_usage_large_queries(self, db_session, benchmark):
        """Test memory usage with large queries."""
        performance_service = PerformanceService(db_session)
        
        def query_large_dataset():
            return asyncio.run(performance_service.get_all(limit=1000))
        
        result = benchmark(query_large_dataset)
        assert isinstance(result, list)


class TestConcurrentOperations:
    """Test concurrent operation performance."""
    
    @pytest.mark.benchmark
    async def test_concurrent_user_creation(self, db_session, benchmark):
        """Test concurrent user creation performance."""
        user_service = UserService(db_session)
        
        async def create_users_concurrently():
            tasks = []
            for i in range(10):
                user_data = UserCreate(
                    username=f"concurrent_user_{i}_{int(time.time())}",
                    email=f"concurrent_{i}_{int(time.time())}@example.com",
                    password="concurrentpassword123",
                    full_name=f"Concurrent User {i}"
                )
                task = user_service.create(user_data)
                tasks.append(task)
            
            return await asyncio.gather(*tasks)
        
        def run_concurrent_creation():
            return asyncio.run(create_users_concurrently())
        
        result = benchmark(run_concurrent_creation)
        assert len(result) == 10
    
    @pytest.mark.benchmark
    async def test_concurrent_queries(self, db_session, benchmark):
        """Test concurrent query performance."""
        user_service = UserService(db_session)
        campaign_service = CampaignService(db_session)
        ad_service = AdService(db_session)
        
        async def run_concurrent_queries():
            tasks = [
                user_service.get_all(limit=50),
                campaign_service.get_all(limit=50),
                ad_service.get_all(limit=50)
            ]
            return await asyncio.gather(*tasks)
        
        def run_queries():
            return asyncio.run(run_concurrent_queries())
        
        result = benchmark(run_queries)
        assert len(result) == 3
        assert all(isinstance(r, list) for r in result)


class TestDataProcessingPerformance:
    """Test data processing performance."""
    
    @pytest.mark.benchmark
    async def test_performance_data_aggregation(self, db_session, benchmark):
        """Test performance data aggregation speed."""
        performance_service = PerformanceService(db_session)
        
        def aggregate_performance_data():
            async def get_aggregated_data():
                # Get all performance data
                performances = await performance_service.get_all(limit=1000)
                
                # Aggregate by metric type
                aggregated = {}
                for perf in performances:
                    metric_type = perf.metric_type
                    if metric_type not in aggregated:
                        aggregated[metric_type] = {
                            'count': 0,
                            'total_value': 0,
                            'total_cost': 0
                        }
                    
                    aggregated[metric_type]['count'] += 1
                    aggregated[metric_type]['total_value'] += perf.value
                    aggregated[metric_type]['total_cost'] += perf.cost or 0
                
                return aggregated
            
            return asyncio.run(get_aggregated_data())
        
        result = benchmark(aggregate_performance_data)
        assert isinstance(result, dict)
    
    @pytest.mark.benchmark
    async def test_campaign_analytics_calculation(self, db_session, benchmark):
        """Test campaign analytics calculation performance."""
        campaign_service = CampaignService(db_session)
        performance_service = PerformanceService(db_session)
        
        def calculate_campaign_analytics():
            async def get_analytics():
                campaigns = await campaign_service.get_all(limit=100)
                analytics = []
                
                for campaign in campaigns:
                    performances = await performance_service.get_by_campaign(campaign.id)
                    
                    if performances:
                        total_impressions = sum(p.value for p in performances if p.metric_type == 'impressions')
                        total_clicks = sum(p.value for p in performances if p.metric_type == 'clicks')
                        total_cost = sum(p.cost or 0 for p in performances)
                        
                        ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
                        cpc = (total_cost / total_clicks) if total_clicks > 0 else 0
                        
                        analytics.append({
                            'campaign_id': campaign.id,
                            'campaign_name': campaign.name,
                            'total_impressions': total_impressions,
                            'total_clicks': total_clicks,
                            'total_cost': total_cost,
                            'ctr': ctr,
                            'cpc': cpc
                        })
                
                return analytics
            
            return asyncio.run(get_analytics())
        
        result = benchmark(calculate_campaign_analytics)
        assert isinstance(result, list)
