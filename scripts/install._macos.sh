#!/bin/bash
# Stormy macOS Installer

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}🌪️  STORMY MACOS INSTALLER${NC}"
echo -e "${BLUE}========================================${NC}"

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo -e "${YELLOW}Installing Homebrew...${NC}"
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Install system dependencies
echo -e "${BLUE}🔹 Installing system dependencies...${NC}"
brew update
brew install \
    python@3.9 \
    portaudio \
    espeak \
    git \
    pulseaudio

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
        IP=$(ipconfig getifaddr en0 || ipconfig getifaddr en1)
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
