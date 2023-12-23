import json

_config: dict = None
_fp = None

def __generate_default_config():
    return {
        "video": {
            "width": 1080,
            "height": 1920,
            "fps": 30
        },
        "captions": {
            "font": "Arial",
            "font_size": 24
        },
        "text_gen": {
            "prompt": """Generate TikTok video scripts using the given prompt.
Example:

This boy has an incredible talent. His name is Jacob Mello.
[img:smiling boy giving a thumbs up]

They all laughed at him for eating powdered sugar because he could not afford granulated sugar for lunch.
[img:boy eating granulated sugar]

Little did they know what amazing talent he possessed.
[img:boy doing flossing dance]"""
        },
        "image_gen": {
            "width": 512,
            "height": 512
        },
        "speech_gen": {

        }
    }

def load(config_path: str = "config.json"):
    global _config, _fp
    try:
        _fp = open(config_path, "r+")
        _config = json.load(_fp)
    except FileNotFoundError:
        _fp = open(config_path, "w")
        _config = __generate_default_config()
        json.dump(_config, _fp, indent=4)
    
def get_value(key: str):
    global _config
    if _config is None:
        load()
    return _config[key]

def set_value(key: str, value):
    global _config
    if _config is None:
        load()
    _config[key] = value
    json.dump(_config, _fp, indent=4)