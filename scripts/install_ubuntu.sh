#!/bin/bash
# Stormy Ubuntu/Linux Installer

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}🌪️  STORMY UBUNTU INSTALLER${NC}"
echo -e "${BLUE}========================================${NC}"

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
   echo -e "${RED}Please do not run as root${NC}"
   exit 1
fi

# Update system
echo -e "${BLUE}🔹 Updating system packages...${NC}"
sudo apt-get update

# Install system dependencies
echo -e "${BLUE}🔹 Installing system dependencies...${NC}"
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    portaudio19-dev \
    python3-pyaudio \
    espeak \
    git \
    curl \
    wget \
    build-essential \
    alsa-utils \
    pulseaudio \
    pulseaudio-utils

# Check Python
PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✅ Python found: $PYTHON_VERSION${NC}"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo -e "${BLUE}🔹 Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
echo -e "${BLUE}🔹 Installing Python packages...${NC}"
pip install -r requirements.txt
pip install -r web/requirements-web.txt
pip install -r desktop/requirements-desktop.txt

# Create directories
mkdir -p data data/logs localization/stt_models localization/tts_voices

# Test microphone
echo -e "${BLUE}🔹 Testing microphone...${NC}"
python scripts/test_microphone.py

# Audio setup for Linux
echo -e "${BLUE}🔹 Configuring audio...${NC}"
if ! pulseaudio --check; then
    pulseaudio --start
fi

# Add user to audio group
sudo usermod -a -G audio $USER

# Launch options
echo -e "\n${BLUE}Launch Options:${NC}"
echo "1. Desktop version (full voice)"
echo "2. Web version (Flask server)"
echo "3. Docker container"
echo "4. Exit"

read -p "Enter choice (1-4): " choice

case $choice in
    1)
        python desktop/main.py
        ;;
    2)
        read -p "Port (default 5000): " port
        port=${port:-5000}
        IP=$(hostname -I | awk '{print $1}')
        echo -e "${GREEN}🌐 Server: http://$IP:$port${NC}"
        python web/app.py --host 0.0.0.0 --port $port
        ;;
    3)
        if command -v docker &> /dev/null; then
            docker-compose up
        else
            echo -e "${RED}Docker not installed${NC}"
        fi
        ;;
esac

echo -e "${GREEN}✅ Installation complete!${NC}"
