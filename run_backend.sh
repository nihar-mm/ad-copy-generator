#!/bin/bash
cd "$(dirname "$0")/server"
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
