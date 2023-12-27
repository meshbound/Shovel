from lib.util import random_file_from_dir, get_subdir_path
from lib.config import get_config
from lib.video_outline import VideoOutline
from moviepy.video.fx import resize
from moviepy.editor import *
import random
import math

def patch_video(outline: VideoOutline) -> VideoFileClip:
    padding = float(get_config()["video"]["padding"])
    chunks = int(get_config()["video"]["max_caption_chunks"])

    patched_duration = 0
    video_clips = []
    audio_clips = []

    for i in range (0, len(outline.shots)):
        s = outline.shots[i]
        duration = s.speech.duration + padding
        patched_duration += duration

        image = s.image.set_start(duration * i)
        image = image.set_duration(duration)
        image = resize.resize(image, width=1080, height=1080)
        video_clips.append(image)
        
        words = s.text.split()
        wps = math.ceil(len(words) / duration)
        twps = wps * chunks
        captions_count = 0
        while len(words) > 0:
            curr = []
            x = 0
            if len(words) - twps >= 0:
                curr = words[:twps]
                words = words[twps:]
            else:
                curr = words
                words = []

            text = " ".join(curr)
            zoom_fun = lambda t: 1 / (1.0 + math.e**(-20.0*(t-0.2)))

            caption = TextClip(text, fontsize=50,
                                color="black", font="Arial-bold", 
                                stroke_width=30, stroke_color="black")
            caption = caption.set_start(duration * i + captions_count * chunks)
            caption = caption.set_duration(chunks)
            caption = resize.resize(caption, zoom_fun)
            caption = caption.set_position(("center", 1070))
            video_clips.append(caption)

            caption = TextClip(text, fontsize=50,
                                color="white", font="Arial-bold")
            caption = caption.set_start(duration * i + captions_count * chunks)
            caption = caption.set_duration(chunks)
            caption = resize.resize(caption, zoom_fun)
            caption = caption.set_position(("center", 1080))
            video_clips.append(caption)
            captions_count += 1

        audio = s.speech.set_start(duration * i)
        audio_clips.append(audio)

    backgrounds_path = get_subdir_path(get_config(), "assets_background")
    background_select = random_file_from_dir(backgrounds_path)
    background = ImageClip(backgrounds_path + "/" + background_select)
    video_clips.insert(0, background)

    bottoms_path = get_subdir_path(get_config(), "assets_bottom")
    bottom_select = random_file_from_dir(bottoms_path)
    if bottom_select != None:
        bottom = VideoFileClip(bottoms_path + "/" + bottom_select)
        bottom = bottom.subclip(random.randint(0, math.floor(bottom.duration) 
                                            - math.ceil(patched_duration)))
        bottom = bottom.set_position(("center",1080))
        bottom = resize.resize(bottom, width=1080, height=840)
        video_clips.insert(1, bottom)

    patched = CompositeVideoClip(video_clips)
    patched.duration = patched_duration
    patched.audio = CompositeAudioClip(audio_clips)

    return patched
