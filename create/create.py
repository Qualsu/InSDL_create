import tempfile
import requests
import os
import zipfile
import shutil
import create.config as config

def create_project(project_name, vsc_keep=False, bat_keep=False):
    try:
        os.makedirs(project_name, exist_ok=True)
        original_dir = os.getcwd()
        os.chdir(project_name)
        
        print("Create project...")
        response = requests.get(config.ARCHIVE_URL, stream=True)
        response.raise_for_status()
        
        with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as tmp_file:
            for chunk in response.iter_content(chunk_size=8192):
                tmp_file.write(chunk)
            tmp_path = tmp_file.name
        
        with zipfile.ZipFile(tmp_path, 'r') as zip_ref:
            zip_ref.extractall(".")
        
        os.unlink(tmp_path)
        
        if not vsc_keep:
            vscode_dir = os.path.join(os.getcwd(), ".vscode")
            if os.path.exists(vscode_dir):
                shutil.rmtree(vscode_dir)
        
        if not bat_keep:
            bat_path = os.path.join(os.getcwd(), "compile.bat")
            if os.path.exists(bat_path):
                os.remove(bat_path)
        
        os.chdir(original_dir)
        print(f"Project '{project_name}' created successful!")
    
    except Exception as e:
        print(f"Created error: {e}")
        os.chdir(original_dir)