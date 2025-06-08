#!/bin/sh
# check_format.sh - Run formatting and lint checks for the project.
#
# This script runs flake8 and black on Python directories and
# shellcheck on all shell scripts. It exits with a non-zero status if
# any of the tools report an error.

# Exit immediately if a command exits with a non-zero status.
set -e

# Directories containing Python code to check. Add more directories as needed.
PY_DIRS="scripts tools releasetools"

# Build a list of existing directories to avoid errors.
EXISTING_PY_DIRS=""
for dir in $PY_DIRS; do
    if [ -d "$dir" ]; then
        EXISTING_PY_DIRS="$EXISTING_PY_DIRS $dir"
    fi
done

# Run Python linters and formatters when directories are present.
if [ -n "$EXISTING_PY_DIRS" ]; then
    echo "Running flake8 on:$EXISTING_PY_DIRS"
    flake8 $EXISTING_PY_DIRS

    echo "Running black --check on:$EXISTING_PY_DIRS"
    black --check $EXISTING_PY_DIRS
fi

# Find all shell scripts and run shellcheck on them.
# The find command searches the entire repository for files ending in .sh.
if command -v shellcheck >/dev/null 2>&1; then
    echo "Running shellcheck on all shell scripts"
    find . -name '*.sh' -print0 | xargs -0 shellcheck
else
    echo "shellcheck not found" >&2
    exit 1
fi
