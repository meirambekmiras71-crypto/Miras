import os
from pathlib import Path

base_path = Path("test_directory/level1/level2")
base_path.mkdir(parents=True, exist_ok=True)

Path("test_directory/document.txt").touch()
Path("test_directory/level1/image.png").touch()
Path("test_directory/level1/notes.txt").touch()

for root, dirs, files in os.walk("test_directory"):
    print(root)
    
    for d in dirs:
        print(f"  {d}/")
        
    for f in files:
        print(f"  {f}")