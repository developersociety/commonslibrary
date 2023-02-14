#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

python -m pip install setuptools==59.8.0
exec python -m pip install "$@"
