#!/bin/bash
# Stormy Docker Setup Script

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}🐳 STORMY DOCKER SETUP${NC}"
echo -e "${BLUE}========================================${NC}"

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker not found. Please install Docker first.${NC}"
    exit 1
fi

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo -e "${YELLOW}Docker Compose not found. Installing...${NC}"
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Build Docker image
echo -e "${BLUE}🔹 Building Docker image...${NC}"
docker build -t stormy:latest .

# Create data directories
mkdir -p data data/logs

# Run with Docker Compose
echo -e "${BLUE}🔹 Starting containers...${NC}"
docker-compose up -d

# Show status
echo -e "${BLUE}🔹 Container status:${NC}"
docker-compose ps

# Show logs
echo -e "${BLUE}🔹 Container logs:${NC}"
docker-compose logs --tail=50

echo -e "${GREEN}✅ Stormy is running in Docker!${NC}"
echo -e "${GREEN}🌐 Web interface: http://localhost:5000${NC}"
