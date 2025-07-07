#!/bin/bash
BASE_URL=http://127.0.0.1:5000

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Some test fields (with random data)
TEST_NAME="Jia $RANDOM"
TEST_EMAIL="Jia@$RANDOM.com"
TEST_CONTENT="Hello, $RANDOM"

echo -e "${YELLOW}> 1. Creating new post ...${NC}"
TEST_POST=$(curl -sS -X POST "$BASE_URL/api/timeline_post" \
    -d "name=$TEST_NAME" \
    -d "email=$TEST_EMAIL" \
    -d "content=$TEST_CONTENT")

TEST_ID=$(echo "$TEST_POST" | jq '.id')

echo -e "${YELLOW}> 2. Fetching all posts ...${NC}"
ALL_POSTS=$(curl -sS -X GET "$BASE_URL/api/timeline_post")

TEST_RESPONSES=(
    "\"id\": $TEST_ID"
    "\"name\": \"$TEST_NAME\""
    "\"email\": \"$TEST_EMAIL\""
    "\"content\": \"$TEST_CONTENT\""
)

echo -e "${YELLOW}> 3. Evaluating response ...${NC}"

fail_count=0
for i in "${!TEST_RESPONSES[@]}"; do
    response="${TEST_RESPONSES[$i]}"
    test_num=$(( i + 1 ))

    if [[ "$ALL_POSTS" == *"$response"* ]]; then
        echo -e "${GREEN}✅ Test $test_num: PASS${NC} (found: $response)"
    else
        echo -e "${RED}❌ Test $test_num: FAIL${NC} (missing: $response)"
        (( fail_count += 1 ))
    fi
done

echo "------------------------------------------"

if [[ $fail_count == 0 ]]; then
    echo -e "${GREEN}✅ Status: All tests passed!${NC}"
else
    echo -e "${RED}❌ Status: $fail_count test(s) failed!${NC}"
fi

echo -e "${YELLOW}> Cleaning up test post...${NC}"
curl -sS -X DELETE "$BASE_URL/api/timeline_post/$TEST_ID" > /dev/null

echo -e "${GREEN}> Done.${NC}"
