from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os.path

SCOPES = ['https://www.googleapis.com/auth/tasks']

def create_grocery_list(grocery_items, tasklist_title="Grocery Shopping"):
    creds = None
    if os.path.exists('task_token.json'):
        creds = Credentials.from_authorized_user_file('task_token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('task_token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('tasks', 'v1', credentials=creds)

    # Create a task list
    tasklist_body = {'title': tasklist_title}
    try:
        tasklist_result = service.tasklists().insert(body=tasklist_body).execute()
        tasklist_id = tasklist_result['id']
        print(f"Task list '{tasklist_result['title']}' created with ID: {tasklist_id}")
    except Exception as e:
        print(f"Error creating task list: {e}")
        return

    # Create tasks within the task list, organized by category
    for category, items in grocery_items.items():
        # Create a parent task for the category
        try:
            parent_task_body = {'title': category.capitalize()}
            parent_task_result = service.tasks().insert(tasklist=tasklist_id, body=parent_task_body).execute()
            parent_task_id = parent_task_result['id']
        except Exception as e:
            print(f"Error creating parent task '{category}': {e}")
            continue

        # Create child tasks for each item in the category
        for item in items:
            try:
                task_body = {'title': item, 'parent': parent_task_id}
                service.tasks().insert(tasklist=tasklist_id, body=task_body).execute()
            except Exception as e:
                print(f"Error creating task '{item}': {e}")

    print("Grocery list tasks added successfully.")

if __name__ == '__main__':
    grocery_list_items = {
        "proteins": [
            "Chicken Breast (1.05 kg)",
            "Ground Beef (1.05 kg)",
            "Eggs (14)",
            "Protein Powder (for 7 shakes)"
        ],
        "carbohydrates": [
            "Sourdough Bread (294g)",
            "Brown Rice (700g)",
            "Sweet Potatoes (600g)",
            "Lentils (dry, for soup)",
            "Blackberry Jam"
        ],
        "vegetables": [
            "Broccoli (450g)",
            "Green Beans (600g)",
            "Mixed Stir-Fry Vegetables"
        ],
        "fats": [
            "Soy Sauce"
        ],
        "pantry": [
            "cooking oil"
        ]
    }

    create_grocery_list(grocery_list_items)