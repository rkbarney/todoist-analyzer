# Todoist Task Analyzer

## Overview

The Todoist Task Analyzer is a tool designed to export, process, and visualize tasks from Todoist. It helps users analyze their completed and active tasks, providing insights into their productivity and task management.

## Features

- **Data Export**: Extracts completed and active tasks from Todoist.
- **Data Processing**: Processes the exported tasks to generate meaningful insights.
- **Visualization**: Creates visual representations of the task data for easy analysis.

## Prerequisites

- Python 3.x
- Todoist API Token

## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Create a config.json file with your Todoist API token and a list of projects you don't want to include (if any):
    ```json
    {
        "todoist_token": "your_todoist_api_token",
        "projects_to_exclude": [
            "PROJECT1",
            "PROJECT2",
            "PROJECT3"
    ]
    }
    ```

## Usage

1. Run the analysis script:
    ```sh
    ./analyze_todoist.sh
    ```

2. The script will perform the following steps:
    - Export Todoist data to todoist_tasks_latest.csv
    - Create visualizations and save them as todoist_project_analysis.png



## Files

- analyze_todoist.sh: Shell script to run the data export and visualization.
- todoist_export.py: Python script to export tasks from Todoist.
- todoist_visualize.py: Python script to create visualizations from the exported data.
- config.json: Configuration file containing the Todoist API token.
- todoist_tasks_latest.csv: CSV file containing the latest exported tasks.
- todoist_project_analysis.png: PNG file containing the visualized task data.

## Example Output

After running the analysis script, you will get the following files:
- todoist_tasks_latest.csv: Contains the exported tasks with details such as task name, project ID, status, completion date, etc.
- todoist_project_analysis.png: Visual representation of the task data.
![Completed Tasks by Project](todoist_project_analysis.png)

## Conclusion

The Todoist Task Analyzer is a powerful tool for anyone looking to gain insights into their task management and productivity. By exporting, processing, and visualizing Todoist tasks, users can better understand their task patterns and improve their productivity.

For more details, check out the source code and documentation in the repository. Happy analyzing!

To learn more about the author Richard Barney visit: https://www.richardbarneyresearch.com/ for data and data science needs or if you are in for a laugh check out my comedy at https://www.richardbarney.com/.