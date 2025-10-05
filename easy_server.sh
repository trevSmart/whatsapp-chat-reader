#!/bin/bash
# WhatsApp Chat Reader - Easy Server Runner
# Script que utilitza automàticament l'entorn virtual

set -e

# Colors per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 WhatsApp Chat Reader - Easy Server Runner${NC}"
echo

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$SCRIPT_DIR/venv_new"

# Check if virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    echo -e "${RED}❌ Entorn virtual no trobat a: $VENV_PATH${NC}"
    echo -e "${YELLOW}💡 Executa: python3 -m venv venv_new${NC}"
    echo -e "${YELLOW}💡 Després: source venv_new/bin/activate${NC}"
    echo -e "${YELLOW}💡 I finalment: pip install flask flask-cors${NC}"
    exit 1
fi

# Check if Flask is installed in the virtual environment
if ! "$VENV_PATH/bin/python" -c "import flask" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Flask no està instal·lat a l'entorn virtual${NC}"
    echo -e "${BLUE}📦 Instal·lant dependències a l'entorn virtual...${NC}"

    # Install dependencies in virtual environment
    "$VENV_PATH/bin/pip" install flask flask-cors

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Dependències instal·lades correctament${NC}"
    else
        echo -e "${RED}❌ Error instal·lant dependències${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ Flask ja està instal·lat a l'entorn virtual${NC}"
fi

echo
echo -e "${BLUE}🎯 Executant servidor amb entorn virtual...${NC}"
echo

# Run the server using the virtual environment's Python
cd "$SCRIPT_DIR"
"$VENV_PATH/bin/python" progressive_server.py "$@"
