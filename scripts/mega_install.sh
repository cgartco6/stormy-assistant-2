#!/bin/bash
# MEGA INSTALLER - Works on Windows (Git Bash), macOS, Linux
# One script to rule them all!

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${PURPLE}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║     🌪️  STORMY ASSISTANT - MEGA CROSS-PLATFORM INSTALLER   ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Detect OS
OS="unknown"
case "$(uname -s)" in
    Linux*)     OS="linux";;
    Darwin*)    OS="macos";;
    CYGWIN*|MINGW*|MSYS*) OS="windows";;
    *)          OS="unknown"
esac

echo -e "${CYAN}🔹 Detected OS: $OS${NC}"

# Detect architecture
ARCH=$(uname -m)
echo -e "${CYAN}🔹 Architecture: $ARCH${NC}"

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON="python3"
elif command -v python &> /dev/null; then
    PYTHON="python"
else
    echo -e "${RED}❌ Python not found! Please install Python 3.8+${NC}"
    exit 1
fi

PY_VERSION=$($PYTHON --version)
echo -e "${GREEN}✅ $PY_VERSION${NC}"

# Check pip
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo -e "${YELLOW}⚠️  pip not found, installing...${NC}"
    $PYTHON -m ensurepip --upgrade
fi

# Set pip command
if command -v pip3 &> /dev/null; then
    PIP="pip3"
else
    PIP="pip"
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    echo -e "${CYAN}🔹 Creating virtual environment...${NC}"
    $PYTHON -m venv venv
fi

# Activate based on OS
if [ "$OS" = "windows" ]; then
    source venv/Scripts/activate 2>/dev/null || . venv/Scripts/activate
else
    source venv/bin/activate
fi

# Upgrade pip
echo -e "${CYAN}🔹 Upgrading pip...${NC}"
$PIP install --upgrade pip

# Install requirements
echo -e "${CYAN}🔹 Installing dependencies...${NC}"
$PIP install -r requirements.txt
$PIP install -r web/requirements-web.txt
$PIP install -r desktop/requirements-desktop.txt

# OS-specific installations
if [ "$OS" = "linux" ]; then
    echo -e "${CYAN}🔹 Installing Linux audio dependencies...${NC}"
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y portaudio19-dev python3-pyaudio espeak pulseaudio
    elif command -v yum &> /dev/null; then
        sudo yum install -y portaudio-devel python3-pyaudio espeak pulseaudio
    fi
elif [ "$OS" = "macos" ]; then
    echo -e "${CYAN}🔹 Installing macOS audio dependencies...${NC}"
    if command -v brew &> /dev/null; then
        brew install portaudio espeak pulseaudio
    fi
elif [ "$OS" = "windows" ]; then
    echo -e "${CYAN}🔹 Installing Windows audio dependencies...${NC}"
    # Try to install PyAudio
    $PIP install pyaudio || echo -e "${YELLOW}⚠️  PyAudio failed, may need manual install${NC}"
fi

# Create directories
mkdir -p data data/logs localization/stt_models localization/tts_voices

# Test microphone
echo -e "${CYAN}🔹 Testing microphone...${NC}"
$PYTHON scripts/test_microphone.py

# Check Docker
if command -v docker &> /dev/null; then
    echo -e "${GREEN}✅ Docker found${NC}"
    HAS_DOCKER=true
else
    HAS_DOCKER=false
fi

# Check Git
if command -v git &> /dev/null; then
    echo -e "${GREEN}✅ Git found${NC}"
    HAS_GIT=true
else
    HAS_GIT=false
fi

# Menu
while true; do
    echo -e "\n${PURPLE}════════════════════════════════════════════${NC}"
    echo -e "${CYAN}🌪️  STORMY LAUNCH MENU${NC}"
    echo -e "${PURPLE}════════════════════════════════════════════${NC}"
    echo "1) 🖥️  Desktop Version (Full voice, local)"
    echo "2) 🌐 Web Version (Flask server - access from phone)"
    echo "3) 🐳 Docker Container"
    echo "4) ☁️  Deploy to Render"
    echo "5) ☁️  Deploy to PythonAnywhere"
    echo "6) 📦 Create GitHub Repository"
    echo "7) 🔧 Run Tests"
    echo "8) ❌ Exit"
    echo -e "${PURPLE}════════════════════════════════════════════${NC}"
    read -p "Choice [1-8]: " choice

    case $choice in
        1)
            echo -e "${GREEN}Launching Desktop Stormy...${NC}"
            $PYTHON desktop/main.py
            ;;
        2)
            read -p "Port [default: 5000]: " port
            port=${port:-5000}
            
            # Get IP address based on OS
            if [ "$OS" = "macos" ]; then
                IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "localhost")
            elif [ "$OS" = "linux" ]; then
                IP=$(hostname -I | awk '{print $1}' 2>/dev/null || echo "localhost")
            else
                IP="localhost"
            fi
            
            echo -e "${GREEN}🌐 Server running at:${NC}"
            echo -e "   ${CYAN}http://localhost:$port${NC} (this computer)"
            echo -e "   ${CYAN}http://$IP:$port${NC} (other devices on network)"
            $PYTHON web/app.py --host 0.0.0.0 --port $port
            ;;
        3)
            if [ "$HAS_DOCKER" = true ]; then
                echo -e "${GREEN}Starting Docker container...${NC}"
                docker-compose up
            else
                echo -e "${RED}Docker not installed${NC}"
            fi
            ;;
        4)
            echo -e "${CYAN}Deploying to Render...${NC}"
            $PYTHON scripts/deploy_render.py
            ;;
        5)
            echo -e "${CYAN}Deploying to PythonAnywhere...${NC}"
            $PYTHON scripts/deploy_pythonanywhere.py
            ;;
        6)
            if [ "$HAS_GIT" = true ]; then
                echo -e "${CYAN}Creating GitHub repository...${NC}"
                read -p "GitHub username: " GH_USER
                read -p "Repository name [stormy-assistant-2]: " REPO_NAME
                REPO_NAME=${REPO_NAME:-stormy-assistant-2}
                
                curl -u "$GH_USER" https://api.github.com/user/repos -d "{\"name\":\"$REPO_NAME\"}"
                git init
                git add .
                git commit -m "Initial commit"
                git branch -M main
                git remote add origin "https://github.com/$GH_USER/$REPO_NAME.git"
                git push -u origin main
                echo -e "${GREEN}✅ Repository created and pushed!${NC}"
            else
                echo -e "${RED}Git not installed${NC}"
            fi
            ;;
        7)
            echo -e "${CYAN}Running tests...${NC}"
            $PYTHON -m pytest tests/ -v
            ;;
        8)
            echo -e "${GREEN}Thank you for using Stormy! 🌪️${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid choice${NC}"
            ;;
    esac
done
