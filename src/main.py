from generate_video import generate_video
from video.composer import patch_video
from video.upload import write_video

video = generate_video(["test", "tags"])
patched = patch_video(video)
write_video(patched)

print(video)