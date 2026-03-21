import shutil
from pathlib import Path

source_dir = Path("test_directory")
archive_dir = Path("archive_directory")

archive_dir.mkdir(exist_ok=True)

txt_files = list(source_dir.rglob("*.txt"))

for file_path in txt_files:
    print(file_path)

for file_path in txt_files:
    destination = archive_dir / file_path.name
    shutil.copy(file_path, destination)

png_files = list(source_dir.rglob("*.png"))

for file_path in png_files:
    destination = archive_dir / file_path.name
    shutil.move(file_path, destination)