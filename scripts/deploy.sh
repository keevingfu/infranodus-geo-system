#!/bin/bash
# GEO System Deployment Script

set -e  # Exit on error
set -u  # Exit on undefined variable

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Configuration
ENVIRONMENT="${1:-staging}"
VERSION="${2:-latest}"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  GEO System Deployment${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "Environment: ${YELLOW}${ENVIRONMENT}${NC}"
echo -e "Version: ${YELLOW}${VERSION}${NC}"
echo ""

# Validate environment
if [[ ! "$ENVIRONMENT" =~ ^(staging|production)$ ]]; then
    echo -e "${RED}Error: Invalid environment. Use 'staging' or 'production'${NC}"
    exit 1
fi

# Change to project root
cd "$PROJECT_ROOT"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Warning: .env file not found. Using default values.${NC}"
    echo -e "${YELLOW}Creating .env from .env.example...${NC}"
    if [ -f ".env.example" ]; then
        cp .env.example .env
    else
        echo -e "${RED}Error: Neither .env nor .env.example found${NC}"
        exit 1
    fi
fi

# Pull latest code
echo -e "${GREEN}[1/8] Pulling latest code...${NC}"
git pull origin main

# Stop existing containers
echo -e "${GREEN}[2/8] Stopping existing containers...${NC}"
docker-compose down

# Pull latest images
echo -e "${GREEN}[3/8] Pulling latest Docker images...${NC}"
docker-compose pull

# Build application
echo -e "${GREEN}[4/8] Building application...${NC}"
docker-compose build --no-cache geo-api

# Create backup of Neo4j data
echo -e "${GREEN}[5/8] Creating backup...${NC}"
bash "$SCRIPT_DIR/backup-db.sh"

# Start services
echo -e "${GREEN}[6/8] Starting services...${NC}"
docker-compose up -d

# Wait for services to be healthy
echo -e "${GREEN}[7/8] Waiting for services to be healthy...${NC}"
sleep 10

# Health check
echo -e "${GREEN}[8/8] Running health checks...${NC}"
bash "$SCRIPT_DIR/health-check.sh"

# Display status
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Deployment Completed Successfully!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "Services status:"
docker-compose ps

echo ""
echo -e "Application URLs:"
echo -e "  Neo4j Browser: ${GREEN}http://localhost:7474${NC}"
echo -e "  API Docs: ${GREEN}http://localhost:8000/docs${NC}"
echo -e "  Health Check: ${GREEN}http://localhost:8000/health${NC}"

echo ""
echo -e "${YELLOW}Deployment logs:${NC}"
echo -e "  View logs: ${GREEN}docker-compose logs -f${NC}"
echo -e "  View specific service: ${GREEN}docker-compose logs -f geo-api${NC}"
