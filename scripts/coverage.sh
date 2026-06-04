#!/usr/bin/env bash
set -euo pipefail

python -m pytest tests --cov=packages.core --cov-report=term --cov-report=html