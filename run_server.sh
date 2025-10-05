#!/bin/bash
# WhatsApp Chat Reader - Server Runner
# Script per executar el servidor sense dependre de l'entorn virtual

set -e

# Colors per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 WhatsApp Chat Reader - Server Runner${NC}"
echo

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
        echo -e "${YELLOW}💡 Prova executar: pip3 install --user flask flask-cors${NC}"
        echo -e "${YELLOW}💡 O usa l'entorn virtual: source venv_new/bin/activate${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ Flask ja està instal·lat${NC}"
fi

echo
echo -e "${BLUE}🎯 Executant servidor...${NC}"
echo

# Run the server with all arguments passed to this script
python3 progressive_server.py "$@"
