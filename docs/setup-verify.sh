#!/bin/bash
# =============================================================================
# AI Security Lab — Day 1 Setup Script
# Mac Mini M1 · macOS
# Run this script to verify your environment is ready for the lab
# =============================================================================

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Colour

echo ""
echo "============================================================"
echo "  AI Security Lab — Environment Verification"
echo "  Narendra Karki · CAISP · 2026"
echo "============================================================"
echo ""

PASS=0
FAIL=0

check() {
    local name="$1"
    local cmd="$2"
    if eval "$cmd" > /dev/null 2>&1; then
        echo -e "  ${GREEN}✓${NC} $name"
        PASS=$((PASS + 1))
    else
        echo -e "  ${RED}✗${NC} $name"
        FAIL=$((FAIL + 1))
    fi
}

echo "--- Core tools ---"
check "Homebrew"         "brew --version"
check "Git"             "git --version"
check "Python 3.11+"    "python3 -c 'import sys; assert sys.version_info >= (3,11)'"
check "pip"             "pip3 --version"
check "VS Code CLI"     "code --version"
check "Docker"          "docker ps"
check "Ollama"          "curl -s http://localhost:11434/api/tags"

echo ""
echo "--- Python packages (Module 1) ---"
check "Flask"           "python3 -c 'import flask'"
check "requests"        "python3 -c 'import requests'"
check "python-dotenv"   "python3 -c 'import dotenv'"
check "langchain"       "python3 -c 'import langchain'"

echo ""
echo "--- Ollama models ---"
check "llama3 model"    "ollama list 2>/dev/null | grep -q llama3"
check "phi3 model"      "ollama list 2>/dev/null | grep -q phi3"

echo ""
echo "--- Git configuration ---"
check "Git user name"   "git config --global user.name | grep -q '.'"
check "Git user email"  "git config --global user.email | grep -q '.'"

echo ""
echo "============================================================"
echo -e "  Results: ${GREEN}${PASS} passed${NC} · ${RED}${FAIL} failed${NC}"
echo "============================================================"
echo ""

if [ $FAIL -gt 0 ]; then
    echo -e "${YELLOW}Some checks failed. See Exercise 01 for installation steps.${NC}"
    echo ""
fi

# Garak check separately (may not be installed yet)
if garak --version > /dev/null 2>&1; then
    echo -e "  ${GREEN}✓${NC} Garak (LLM scanner)"
else
    echo -e "  ${YELLOW}!${NC} Garak not installed — run: pip install garak"
fi

echo ""
echo "If all checks pass, you are ready to start Exercise 01."
echo ""
