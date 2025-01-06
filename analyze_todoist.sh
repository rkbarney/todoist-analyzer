#!/bin/bash

# Todoist Analysis Script
echo "Starting Todoist Analysis..."

# Navigate to script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Run data export
echo "Exporting Todoist data..."
python3 todoist_export.py
if [ $? -ne 0 ]; then
    echo "Error: Data export failed"
    exit 1
fi

# Run visualization
echo "Creating visualization..."
python3 todoist_visualize.py
if [ $? -ne 0 ]; then
    echo "Error: Visualization failed"
    exit 1
fi

echo "Analysis complete!"
echo "Results saved as:"
echo "- todoist_tasks_latest.csv"
echo "- todoist_project_analysis.png"