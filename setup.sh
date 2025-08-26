#!/usr/bin/env bash
set -e
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
cp -n .env.example .env || true
echo "✅ Setup complete. Activate with: source .venv/bin/activate"
