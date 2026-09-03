#!/bin/bash
# Quick sanity check - no dependencies needed
# Run: bash tests/test_quick.sh

echo ""
echo "🧪 Content Repurposer - Quick Tests"
echo "===================================="
echo ""

# 1. Check project structure
echo "1️⃣  Project Structure:"
test -d backend && echo "   ✓ backend/ exists"
test -d frontend && echo "   ✓ frontend/ exists"
test -f backend/app.py && echo "   ✓ backend/app.py"
test -f frontend/src/App.jsx && echo "   ✓ frontend/src/App.jsx"
test -f docker-compose.yml && echo "   ✓ docker-compose.yml"
echo ""

# 2. Check dependencies
echo "2️⃣  Dependencies Installed:"

# Python
if [ -d "backend/.venv" ]; then
    source backend/.venv/bin/activate
    python3 -c "import flask" 2>/dev/null && echo "   ✓ Flask"
    python3 -c "import flask_cors" 2>/dev/null && echo "   ✓ Flask-CORS"
    python3 -c "import dotenv" 2>/dev/null && echo "   ✓ python-dotenv"
    python3 -c "import anthropic" 2>/dev/null && echo "   ✓ Anthropic SDK"
    deactivate
else
    echo "   ⚠️  Backend venv not created yet"
    echo "      Run: cd backend && python3 -m venv .venv"
    echo "      Then: source .venv/bin/activate && pip install -r requirements.txt"
fi

# Node
if [ -d "frontend/node_modules" ]; then
    echo "   ✓ Node modules (68+ packages)"
else
    echo "   ⚠️  Frontend modules not installed"
    echo "      Run: cd frontend && npm install"
fi
echo ""

# 3. Ready to run
echo "3️⃣  Ready to Start:"
echo ""
echo "   Option A - Local Development:"
echo "   $ make dev"
echo ""
echo "   Option B - Docker:"
echo "   $ docker-compose up"
echo ""
echo "   Option C - GitHub Codespaces:"
echo "   https://github.com/m2ks79/content-repurposer/codespaces"
echo ""
echo "===================================="
