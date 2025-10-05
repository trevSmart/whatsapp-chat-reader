#!/bin/bash
# WhatsApp Chat Reader - Universal Server Runner
# Script intel·ligent que intenta usar entorn virtual primer, després instal·lació global

set -e

# Colors per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 WhatsApp Chat Reader - Server Runner${NC}"
echo

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$SCRIPT_DIR/venv_new"

# Strategy 1: Try to use virtual environment if it exists
if [ -d "$VENV_PATH" ]; then
    echo -e "${BLUE}📦 Entorn virtual detectat: $VENV_PATH${NC}"
    
    # Check if Flask is installed in the virtual environment
    if "$VENV_PATH/bin/python" -c "import flask" 2>/dev/null; then
        echo -e "${GREEN}✅ Usant entorn virtual amb Flask instal·lat${NC}"
        echo
        echo -e "${BLUE}🎯 Executant servidor amb entorn virtual...${NC}"
        echo
        
        # Run the server using the virtual environment's Python
        cd "$SCRIPT_DIR"
        "$VENV_PATH/bin/python" progressive_server.py "$@"
        exit 0
    else
        echo -e "${YELLOW}⚠️  Flask no està instal·lat a l'entorn virtual${NC}"
        echo -e "${BLUE}📦 Instal·lant dependències a l'entorn virtual...${NC}"
        
        # Install dependencies in virtual environment
        "$VENV_PATH/bin/pip" install flask flask-cors
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ Dependències instal·lades correctament${NC}"
            echo
            echo -e "${BLUE}🎯 Executant servidor amb entorn virtual...${NC}"
            echo
            
            cd "$SCRIPT_DIR"
            "$VENV_PATH/bin/python" progressive_server.py "$@"
            exit 0
        else
            echo -e "${RED}❌ Error instal·lant dependències a l'entorn virtual${NC}"
            echo -e "${YELLOW}💡 Intentant amb instal·lació global...${NC}"
            echo
        fi
    fi
fi

# Strategy 2: Use global Python installation
echo -e "${BLUE}📦 Provant amb Python global del sistema${NC}"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 no està instal·lat al sistema${NC}"
    exit 1
fi

# Check if Flask is installed globally
if ! python3 -c "import flask" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Flask no està instal·lat globalment${NC}"
    echo -e "${BLUE}📦 Instal·lant dependències amb --user...${NC}"
    
    # Install dependencies with --user flag
    pip3 install --user flask flask-cors
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Dependències instal·lades correctament${NC}"
    else
        echo -e "${RED}❌ Error instal·lant dependències${NC}"
        echo
        echo -e "${YELLOW}💡 Solucions possibles:${NC}"
        echo -e "${YELLOW}   1. Crea un entorn virtual: python3 -m venv venv_new${NC}"
        echo -e "${YELLOW}   2. Activa'l: source venv_new/bin/activate${NC}"
        echo -e "${YELLOW}   3. Instal·la dependències: pip install flask flask-cors${NC}"
        echo -e "${YELLOW}   4. Torna a executar aquest script${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ Flask ja està instal·lat globalment${NC}"
fi

echo
echo -e "${BLUE}🎯 Executant servidor amb Python global...${NC}"
echo

# Run the server with all arguments passed to this script
cd "$SCRIPT_DIR"
python3 progressive_server.py "$@"
