#!/bin/bash

echo "🧪 Quick Test Suite"
echo "==================="
echo ""

# Backend health check
echo "1️⃣  Testing Backend..."
cd backend
source venv/bin/activate
pytest tests/ -q --tb=line 2>&1 | tail -1

# Frontend tests
echo ""
echo "2️⃣  Testing Frontend..."
cd ../frontend
npm test -- --run 2>&1 | grep "Test Files"

echo ""
echo "✅ Quick test complete!"
