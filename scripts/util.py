import os, os.path
import shutil
def copy_directory(source: str, destination: str):
    source_path = source.removesuffix("/")
    destination_path = os.path.join(destination, os.path.basename(source_path))
    if os.path.exists(destination_path):
        if os.path.isdir(destination_path):
            shutil.rmtree(destination_path)
        else:
            os.remove(destination_path)
    shutil.copytree(source_path, destination_path)