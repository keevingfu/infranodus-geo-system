#!/bin/bash
# Health Check Script for GEO System

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Running health checks...${NC}"
echo ""

# Function to check service health
check_service() {
    local service_name=$1
    local url=$2
    local max_retries=30
    local retry=0

    echo -n "Checking ${service_name}... "

    while [ $retry -lt $max_retries ]; do
        if curl -sf "$url" > /dev/null 2>&1; then
            echo -e "${GREEN}✓ Healthy${NC}"
            return 0
        fi
        retry=$((retry + 1))
        sleep 2
    done

    echo -e "${RED}✗ Unhealthy (timeout after ${max_retries} retries)${NC}"
    return 1
}

# Function to check Neo4j
check_neo4j() {
    echo -n "Checking Neo4j... "

    if docker exec geo-neo4j cypher-shell -u neo4j -p geo_password_2025 "RETURN 1" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Healthy${NC}"
        return 0
    else
        echo -e "${RED}✗ Unhealthy${NC}"
        return 1
    fi
}

# Function to check Redis
check_redis() {
    echo -n "Checking Redis... "

    if docker exec geo-redis redis-cli -a redis_password PING > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Healthy${NC}"
        return 0
    else
        echo -e "${RED}✗ Unhealthy${NC}"
        return 1
    fi
}

# Run checks
all_healthy=true

check_neo4j || all_healthy=false
check_redis || all_healthy=false
check_service "API" "http://localhost:8000/health" || all_healthy=false

echo ""

if [ "$all_healthy" = true ]; then
    echo -e "${GREEN}All services are healthy! ✓${NC}"
    exit 0
else
    echo -e "${RED}Some services are unhealthy! ✗${NC}"
    echo ""
    echo -e "${YELLOW}Troubleshooting:${NC}"
    echo "1. Check logs: docker-compose logs"
    echo "2. Check container status: docker-compose ps"
    echo "3. Restart services: docker-compose restart"
    exit 1
fi
