import os

list_of_files = [
    "data/raw/",
    "data/processed/",
    "models/model.pkl",
    "notebooks/eda.ipynb",
    "notebooks/model_training.ipynb",
    "src/data_fetch.py",
    "src/feature_generation.py",
    "src/model_training.py",
    "src/model_predict.py",
    "dvc.yaml",
    "params.yaml",
    "requirements.txt",
    "setup.py",
    ".github/workflows/ci.yml",
    "app.py"
]

for filepath in list_of_files:
    # Check if the path is a file or directory
    filedir, filename = os.path.split(filepath)
    
    # Create directories if they don't exist
    if filedir and not os.path.exists(filedir):
        os.makedirs(filedir)
        print(f"Created directory: {filedir}")
    
    # Create files if they don't exist
    if filename:
        # Create parent directories if they don't exist
        if filedir and not os.path.exists(filedir):
            os.makedirs(filedir)
            print(f"Created directory: {filedir}")
        
        # Create the file
        if not os.path.exists(filepath):
            with open(filepath, 'w') as f:
                # Optionally, write default content to the file
                print(f"Created file: {filepath}")
        else:
            print(f"File already exists: {filepath}")
    else:
        print(f"Directory already exists: {filepath}")
