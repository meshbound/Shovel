import config
from generate_video import generate_video

config.load()

video = generate_video(["test", "tags"])
print(video)