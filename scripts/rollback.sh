#!/bin/bash
# Rollback Script for GEO System

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
BACKUP_DIR="${BACKUP_DIR:-./backups}"

echo -e "${RED}========================================${NC}"
echo -e "${RED}  GEO System Rollback${NC}"
echo -e "${RED}========================================${NC}"
echo ""

# List available backups
echo -e "${YELLOW}Available backups:${NC}"
ls -lht "$BACKUP_DIR"/*.tar.gz 2>/dev/null | head -5 || {
    echo -e "${RED}No backups found in ${BACKUP_DIR}${NC}"
    exit 1
}

echo ""
echo -e "${YELLOW}Enter backup filename to restore (or 'latest' for most recent):${NC}"
read -r backup_file

if [ "$backup_file" = "latest" ]; then
    backup_file=$(ls -t "$BACKUP_DIR"/*.tar.gz 2>/dev/null | head -1)
    if [ -z "$backup_file" ]; then
        echo -e "${RED}No backups found${NC}"
        exit 1
    fi
    echo -e "Selected: ${GREEN}$(basename "$backup_file")${NC}"
elif [ ! -f "$BACKUP_DIR/$backup_file" ]; then
    echo -e "${RED}Backup file not found: $backup_file${NC}"
    exit 1
else
    backup_file="$BACKUP_DIR/$backup_file"
fi

# Confirm rollback
echo ""
echo -e "${RED}WARNING: This will restore the database to a previous state.${NC}"
echo -e "${RED}Current data will be overwritten!${NC}"
echo ""
echo -e "${YELLOW}Continue with rollback? (yes/no):${NC}"
read -r confirm

if [ "$confirm" != "yes" ]; then
    echo -e "${YELLOW}Rollback cancelled.${NC}"
    exit 0
fi

# Create current backup before rollback
echo -e "${GREEN}[1/5] Creating backup of current state...${NC}"
bash "$(dirname "$0")/backup-db.sh"

# Stop services
echo -e "${GREEN}[2/5] Stopping services...${NC}"
docker-compose down

# Extract backup
echo -e "${GREEN}[3/5] Extracting backup...${NC}"
TEMP_DIR=$(mktemp -d)
tar -xzf "$backup_file" -C "$TEMP_DIR"

# Restore Neo4j
echo -e "${GREEN}[4/5] Restoring Neo4j database...${NC}"
NEO4J_DUMP=$(find "$TEMP_DIR" -name "neo4j_backup_*.dump" | head -1)
if [ -n "$NEO4J_DUMP" ]; then
    # Start only Neo4j
    docker-compose up -d neo4j
    sleep 10

    # Copy dump file to container
    docker cp "$NEO4J_DUMP" geo-neo4j:/backups/restore.dump

    # Stop Neo4j and restore
    docker-compose stop neo4j
    docker-compose run --rm neo4j neo4j-admin database load neo4j --from-path=/backups/restore.dump --overwrite-destination=true || true
fi

# Restore Redis
REDIS_DUMP=$(find "$TEMP_DIR" -name "redis_backup_*.rdb" | head -1)
if [ -n "$REDIS_DUMP" ]; then
    docker cp "$REDIS_DUMP" geo-redis:/data/dump.rdb
fi

# Clean up temp directory
rm -rf "$TEMP_DIR"

# Start all services
echo -e "${GREEN}[5/5] Starting services...${NC}"
docker-compose up -d

# Wait and health check
echo -e "${YELLOW}Waiting for services to start...${NC}"
sleep 15

bash "$(dirname "$0")/health-check.sh"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Rollback Completed Successfully!${NC}"
echo -e "${GREEN}========================================${NC}"
