import os
import shutil

def delete_project(project_name):
    try:
        target_path = os.path.join(os.getcwd(), project_name)
        if os.path.exists(target_path):
            print(f"Delete project '{project_name}'...")
            shutil.rmtree(target_path)
            print("Project delete successful!")
        else:
            print(f"Project '{project_name}' not found!")
    except Exception as e:
        print(f"Deleted error: {e}")