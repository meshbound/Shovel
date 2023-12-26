from configobj import ConfigObj
import random
import os

def get_files_in_dir(dir_path: str) -> list[str]:
    files = [f for f in os.listdir(dir_path) 
             if os.path.isfile(dir_path + "/" + f)]
    return files

def random_file_from_dir(dir_path: str) -> str:
    files = get_files_in_dir(dir_path)
    if len(files) == 0:
        return None
    file_select = files[random.randint(0, len(files) - 1)]
    return file_select

def get_subdir_path(config: ConfigObj, subfolder: str) -> str:
    return config["dirs"]["root"] + config["dirs"]["sub_dirs"][subfolder]
