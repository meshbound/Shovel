from config import load_config
from generate_video import generate_video
from video.composer import patch_video
from video.upload import write_video

config = load_config()
video = generate_video(["test", "tags"])
patched = patch_video(config, video)
write_video(config, patched)

print(video)