import lib.config as config
from lib.generate_video import generate_video

config.load()

video = generate_video(["dank", "ohio", "skibiditoilet"])
print(video)