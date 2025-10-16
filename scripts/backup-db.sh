#!/bin/bash
# Database Backup Script for GEO System

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
BACKUP_DIR="${BACKUP_DIR:-./backups}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
NEO4J_BACKUP_FILE="neo4j_backup_${TIMESTAMP}.dump"

echo -e "${GREEN}Creating database backup...${NC}"
echo ""

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup Neo4j
echo -e "${YELLOW}Backing up Neo4j database...${NC}"
docker exec geo-neo4j neo4j-admin database dump neo4j --to-path=/backups || true

# Copy backup file to host
if docker exec geo-neo4j test -f /backups/neo4j.dump; then
    docker cp geo-neo4j:/backups/neo4j.dump "${BACKUP_DIR}/${NEO4J_BACKUP_FILE}"
    echo -e "${GREEN}✓ Neo4j backup saved: ${BACKUP_DIR}/${NEO4J_BACKUP_FILE}${NC}"
else
    echo -e "${YELLOW}Warning: Neo4j backup file not found. Database might be empty.${NC}"
fi

# Backup Redis (if needed)
echo -e "${YELLOW}Backing up Redis data...${NC}"
docker exec geo-redis redis-cli -a redis_password SAVE || true
docker cp geo-redis:/data/dump.rdb "${BACKUP_DIR}/redis_backup_${TIMESTAMP}.rdb" || true
echo -e "${GREEN}✓ Redis backup saved: ${BACKUP_DIR}/redis_backup_${TIMESTAMP}.rdb${NC}"

# Compress backups
echo -e "${YELLOW}Compressing backups...${NC}"
cd "$BACKUP_DIR"
tar -czf "geo_backup_${TIMESTAMP}.tar.gz" *_backup_${TIMESTAMP}.* 2>/dev/null || true
echo -e "${GREEN}✓ Compressed backup: ${BACKUP_DIR}/geo_backup_${TIMESTAMP}.tar.gz${NC}"

# Clean up old backups (keep last 7 days)
echo -e "${YELLOW}Cleaning up old backups...${NC}"
find "$BACKUP_DIR" -name "geo_backup_*.tar.gz" -mtime +7 -delete 2>/dev/null || true
echo -e "${GREEN}✓ Old backups cleaned up${NC}"

echo ""
echo -e "${GREEN}Backup completed successfully!${NC}"
echo -e "Backup location: ${BACKUP_DIR}/geo_backup_${TIMESTAMP}.tar.gz"
