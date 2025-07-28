#!/bin/bash

# Weather ETL Pipeline Runner Script
# This script runs the weather ETL pipeline for daily scheduling

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/weather_etl.py"
LOG_FILE="$SCRIPT_DIR/cron_runner.log"

# Change to script directory
cd "$SCRIPT_DIR"

# Add timestamp to log
echo "$(date '+%Y-%m-%d %H:%M:%S') - Starting weather ETL pipeline" >> "$LOG_FILE"

# Run the Python script
if command -v python3 &> /dev/null; then
    python3 "$PYTHON_SCRIPT" >> "$LOG_FILE" 2>&1
    exit_code=$?
elif command -v python &> /dev/null; then
    python "$PYTHON_SCRIPT" >> "$LOG_FILE" 2>&1
    exit_code=$?
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') - ERROR: Python not found" >> "$LOG_FILE"
    exit 1
fi

# Log completion status
if [ $exit_code -eq 0 ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Weather ETL pipeline completed successfully" >> "$LOG_FILE"
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Weather ETL pipeline failed with exit code $exit_code" >> "$LOG_FILE"
fi

exit $exit_code 