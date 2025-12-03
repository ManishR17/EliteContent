#!/bin/bash
# EliteContent API Testing Script
# Tests all POST endpoints with correct data

BASE_URL="http://localhost:8000"

echo "🧪 Testing EliteContent API Endpoints"
echo "======================================"

# Test 1: Auth - Register
echo -e "\n1. Testing /api/auth/register..."
curl -s -X POST "$BASE_URL/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"test'$(date +%s)'@example.com","password":"test123","full_name":"Test User"}' \
  | python3 -m json.tool

# Test 2: Document Generation
echo -e "\n2. Testing /api/document/generate..."
curl -s -X POST "$BASE_URL/api/document/generate" \
  -H "Content-Type: application/json" \
  -d '{"document_type":"cover_letter","topic":"Software Engineer","target_audience":"Tech Company","key_points":["Python","FastAPI","AI"]}' \
  | python3 -m json.tool | head -20

# Test 3: Email Generation
echo -e "\n3. Testing /api/email/generate..."
curl -s -X POST "$BASE_URL/api/email/generate" \
  -H "Content-Type: application/json" \
  -d '{"email_type":"professional","recipient":"Hiring Manager","purpose":"Job application","key_points":["Experience","Skills"]}' \
  | python3 -m json.tool | head -20

# Test 4: Social Media Generation
echo -e "\n4. Testing /api/social/generate..."
curl -s -X POST "$BASE_URL/api/social/generate" \
  -H "Content-Type: application/json" \
  -d '{"platform":"twitter","content_type":"post","topic":"AI Technology","tone":"professional"}' \
  | python3 -m json.tool | head -20

# Test 5: Creative Content Generation
echo -e "\n5. Testing /api/creative/generate..."
curl -s -X POST "$BASE_URL/api/creative/generate" \
  -H "Content-Type: application/json" \
  -d '{"content_type":"blog","topic":"Technology Trends","target_audience":"Tech enthusiasts","tone":"informative"}' \
  | python3 -m json.tool | head -20

# Test 6: Research Generation
echo -e "\n6. Testing /api/research/generate..."
curl -s -X POST "$BASE_URL/api/research/generate" \
  -H "Content-Type: application/json" \
  -d '{"topic":"Artificial Intelligence","depth":"standard","sources_count":3}' \
  | python3 -m json.tool | head -20

# Test 7: Dashboard Stats
echo -e "\n7. Testing /api/dashboard/stats..."
curl -s -X GET "$BASE_URL/api/dashboard/stats" \
  | python3 -m json.tool

echo -e "\n✅ API Testing Complete!"
