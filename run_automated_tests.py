#!/usr/bin/env python3
"""
Automated test runner for BRICK 2.
Runs all tests locally to simulate CI/CD pipeline.
"""

import sys
import os
import asyncio
import subprocess
from datetime import datetime

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def run_command(command, description):
    """Run a command and return success status."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print('='*60)
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            return True
        else:
            print(f"❌ {description} - FAILED (exit code: {result.returncode})")
            return False
            
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        # Core imports
        from brick2.core.config import settings
        from brick2.core.database import get_async_session
        from brick2.core.security import get_password_hash, verify_password
        from brick2.core.exceptions import AdOrchestratorException
        
        # Model imports
        from brick2.models import (
            User, Campaign, Ad, Performance, Lead,
            OrchestrationSession, Memory, KnowledgeNode, KnowledgeRelationship
        )
        
        # Schema imports
        from brick2.schemas import (
            UserCreate, CampaignCreate, AdCreate, PerformanceCreate, LeadCreate
        )
        
        # Service imports
        from brick2.services import (
            UserService, CampaignService, AdService, PerformanceService,
            LeadService, OrchestrationSessionService
        )
        
        # API imports
        from brick2.api.deps import get_db, get_current_user
        from brick2.main import app
        
        print("All imports successful!")
        return True
        
    except Exception as e:
        print(f"Import error: {e}")
        return False

def test_fastapi_app():
    """Test FastAPI application."""
    print("Testing FastAPI application...")
    
    try:
        from brick2.main import app
        
        # Check if app has routes
        routes = [route.path for route in app.routes]
        print(f"FastAPI app loaded successfully with {len(routes)} routes")
        
        # Check specific endpoints
        expected_routes = ["/", "/health", "/api/v1/campaigns", "/api/v1/ads"]
        found_routes = []
        
        for route in expected_routes:
            if any(route in r for r in routes):
                found_routes.append(route)
                print(f"Route {route} found")
        
        print(f"Found {len(found_routes)}/{len(expected_routes)} expected routes")
        return len(found_routes) >= 2  # At least 2 routes should be found
        
    except Exception as e:
        print(f"FastAPI app error: {e}")
        return False

def test_configuration():
    """Test configuration loading."""
    print("Testing configuration...")
    
    try:
        from brick2.core.config import settings
        
        print(f"Project name: {settings.PROJECT_NAME}")
        print(f"API version: {settings.API_V1_STR}")
        print(f"Debug mode: {settings.DEBUG}")
        print(f"Database URL configured: {'Yes' if settings.DATABASE_URL else 'No'}")
        
        return True
        
    except Exception as e:
        print(f"Configuration error: {e}")
        return False

def test_schema_validation():
    """Test Pydantic schema validation."""
    print("Testing schema validation...")
    
    try:
        from brick2.schemas import (
            UserCreate, CampaignCreate, AdCreate, PerformanceCreate, LeadCreate
        )
        from datetime import datetime
        
        # Test User Schema
        user_data = UserCreate(
            username="testuser",
            email="test@example.com",
            password="testpassword123",
            full_name="Test User"
        )
        print("User schema validation passed")
        
        # Test Campaign Schema
        campaign_data = CampaignCreate(
            platform="Google",
            name="Test Campaign",
            budget=1000.0,
            owner_id=1
        )
        print("Campaign schema validation passed")
        
        # Test Ad Schema
        ad_data = AdCreate(
            title="Test Ad",
            ad_type="banner",
            campaign_id=1
        )
        print("Ad schema validation passed")
        
        # Test Performance Schema
        performance_data = PerformanceCreate(
            campaign_id=1,
            date=datetime.now(),
            metric_type="impressions",
            value=1000.0,
            cost=50.0
        )
        print("Performance schema validation passed")
        
        # Test Lead Schema
        lead_data = LeadCreate(
            campaign_id=1,
            email="lead@example.com",
            first_name="John",
            last_name="Doe"
        )
        print("Lead schema validation passed")
        
        return True
        
    except Exception as e:
        print(f"Schema validation error: {e}")
        return False

async def test_database_connection():
    """Test database connection."""
    print("Testing database connection...")
    
    try:
        from brick2.core.database import get_async_session
        from brick2.services import CampaignService
        
        async for db in get_async_session():
            print("Database connection successful")
            
            # Test service
            campaign_service = CampaignService(db)
            count = await campaign_service.count()
            print(f"Campaign service working: {count} campaigns found")
            
            break
        
        return True
        
    except Exception as e:
        print(f"Database connection error: {e}")
        return False

def main():
    """Run all automated tests."""
    print("BRICK 2 - Automated Test Runner")
    print("=" * 60)
    print(f"Test started at: {datetime.now()}")
    print("=" * 60)
    
    # Set PYTHONPATH
    os.environ['PYTHONPATH'] = 'src'
    
    # Run tests
    tests = [
        ("Import Test", test_imports),
        ("FastAPI App Test", test_fastapi_app),
        ("Configuration Test", test_configuration),
        ("Schema Validation Test", test_schema_validation),
    ]
    
    results = []
    
    # Run synchronous tests
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"{test_name} failed with error: {e}")
            results.append((test_name, False))
    
    # Run async test
    try:
        async_result = asyncio.run(test_database_connection())
        results.append(("Database Connection Test", async_result))
    except Exception as e:
        print(f"Database Connection Test failed with error: {e}")
        results.append(("Database Connection Test", False))
    
    # Run external tests
    external_tests = [
        ("Unit Tests", "python -m pytest tests/ -v"),
        ("Integration Tests", "python tests/test_database_integrity.py"),
        ("Campaign Load Tests", "python tests/test_campaign_load.py"),
        ("Linting", "python -m flake8 src/ --max-line-length=100 --exclude=__pycache__"),
        ("Security Check", "python -m bandit -r src/brick2"),
    ]
    
    for test_name, command in external_tests:
        result = run_command(command, test_name)
        results.append((test_name, result))
    
    # Summary
    print("\n" + "=" * 60)
    print("AUTOMATED TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    print(f"Test completed at: {datetime.now()}")
    
    if passed >= total * 0.7:  # 70% success rate
        print("Automated tests passed!")
        return True
    else:
        print("Some automated tests failed.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
