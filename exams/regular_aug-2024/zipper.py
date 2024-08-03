import os.path
import zipfile

# specify folders to add
folders_names = [
    'main_app', 'orm_skeleton'
]

# specify files to add
files_names = [
    'caller.py', 'manage.py', 'requirements.txt'
]

current_dir = os.path.dirname(os.path.abspath(__file__))
filename = 'output.zip'

filepath = os.path.join(current_dir, filename)

# check if output.zip exists and deletes it
if os.path.exists(filepath):
    os.remove(filepath)

# zips files and folders
with zipfile.ZipFile(filepath, 'w') as zipf:
    for root, dirs, files in os.walk(
            f'../{os.path.basename(os.getcwd())}'):  # using os.walk() to pass recursively through folders
        for file in files:
            if dirs == folders_names and file not in files_names:
                continue
            full_path = os.path.join(root, file)
            if '__pycache__' in full_path:
                continue
            relative_path = os.path.relpath(full_path, os.path.commonpath(['.', full_path]))
            zipf.write(full_path, arcname=relative_path)

print('output.zip created')
