import os
import json
import requests
from datetime import datetime
from pathlib import Path
import csv

CONFIG_DIR = Path('./')
CONFIG_FILE = CONFIG_DIR / 'config.json'

def load_config():
    """Load configuration from file."""
    try:
        with open(CONFIG_FILE) as f:
            config = json.load(f)
            token = config.get('todoist_token', '').strip()
            if not token:
                raise ValueError("No token found in config file or token is empty")
            return {'todoist_token': token}
    except Exception as e:
        print("Error loading config:", str(e))
        raise

def get_projects(api_token):
    """Fetch all Todoist projects."""
    url = "https://api.todoist.com/rest/v2/projects"
    headers = {
        "Authorization": "Bearer {}".format(api_token),
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    projects = response.json()
    return {str(project['id']): project['name'] for project in projects}

def get_sections(api_token):
    """Fetch all Todoist sections."""
    url = "https://api.todoist.com/rest/v2/sections"
    headers = {
        "Authorization": "Bearer {}".format(api_token),
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    sections = response.json()
    return {str(section['id']): section['name'] for section in sections}

def get_completed_tasks(api_token):
    """Fetch all completed Todoist tasks."""
    url = "https://api.todoist.com/sync/v9/completed/get_all"
    headers = {"Authorization": "Bearer {}".format(api_token)}
    all_tasks = []
    offset = 0
    last_item_count = None
    
    while True:
        params = {
            "limit": 200,
            "offset": offset
        }
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        items = data.get('items', [])
        current_count = len(items)
        
        if current_count == 0 or current_count == last_item_count:
            break
            
        all_tasks.extend(items)
        offset += current_count
        last_item_count = current_count
        print("Retrieved {} completed tasks...".format(len(all_tasks)))
    
    return all_tasks

def get_active_tasks(api_token):
    """Fetch all active Todoist tasks."""
    url = "https://api.todoist.com/rest/v2/tasks"
    headers = {
        "Authorization": "Bearer {}".format(api_token),
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    tasks = response.json()
    print("Retrieved {} active tasks...".format(len(tasks)))
    return tasks

def process_tasks(completed_tasks, active_tasks, project_map, section_map):
    """Process all tasks into a list for CSV export."""
    processed = []
    
    # Process completed tasks
    for task in completed_tasks:
        completed_date = datetime.fromisoformat(task['completed_at'].replace('Z', '+00:00'))
        section_id = str(task.get('section_id', ''))
        processed.append({
            'task': task['content'],
            'project_id': str(task['project_id']),
            'project_name': project_map.get(str(task['project_id']), 'Unknown Project'),
            'section_name': section_map.get(section_id, ''),
            'status': 'Completed',
            'completed_date': completed_date.strftime('%Y-%m-%d'),
            'completed_time': completed_date.strftime('%H:%M:%S'),
            'due_date': None,
            'priority': task.get('priority', 1),
            'labels': ','.join(task.get('labels', [])),
            'url': task.get('url', '')
        })
    
    # Process active tasks
    for task in active_tasks:
        due_date = None
        if task.get('due'):
            due_date = task['due'].get('date')
        
        section_id = str(task.get('section_id', ''))
        processed.append({
            'task': task['content'],
            'project_id': str(task['project_id']),
            'project_name': project_map.get(str(task['project_id']), 'Unknown Project'),
            'section_name': section_map.get(section_id, ''),
            'status': 'Active',
            'completed_date': None,
            'completed_time': None,
            'due_date': due_date,
            'priority': task.get('priority', 1),
            'labels': ','.join(task.get('labels', [])),
            'url': task.get('url', '')
        })
    
    return processed

def main():
    print("Todoist Task Exporter")
    print("--------------------")
    
    try:
        config = load_config()
        project_map = get_projects(config['todoist_token'])
        section_map = get_sections(config['todoist_token'])
        completed_tasks = get_completed_tasks(config['todoist_token'])
        active_tasks = get_active_tasks(config['todoist_token'])
        
        processed_tasks = process_tasks(completed_tasks, active_tasks, project_map, section_map)
        
        # Save to CSV file
        filename = "todoist_tasks_latest.csv"
        fieldnames = ['task', 'project_id', 'project_name', 'section_name', 'status', 
                     'completed_date', 'completed_time', 'due_date', 
                     'priority', 'labels', 'url']
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(processed_tasks)
        
        print("\nExport complete!")
        print("File saved as:", filename)
        print("Total tasks exported:", len(processed_tasks))
        print("- Completed tasks:", len(completed_tasks))
        print("- Active tasks:", len(active_tasks))
        
    except Exception as e:
        print("Error occurred:", str(e))
        raise

if __name__ == "__main__":
    main()