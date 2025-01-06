import pandas as pd
from plotnine import *
import matplotlib.pyplot as plt
import json
from pathlib import Path

CONFIG_DIR = Path('./')
CONFIG_FILE = CONFIG_DIR / 'config.json'

def load_config():
    """Load configuration from file."""
    try:
        with open(CONFIG_FILE) as f:
            config = json.load(f)
            return config
    except Exception as e:
        print("Error loading config:", str(e))
        raise

def create_visualization():
    # Read the CSV file
    df = pd.read_csv('todoist_tasks_latest.csv')
    
    # Filter for completed tasks only
    completed_tasks = df[df['status'] == 'Completed']

    # Load config and filter out specific projects
    config = load_config()
    projects_to_exclude = config.get('projects_to_exclude', [])
    completed_tasks = completed_tasks[~completed_tasks['project_name'].isin(projects_to_exclude)]
    
    # Count tasks by project
    project_counts = completed_tasks.groupby('project_name').size().reset_index()
    project_counts.columns = ['project_name', 'count']
    
    # Create the plot
    plot = (ggplot(project_counts, 
                   aes(x='reorder(project_name, count)', y='count', fill='project_name'))
            + geom_bar(stat='identity')
            + coord_flip()
            + theme_minimal()
            + theme(
                figure_size=(10, 6),
                plot_background=element_rect(fill="white"),
                panel_background=element_rect(fill="white")
            )
            + labs(title='Completed Tasks by Project',
                  x='Project',
                  y='Number of Completed Tasks')
    )
    
    # Save the plot
    plot.save('todoist_project_analysis.png', dpi=300, bbox_inches='tight')
    print("Visualization saved as: todoist_project_analysis.png")

if __name__ == "__main__":
    create_visualization()