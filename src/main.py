from lib.config import load_config
from lib.generate_video import generate_video
from lib.video_composer import patch_video
from lib.video_export import write_video

load_config()

video = generate_video(["dank", "ohio", "skibiditoilet"])
patched = patch_video(video)
write_video(patched)

print(video)