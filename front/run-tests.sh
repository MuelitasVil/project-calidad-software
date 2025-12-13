#!/bin/bash
# Helper script to run frontend tests in Docker

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# Navigate to project root (one level up from front/)
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Change to project root
cd "$PROJECT_ROOT"

echo -e "${GREEN}🧪 Running frontend tests in Docker...${NC}"
echo ""

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo -e "${RED}❌ Error: docker-compose.yml not found in project root: $PROJECT_ROOT${NC}"
    exit 1
fi

# Check if services are running
if ! docker compose ps 2>/dev/null | grep -q "frontend-service.*Up"; then
    echo -e "${YELLOW}⚠️  Frontend service doesn't seem to be running.${NC}"
    echo "Starting services..."
    docker compose up -d frontend auth-service users-service mysql localstack
    echo "Waiting for services to be ready..."
    sleep 10
fi

# Build test image if needed
echo -e "${YELLOW}📦 Building test image (if needed)...${NC}"
docker compose --profile test build frontend-tests

# Parse argument
ARG="$1"

# Determine if argument is a test type or a file path
if [ -z "$ARG" ]; then
    # No argument - run all tests
    echo -e "${GREEN}Running all tests...${NC}"
    docker compose --profile test run --rm frontend-tests pytest -v
elif [ "$ARG" == "unit" ]; then
    # Run all unit tests
    echo -e "${GREEN}Running unit tests...${NC}"
    docker compose --profile test run --rm frontend-tests pytest -m unit -v
elif [ "$ARG" == "integration" ]; then
    # Run all integration tests
    echo -e "${GREEN}Running integration tests...${NC}"
    docker compose --profile test run --rm frontend-tests pytest -m integration -v -s
elif [ "$ARG" == "end-to-end" ]; then
    # Run all end-to-end tests
    echo -e "${GREEN}Running end-to-end tests...${NC}"
    docker compose --profile test run --rm frontend-tests pytest -m end_to_end -v -s
elif [ "$ARG" == "all" ]; then
    # Run all tests
    echo -e "${GREEN}Running all tests...${NC}"
    docker compose --profile test run --rm frontend-tests pytest -v
else
    # Treat as a specific test file path
    echo -e "${GREEN}Running specific test: $ARG${NC}"
    docker compose --profile test run --rm frontend-tests pytest "$ARG" -v -s
fi

echo ""
echo -e "${GREEN}✅ Tests completed!${NC}"