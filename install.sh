#!/usr/bin/env bash
# install.sh — bootstrap for Chinnu-Claude-setup
# Usage (local):  ./install.sh [flags]
# Usage (remote): curl -fsSL https://raw.githubusercontent.com/YOUR-ORG/Chinnu-Claude-setup/main/install.sh | bash
set -euo pipefail

REPO_URL="https://github.com/YOUR-ORG/Chinnu-Claude-setup"
CLONE_DIR="${HOME}/.chinnu-claude-setup"

# ── OS check ──────────────────────────────────────────────────────────────
OS="$(uname -s)"
case "${OS}" in
    Linux|Darwin) ;;
    *)
        echo "ERROR: Unsupported OS '${OS}'. On Windows, use WSL." >&2
        exit 1
        ;;
esac

# ── Python 3.8+ check ────────────────────────────────────────────────────
if ! command -v python3 >/dev/null 2>&1; then
    echo "ERROR: python3 is required but was not found." >&2
    case "${OS}" in
        Darwin) echo "  Install: brew install python3" >&2 ;;
        Linux)  echo "  Install: sudo apt-get install python3  (or distro equivalent)" >&2 ;;
    esac
    exit 1
fi

PY_MAJOR=$(python3 -c "import sys; print(sys.version_info.major)")
PY_MINOR=$(python3 -c "import sys; print(sys.version_info.minor)")
PY_VER="${PY_MAJOR}.${PY_MINOR}"

if [ "${PY_MAJOR}" -lt 3 ] || { [ "${PY_MAJOR}" -eq 3 ] && [ "${PY_MINOR}" -lt 8 ]; }; then
    echo "ERROR: Python 3.8+ required (found ${PY_VER})." >&2
    exit 1
fi

# ── Local vs curl|bash detection ─────────────────────────────────────────
# When run via curl | bash, BASH_SOURCE[0] may be empty or "bash"; the
# directory will not contain bin/claude-setup.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-"."}")" 2>/dev/null && pwd || echo "")"

if [ -f "${SCRIPT_DIR}/bin/claude-setup" ]; then
    # Running from inside a local clone
    REPO_DIR="${SCRIPT_DIR}"
else
    # curl | bash path — need git
    if ! command -v git >/dev/null 2>&1; then
        echo "ERROR: git is required for remote install. Please install git and retry." >&2
        exit 1
    fi

    if [ -d "${CLONE_DIR}/.git" ]; then
        echo "Updating existing clone at ${CLONE_DIR}..."
        git -C "${CLONE_DIR}" pull --ff-only
    else
        echo "Cloning ${REPO_URL} into ${CLONE_DIR}..."
        git clone "${REPO_URL}" "${CLONE_DIR}"
    fi

    REPO_DIR="${CLONE_DIR}"
fi

echo "Using repo at: ${REPO_DIR}"
exec python3 "${REPO_DIR}/bin/claude-setup" install "$@"
