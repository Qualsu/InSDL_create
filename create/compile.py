import os
import create.config as config

def compile_project(project_name):
    try:
        original_dir = os.getcwd()
        project_path = os.path.join(original_dir, project_name)
        
        if not os.path.exists(project_path):
            print(f"Project '{project_name}' not found!")
            return
        
        os.chdir(project_path)
        print(f"Compile '{project_name}'...")
        print(f"Command: {config.COMPILE_COMMAND}")
        os.system(config.COMPILE_COMMAND)
        os.chdir(original_dir)
    except Exception as e:
        print(f"Compiled error: {e}")
        os.chdir(original_dir)