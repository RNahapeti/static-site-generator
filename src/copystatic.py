import os
import shutil

def copy_files_recursive(from_dir, to_dir):
    for item in os.listdir(from_dir):
        from_path = os.path.join(from_dir, item)
        to_path = os.path.join(to_dir, item)

        if os.path.isfile(from_path):
            shutil.copy(from_path, to_path)
        else:
            os.mkdir(to_path)
            copy_files_recursive(from_path, to_path)

def setup_public_dir(src_path, path_to_public):
    if os.path.exists(path_to_public):
        shutil.rmtree(path_to_public)
    os.mkdir(path_to_public)
    copy_files_recursive(src_path, path_to_public)