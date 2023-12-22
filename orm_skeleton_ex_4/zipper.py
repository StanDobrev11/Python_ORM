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


# check if output.zip exists and deletes it
if os.path.exists('output.zip'):
    os.remove('output.zip')

# zips files and folders
with zipfile.ZipFile('output.zip', 'w') as zipf:
    for root, dirs, files in os.walk('.'):
        for file in files:
            if dirs == folders_names and file not in files_names:
                continue
            full_path = os.path.join(root, file)
            if '__pycache__' in full_path:
                continue
            relative_path = os.path.relpath(full_path, os.path.commonpath(['.', full_path]))
            zipf.write(full_path, arcname=relative_path)

print('Output file created')
