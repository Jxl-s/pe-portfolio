#!/bin/bash
BASE_URL=http://127.0.0.1:5000

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 1. Test post creation
echo -e "${YELLOW}> 1. Create Post ...${NC}"

TEST_NAME="Jia $RANDOM"
TEST_EMAIL="Jia@$RANDOM.com"
TEST_CONTENT="Hello, $RANDOM"

TEST_POST=$(curl -sS -X POST "$BASE_URL/api/timeline_post" \
    -d "name=$TEST_NAME" \
    -d "email=$TEST_EMAIL" \
    -d "content=$TEST_CONTENT")

# Make sure the post was successfully created
TEST_POST_AS_ROW=$(echo "$TEST_POST" | jq -r '"\(.id) \(.name) \(.email) \(.content)"')

TEST_ID=$(echo "$TEST_POST" | jq -r '.id')
EXPECTED_ROW="$TEST_ID $TEST_NAME $TEST_EMAIL $TEST_CONTENT"

if [[ "$TEST_POST_AS_ROW" != "$EXPECTED_ROW" ]]; then
    echo -e "${RED}❌ Failed to create post!"
    exit 1
else
    echo -e "${GREEN}✅ Post successfully created!"
fi

# 2. Get all the posts and flatten as rows to ensure new post is there
echo -e "${YELLOW}> 2. Get Posts ...${NC}"
ALL_POSTS=$(curl -sS -X GET "$BASE_URL/api/timeline_post")
ALL_POSTS_AS_ROWS=$(echo "$ALL_POSTS" | jq -r '.timeline_posts[] | "\(.id) \(.name) \(.email) \(.content)"')

# Testing the output with grep for an exact match
if echo "$ALL_POSTS_AS_ROWS" | grep -qxF "$EXPECTED_ROW"; then
    echo -e "${GREEN}✅ Post was found!${NC}"
else
    echo -e "${RED}❌ Post was not found${NC}"
fi

# 3. Clean the test post
echo -e "${YELLOW}> 3. Cleaning up test post ...${NC}"
curl -sS -X DELETE "$BASE_URL/api/timeline_post/$TEST_ID" > /dev/null
echo -e "${GREEN}> Done!${NC}"
