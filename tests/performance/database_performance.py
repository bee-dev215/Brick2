#!/usr/bin/env python3
"""
Database performance testing script.
"""

import asyncio
import time
import json
from datetime import datetime
from typing import Dict, List, Any

from brick2.core.database import get_async_session
from brick2.services import (
    UserService, CampaignService, AdService, 
    PerformanceService, LeadService, OrchestrationSessionService
)
from brick2.schemas import (
    UserCreate, CampaignCreate, AdCreate, 
    PerformanceCreate, LeadCreate, OrchestrationSessionCreate
)


class DatabasePerformanceTester:
    """Database performance testing class."""
    
    def __init__(self):
        self.results = {}
    
    async def run_all_tests(self):
        """Run all database performance tests."""
        print("Starting database performance tests...")
        
        async for db in get_async_session():
            self.db = db
            break
        
        # Run individual tests
        await self.test_user_operations()
        await self.test_campaign_operations()
        await self.test_ad_operations()
        await self.test_performance_operations()
        await self.test_lead_operations()
        await self.test_orchestration_operations()
        await self.test_complex_queries()
        await self.test_concurrent_operations()
        
        # Save results
        await self.save_results()
        
        print("Database performance tests completed!")
        return self.results
    
    async def test_user_operations(self):
        """Test user operation performance."""
        print("Testing user operations...")
        
        user_service = UserService(self.db)
        times = []
        
        # Test user creation
        for i in range(10):
            start_time = time.time()
            user_data = UserCreate(
                username=f"perf_test_user_{i}_{int(time.time())}",
                email=f"perf_test_{i}_{int(time.time())}@example.com",
                password="perftestpassword123",
                full_name=f"Performance Test User {i}"
            )
            await user_service.create(user_data)
            end_time = time.time()
            times.append(end_time - start_time)
        
        self.results['user_creation'] = {
            'average_time': sum(times) / len(times),
            'min_time': min(times),
            'max_time': max(times),
            'total_time': sum(times)
        }
        
        # Test user queries
        start_time = time.time()
        users = await user_service.get_all(limit=100)
        end_time = time.time()
        
        self.results['user_query'] = {
            'query_time': end_time - start_time,
            'records_returned': len(users)
        }
    
    async def test_campaign_operations(self):
        """Test campaign operation performance."""
        print("Testing campaign operations...")
        
        campaign_service = CampaignService(self.db)
        user_service = UserService(self.db)
        
        # Create a test user
        user_data = UserCreate(
            username=f"campaign_test_user_{int(time.time())}",
            email=f"campaign_test_{int(time.time())}@example.com",
            password="campaigntestpassword123",
            full_name="Campaign Test User"
        )
        user = await user_service.create(user_data)
        
        times = []
        
        # Test campaign creation
        for i in range(10):
            start_time = time.time()
            campaign_data = CampaignCreate(
                platform="Google",
                name=f"Performance Test Campaign {i}",
                budget=1000.0,
                owner_id=user.id
            )
            await campaign_service.create(campaign_data)
            end_time = time.time()
            times.append(end_time - start_time)
        
        self.results['campaign_creation'] = {
            'average_time': sum(times) / len(times),
            'min_time': min(times),
            'max_time': max(times),
            'total_time': sum(times)
        }
        
        # Test campaign queries
        start_time = time.time()
        campaigns = await campaign_service.get_all(limit=100)
        end_time = time.time()
        
        self.results['campaign_query'] = {
            'query_time': end_time - start_time,
            'records_returned': len(campaigns)
        }
    
    async def test_ad_operations(self):
        """Test ad operation performance."""
        print("Testing ad operations...")
        
        ad_service = AdService(self.db)
        campaign_service = CampaignService(self.db)
        
        # Get a campaign
        campaigns = await campaign_service.get_all(limit=1)
        if not campaigns:
            print("No campaigns found for ad testing")
            return
        
        campaign = campaigns[0]
        times = []
        
        # Test ad creation
        for i in range(10):
            start_time = time.time()
            ad_data = AdCreate(
                title=f"Performance Test Ad {i}",
                ad_type="banner",
                campaign_id=campaign.id
            )
            await ad_service.create(ad_data)
            end_time = time.time()
            times.append(end_time - start_time)
        
        self.results['ad_creation'] = {
            'average_time': sum(times) / len(times),
            'min_time': min(times),
            'max_time': max(times),
            'total_time': sum(times)
        }
        
        # Test ad queries
        start_time = time.time()
        ads = await ad_service.get_all(limit=100)
        end_time = time.time()
        
        self.results['ad_query'] = {
            'query_time': end_time - start_time,
            'records_returned': len(ads)
        }
    
    async def test_performance_operations(self):
        """Test performance data operation performance."""
        print("Testing performance operations...")
        
        performance_service = PerformanceService(self.db)
        campaign_service = CampaignService(self.db)
        
        # Get a campaign
        campaigns = await campaign_service.get_all(limit=1)
        if not campaigns:
            print("No campaigns found for performance testing")
            return
        
        campaign = campaigns[0]
        times = []
        
        # Test performance data creation
        for i in range(10):
            start_time = time.time()
            performance_data = PerformanceCreate(
                campaign_id=campaign.id,
                date=datetime.now(),
                metric_type="impressions",
                value=1000.0,
                cost=50.0
            )
            await performance_service.create(performance_data)
            end_time = time.time()
            times.append(end_time - start_time)
        
        self.results['performance_creation'] = {
            'average_time': sum(times) / len(times),
            'min_time': min(times),
            'max_time': max(times),
            'total_time': sum(times)
        }
        
        # Test performance queries
        start_time = time.time()
        performances = await performance_service.get_all(limit=100)
        end_time = time.time()
        
        self.results['performance_query'] = {
            'query_time': end_time - start_time,
            'records_returned': len(performances)
        }
    
    async def test_lead_operations(self):
        """Test lead operation performance."""
        print("Testing lead operations...")
        
        lead_service = LeadService(self.db)
        campaign_service = CampaignService(self.db)
        
        # Get a campaign
        campaigns = await campaign_service.get_all(limit=1)
        if not campaigns:
            print("No campaigns found for lead testing")
            return
        
        campaign = campaigns[0]
        times = []
        
        # Test lead creation
        for i in range(10):
            start_time = time.time()
            lead_data = LeadCreate(
                campaign_id=campaign.id,
                email=f"perf_test_lead_{i}@example.com",
                first_name="John",
                last_name="Doe"
            )
            await lead_service.create(lead_data)
            end_time = time.time()
            times.append(end_time - start_time)
        
        self.results['lead_creation'] = {
            'average_time': sum(times) / len(times),
            'min_time': min(times),
            'max_time': max(times),
            'total_time': sum(times)
        }
        
        # Test lead queries
        start_time = time.time()
        leads = await lead_service.get_all(limit=100)
        end_time = time.time()
        
        self.results['lead_query'] = {
            'query_time': end_time - start_time,
            'records_returned': len(leads)
        }
    
    async def test_orchestration_operations(self):
        """Test orchestration session operation performance."""
        print("Testing orchestration operations...")
        
        session_service = OrchestrationSessionService(self.db)
        user_service = UserService(self.db)
        
        # Get a user
        users = await user_service.get_all(limit=1)
        if not users:
            print("No users found for orchestration testing")
            return
        
        user = users[0]
        times = []
        
        # Test session creation
        for i in range(10):
            start_time = time.time()
            session_data = OrchestrationSessionCreate(
                user_id=user.id,
                session_type="campaign_creation",
                status="pending"
            )
            await session_service.create(session_data)
            end_time = time.time()
            times.append(end_time - start_time)
        
        self.results['orchestration_creation'] = {
            'average_time': sum(times) / len(times),
            'min_time': min(times),
            'max_time': max(times),
            'total_time': sum(times)
        }
        
        # Test session queries
        start_time = time.time()
        sessions = await session_service.get_all(limit=100)
        end_time = time.time()
        
        self.results['orchestration_query'] = {
            'query_time': end_time - start_time,
            'records_returned': len(sessions)
        }
    
    async def test_complex_queries(self):
        """Test complex query performance."""
        print("Testing complex queries...")
        
        campaign_service = CampaignService(self.db)
        performance_service = PerformanceService(self.db)
        
        # Test campaign with performance data
        start_time = time.time()
        campaigns = await campaign_service.get_all(limit=10)
        
        for campaign in campaigns:
            performances = await performance_service.get_by_campaign(campaign.id)
        
        end_time = time.time()
        
        self.results['complex_query'] = {
            'query_time': end_time - start_time,
            'campaigns_processed': len(campaigns)
        }
    
    async def test_concurrent_operations(self):
        """Test concurrent operation performance."""
        print("Testing concurrent operations...")
        
        user_service = UserService(self.db)
        
        async def create_user(i):
            user_data = UserCreate(
                username=f"concurrent_user_{i}_{int(time.time())}",
                email=f"concurrent_{i}_{int(time.time())}@example.com",
                password="concurrentpassword123",
                full_name=f"Concurrent User {i}"
            )
            return await user_service.create(user_data)
        
        # Test concurrent user creation
        start_time = time.time()
        tasks = [create_user(i) for i in range(10)]
        results = await asyncio.gather(*tasks)
        end_time = time.time()
        
        self.results['concurrent_operations'] = {
            'total_time': end_time - start_time,
            'operations_completed': len(results),
            'average_time_per_operation': (end_time - start_time) / len(results)
        }
    
    async def save_results(self):
        """Save test results to file."""
        results_with_timestamp = {
            'timestamp': datetime.now().isoformat(),
            'results': self.results
        }
        
        with open('database-performance-report.json', 'w') as f:
            json.dump(results_with_timestamp, f, indent=2)
        
        print("Results saved to database-performance-report.json")


async def main():
    """Run database performance tests."""
    tester = DatabasePerformanceTester()
    results = await tester.run_all_tests()
    
    # Print summary
    print("\n" + "="*50)
    print("DATABASE PERFORMANCE TEST SUMMARY")
    print("="*50)
    
    for test_name, metrics in results.items():
        print(f"\n{test_name.upper()}:")
        for metric, value in metrics.items():
            if isinstance(value, float):
                print(f"  {metric}: {value:.4f}s")
            else:
                print(f"  {metric}: {value}")


if __name__ == "__main__":
    asyncio.run(main())
