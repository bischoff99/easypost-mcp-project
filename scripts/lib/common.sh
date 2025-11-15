#!/usr/bin/env zsh
# Shared utilities for scripts
# Source this file in scripts:
#   For scripts in scripts/dev/, scripts/test/, scripts/utils/: source "$(dirname "$0")/../lib/common.sh"
#   For scripts in scripts/ root: source "$(dirname "$0")/lib/common.sh"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get project root (works from any script location)
get_project_root() {
  local script_path="${1:-${(%):-%x}}"
  local script_dir="$(cd "$(dirname "$script_path")" && pwd)"

  # If we're in a subdirectory (dev/, test/, utils/, python/), go up two levels
  # If we're in scripts/ root, go up one level
  if [[ "$script_dir" == *"/scripts/dev" ]] || \
     [[ "$script_dir" == *"/scripts/test" ]] || \
     [[ "$script_dir" == *"/scripts/utils" ]] || \
     [[ "$script_dir" == *"/scripts/python" ]]; then
    echo "$(cd "$script_dir/../.." && pwd)"
  else
    echo "$(cd "$script_dir/.." && pwd)"
  fi
}

# Get scripts directory
get_scripts_dir() {
  local project_root=$(get_project_root "${(%):-%x}")
  echo "${project_root}/scripts"
}

# Get Python scripts directory
get_python_scripts_dir() {
  local scripts_dir=$(get_scripts_dir)
  echo "${scripts_dir}/python"
}

# Port configuration with defaults
BACKEND_PORT=${BACKEND_PORT:-8000}

# Check virtual environment exists
check_venv() {
  local backend_dir="${1:-$(get_project_root "${(%):-%x}")}"
  if [ -d "${backend_dir}/.venv" ]; then
    echo "${backend_dir}/.venv"
    return 0
  elif [ -d "${backend_dir}/venv" ]; then
    echo "${backend_dir}/venv"
    return 0
  else
    echo -e "${RED}ERROR: Virtual environment not found in ${backend_dir}${NC}" >&2
    echo "Run: make setup" >&2
    return 1
  fi
}

# Check Docker is running
check_docker() {
  if ! docker info >/dev/null 2>&1; then
    echo -e "${RED}ERROR: Docker Desktop not running${NC}" >&2
    echo "Please start Docker Desktop first" >&2
    return 1
  fi
  return 0
}

# Error exit with message
error_exit() {
  echo -e "${RED}ERROR: $1${NC}" >&2
  exit 1
}

# Success message
success_msg() {
  echo -e "${GREEN}✅ $1${NC}"
}

# Info message
info_msg() {
  echo -e "${BLUE}ℹ️  $1${NC}"
}

# Warning message
warning_msg() {
  echo -e "${YELLOW}⚠️  $1${NC}"
}

# Activate virtual environment
activate_venv() {
  local backend_dir="${1:-$(get_project_root "${(%):-%x}")}"
  local venv_path=$(check_venv "$backend_dir")
  if [ $? -ne 0 ]; then
    return 1
  fi
  source "${venv_path}/bin/activate"
  return 0
}

# Install dependencies (standardized)
install_dependencies() {
  local backend_dir="${1:-$(get_project_root "${(%):-%x}")}"
  pushd "$backend_dir" >/dev/null || return 1

  info_msg "Installing dependencies..."
  pip install -U pip setuptools wheel || return 1
  if [ -f "${backend_dir}/config/requirements.txt" ]; then
    pip install -r "${backend_dir}/config/requirements.txt" || return 1
  fi

  popd >/dev/null
  return 0
}

# Get MCP tool path
get_mcp_tool_path() {
  local python_scripts_dir=$(get_python_scripts_dir)
  echo "${python_scripts_dir}/mcp_tool.py"
}

# Call MCP tool (helper function)
mcp_tool() {
  local tool_name="$1"
  shift
  local project_root=$(get_project_root "${(%):-%x}")
  local backend_dir="${project_root}"
  local venv_path=$(check_venv "$backend_dir") || return 1
  local venv_bin="${venv_path}/bin"
  local mcp_tool_path=$(get_mcp_tool_path)
  "${venv_bin}/python" "$mcp_tool_path" "$tool_name" "$@"
}
