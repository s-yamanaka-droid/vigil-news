#!/bin/bash
# VIGIL 手動実行スクリプト
cd "$(dirname "$0")"
source ~/.zshrc 2>/dev/null
source venv/bin/activate
python pipeline/run.py "$@"
