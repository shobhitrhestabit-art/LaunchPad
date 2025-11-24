#!/bin/bash
# Validate script for CI pre-commit and cron use

LOG_FILE="logs/validate.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

mkdir -p logs

echo "[$TIMESTAMP] Running validation..." | tee -a "$LOG_FILE"

# 1. Check src/ directory exists
if [ ! -d "src" ]; then
  echo "[$TIMESTAMP] ❌ Error: src/ directory missing!" | tee -a "$LOG_FILE"
  exit 1
fi

# 2. Check config.json validity
if ! jq empty config.json 2>/dev/null; then
  echo "[$TIMESTAMP] ❌ Error: config.json is invalid JSON!" | tee -a "$LOG_FILE"
  exit 1
fi

echo "[$TIMESTAMP] Validation passed!" | tee -a "$LOG_FILE"
