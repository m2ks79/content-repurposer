#!/usr/bin/env python3
"""
Test backend API without starting full server
Run: cd projects/content-repurposer && python3 tests/test_api.py
"""

import sys
import os
import json

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

def test_imports():
    """Test if all backend modules can be imported"""
    print("📦 Testing imports...\n")

    tests = [
        ("Flask", "from flask import Flask"),
        ("Flask-CORS", "from flask_cors import CORS"),
        ("python-dotenv", "from dotenv import load_dotenv"),
        ("Anthropic SDK", "from anthropic import Anthropic"),
        ("Requests", "import requests"),
    ]

    passed = 0
    failed = 0

    for name, import_stmt in tests:
        try:
            exec(import_stmt)
            print(f"✓ {name}")
            passed += 1
        except Exception as e:
            print(f"✗ {name}")
            print(f"  Error: {str(e)[:60]}")
            failed += 1

    return passed, failed

def test_app_init():
    """Test if Flask app initializes"""
    print("\n🚀 Testing app initialization...\n")

    try:
        from app import app
        print("✓ Flask app created")

        # Test health endpoint
        with app.test_client() as client:
            response = client.get('/health')
            if response.status_code == 200:
                data = response.get_json()
                print(f"✓ Health check: {data}")
                return 2, 0
            else:
                print(f"✗ Health check failed: {response.status_code}")
                return 1, 1
    except Exception as e:
        print(f"✗ App initialization failed")
        print(f"  Error: {str(e)}")
        return 0, 1

def test_utils():
    """Test utility modules"""
    print("\n🛠️  Testing utilities...\n")

    passed = 0
    failed = 0

    try:
        from utils.video_processor import VideoProcessor
        print("✓ VideoProcessor imported")

        processor = VideoProcessor()
        print("✓ VideoProcessor instantiated")

        # Check platform specs
        if hasattr(processor, 'PLATFORMS'):
            platforms = list(processor.PLATFORMS.keys())
            print(f"✓ Platforms configured: {platforms}")
            passed += 3
        else:
            print("✗ No PLATFORMS defined")
            failed += 1
    except Exception as e:
        print(f"✗ VideoProcessor error: {str(e)[:60]}")
        failed += 1

    try:
        from utils.claude_optimizer import ClaudeOptimizer
        print("✓ ClaudeOptimizer imported")
        # Note: Can't instantiate without ANTHROPIC_API_KEY
        passed += 1
    except Exception as e:
        print(f"✗ ClaudeOptimizer error: {str(e)[:60]}")
        failed += 1

    return passed, failed

def main():
    print("\n" + "="*50)
    print("🧪 Content Repurposer - API Test")
    print("="*50 + "\n")

    total_passed = 0
    total_failed = 0

    # Test 1: Imports
    p, f = test_imports()
    total_passed += p
    total_failed += f

    # Test 2: App init
    p, f = test_app_init()
    total_passed += p
    total_failed += f

    # Test 3: Utils
    p, f = test_utils()
    total_passed += p
    total_failed += f

    # Summary
    print("\n" + "="*50)
    print(f"✓ {total_passed} passed | ✗ {total_failed} failed")
    print("="*50 + "\n")

    if total_failed == 0:
        print("🎉 All tests passed! Backend is ready.\n")
        print("Next: Start the development server")
        print("  $ make dev")
        print("  or")
        print("  $ cd backend && source .venv/bin/activate && python app.py")
        print("  $ cd frontend && npm run dev")
        return 0
    else:
        print("❌ Some tests failed. Fix errors above.\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
