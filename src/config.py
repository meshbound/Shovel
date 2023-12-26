from util import get_files_in_dir, get_subdir_path
from configobj import ConfigObj
from PIL import Image
import os

_config_path = "./shovel.ini"
_config = None

def get_config():
    if _config == None:
        load_config()
    return _config

def load_config():
    global _config
    if not os.path.exists(_config_path):
        print("No config found!")
        write_default_config()
    _config = ConfigObj(_config_path)
    verify_file_structure()
    verify_assets()

def write_default_config():
    print("Writing new config...")
    config = ConfigObj()
    config.filename = _config_path

    config["dirs"] = {}
    dirs = config["dirs"]
    dirs["root"] = "./stash/"
    dirs["sub_dirs"] = {}
    sub_dirs = dirs["sub_dirs"]
    sub_dirs["video_out"] = "out"
    sub_dirs["assets_background"] = "backgrounds"
    sub_dirs["assets_overlay"] = "overlays"
    sub_dirs["assets_bottom"] = "bottoms"
    sub_dirs["assets_sfx"] = "sfx"

    config["video"] = {}
    video = config["video"]
    video["padding"] = 0.2
    video["max_caption_chunks"] = 2

    config.write()

def verify_file_structure():
    root = _config["dirs"]["root"]
    if not os.path.exists(root):
        os.mkdir(root)
    sub_dirs = _config["dirs"]["sub_dirs"]
    for sub_dir in sub_dirs:
        dir_path = root + sub_dirs[sub_dir]
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

def verify_assets():
    backgrounds_path = get_subdir_path(_config, "assets_background")
    background_files = get_files_in_dir(backgrounds_path)
    valid_backgrounds = len(background_files)
    for f in background_files:
        file_path = backgrounds_path + "/" + f
        i = Image.open(file_path)
        if i.size[0] != 1080 or i.size[1] != 1920:
            print("[WARN]\tBackground " + f + " has illegal size! Moving...")
            i.close()
            if not os.path.exists(backgrounds_path + "/bad/"):
                os.mkdir(backgrounds_path + "/bad/")
            os.replace(file_path, backgrounds_path + "/bad/" + f)
            valid_backgrounds -= 1
    if valid_backgrounds == 0:
        print("Generating blank background...")
        image = Image.new('RGB', (1080, 1920), (256,256,256))
        image.save(backgrounds_path + "/blank.png")
