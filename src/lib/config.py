from lib.util import get_files_in_dir, get_subdir_path
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
        print("No config found, creating one...")
        write_default_config()
    _config = ConfigObj(_config_path)
    verify_file_structure()
    verify_assets()

def write_default_config():
    config = ConfigObj()
    config.filename = _config_path

    config["dirs"] = {}
    dirs = config["dirs"]
    dirs["stash_dirs"] = {}
    stash_dirs = dirs["stash_dirs"]
    stash_dirs["root"] = "./stash/"
    stash_dirs["video_out"] = "out"
    stash_dirs["background_assets"] = "assets/backgrounds"
    stash_dirs["overlay_assets"] = "assets/overlays"
    stash_dirs["bottom_assets"] = "assets/bottoms"
    stash_dirs["music_assets"] = "assets/music"
    stash_dirs["audio_temp"] = "tmp/audio"
    stash_dirs["image_temp"] = "tmp/image"
    dirs["auth_dirs"] = {}
    auth_dirs = dirs["auth_dirs"]
    auth_dirs["root"] = "./auth/"
    auth_dirs["youtube"] = "youtube"
    auth_dirs["google"] = "google"

    config["video"] = {}
    video = config["video"]
    video["framerate"] = 24
    video["padding"] = 0.2
    video["caption_chunks"] = 2
    video["caption_speed"] = 1.4
    video["font"] = "Arial-bold"
    video["font_size"] = 50
    video["music_lead"] = 10

    config["upload"] = {}
    upload = config["video"]

    config["text_gen"] = {}
    text_gen = config["text_gen"]
    text_gen["prompt"] = """Generate TikTok video scripts using the given prompt.
Example:

This boy has an incredible talent. His name is Jacob Mello.
[img:smiling boy giving a thumbs up]

They all laughed at him for eating powdered sugar because he could not afford granulated sugar for lunch.
[img:boy eating granulated sugar]

Little did they know what amazing talent he possessed.
[img:boy doing flossing dance]"""
    text_gen["api_key"] = ""
    text_gen["model"] = ""
    text_gen["temperature"] = 0.25
    text_gen["max_length"] = 256

    config["image_gen"] = {}
    image_gen = config["image_gen"]
    image_gen["width"] = 512
    image_gen["height"] = 512
    image_gen["api_key"] = ""

    config["speech_gen"] = {}

    config.write()

def verify_file_structure():
    for dir in _config["dirs"]:
        root = _config["dirs"][dir]["root"]
        for subdir in _config["dirs"][dir]:
            if subdir == "root":
                continue
            dir_path = root + _config["dirs"][dir][subdir]
            if not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)

def verify_assets():
    backgrounds_path = get_subdir_path(_config, "background_assets")
    background_files = get_files_in_dir(backgrounds_path)
    valid_backgrounds = len(background_files)
    for f in background_files:
        file_path = backgrounds_path + "/" + f
        i = Image.open(file_path)
        if i.size[0] != 1080 or i.size[1] != 1920:
            print(f"[WARN]\tBackground {f} has illegal size! Moving...")
            i.close()
            if not os.path.exists(backgrounds_path + "/bad/"):
                os.mkdir(backgrounds_path + "/bad/")
            os.replace(file_path, backgrounds_path + "/bad/" + f)
            valid_backgrounds -= 1
    if valid_backgrounds == 0:
        print("Generating blank background...")
        image = Image.new('RGB', (1080, 1920), (256,256,256))
        image.save(backgrounds_path + "/blank.png")
