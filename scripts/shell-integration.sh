#!/bin/bash
# EasyPost MCP - Shell Integration
# Source this file in your ~/.zshrc or ~/.bashrc

# Project root detection
export EASYPOST_PROJECT_ROOT="${EASYPOST_PROJECT_ROOT:-$HOME/easypost-mcp-project}"

# Aliases for common workflows
alias ep='cd "$EASYPOST_PROJECT_ROOT"'
alias epdev='cd "$EASYPOST_PROJECT_ROOT" && make dev'
alias eptest='cd "$EASYPOST_PROJECT_ROOT" && make test-fast'
alias epcheck='cd "$EASYPOST_PROJECT_ROOT" && make check'
alias epclean='cd "$EASYPOST_PROJECT_ROOT" && make clean'
alias epmake='cd "$EASYPOST_PROJECT_ROOT" && make'

# Quick workflow aliases
alias ep-morning='cd "$EASYPOST_PROJECT_ROOT" && make clean && make test-fast && make dev'
alias ep-commit='cd "$EASYPOST_PROJECT_ROOT" && make format && make lint && make test-fast'
alias ep-push='cd "$EASYPOST_PROJECT_ROOT" && make check && make sync && make push'
alias ep-release='cd "$EASYPOST_PROJECT_ROOT" && make clean && make check && make benchmark && make build'

# Health check function
ep-health() {
    cd "$EASYPOST_PROJECT_ROOT" && make health
}

# Quick commit and push function
ep-qcp() {
    if [ -z "$1" ]; then
        echo "Usage: ep-qcp \"commit message\""
        return 1
    fi
    cd "$EASYPOST_PROJECT_ROOT" && make qcp m="$1"
}

# Database reset with confirmation
ep-db-reset() {
    echo "⚠️  This will destroy all database data!"
    read -p "Are you sure? (yes/no): " confirm
    if [ "$confirm" = "yes" ]; then
        cd "$EASYPOST_PROJECT_ROOT" && make db-reset
    else
        echo "Cancelled."
    fi
}

# Run specific test file
ep-test-file() {
    if [ -z "$1" ]; then
        echo "Usage: ep-test-file <path-to-test-file>"
        return 1
    fi
    cd "$EASYPOST_PROJECT_ROOT/backend" && source venv/bin/activate && pytest "$1" -v
}

# Backend shell with venv activated
ep-shell() {
    cd "$EASYPOST_PROJECT_ROOT/backend" && source venv/bin/activate && exec $SHELL
}

# Show available commands
ep-help() {
    echo "🚀 EasyPost MCP Shell Integration"
    echo ""
    echo "Navigation:"
    echo "  ep                - Go to project root"
    echo ""
    echo "Development:"
    echo "  epdev             - Start backend + frontend"
    echo "  eptest            - Run fast tests"
    echo "  epcheck           - Run quality checks"
    echo "  epclean           - Clean artifacts"
    echo "  epmake <target>   - Run make command"
    echo ""
    echo "Workflows:"
    echo "  ep-morning        - Morning routine (clean + test + dev)"
    echo "  ep-commit         - Pre-commit checks (format + lint + test)"
    echo "  ep-push           - Pre-push validation (check + sync + push)"
    echo "  ep-release        - Pre-release pipeline (full validation)"
    echo ""
    echo "Functions:"
    echo "  ep-health         - Check server health"
    echo "  ep-qcp \"message\"  - Quick commit + push"
    echo "  ep-db-reset       - Reset database (with confirmation)"
    echo "  ep-test-file <f>  - Run specific test file"
    echo "  ep-shell          - Open shell with backend venv"
    echo "  ep-help           - Show this help"
    echo ""
    echo "Or run: cd $EASYPOST_PROJECT_ROOT && make help"
}

# Print activation message
echo "✅ EasyPost MCP shell integration loaded"
echo "   Run 'ep-help' for available commands"

