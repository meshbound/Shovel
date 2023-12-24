from util import get_files_in_dir, get_subdir_path, to_imageclip
from generation.script_gen.outline import VideoOutline
from configobj import ConfigObj
from moviepy.editor import *
from PIL import Image
import math
import random

def patch_video(outline: VideoOutline, config: ConfigObj) -> VideoFileClip:
    backgrounds_path = get_subdir_path(config, "assets_background")
    background_files = get_files_in_dir(backgrounds_path)
    background_select = background_files[random.randint(0, len(background_files) - 1)]
    background = to_imageclip(Image.open(backgrounds_path + "/" + background_select))

    padding = float(config["video"]["padding"])
    chunks = float(config["video"]["max_caption_chunks"])

    patched_duration = 0
    video_clips = []
    audio_clips = []

    video_clips.append(background)

    for i in range (0, len(outline.shots)):
        s = outline.shots[i]
        duration = s.speech.duration + padding
        patched_duration += duration

        image = s.image.set_start(duration * i)
        image = image.set_duration(duration)
        video_clips.append(image)

        words = s.text.split()
        wps = math.ceil(len(words) / duration)
        twps = wps * chunks
        while len(words) > 0:
            curr = []
            if len(words) - twps < 0:
                curr = words[:twps]
                words = words[twps:]
            else:
                curr = words
                words = []
            
            text = " ".join(curr)
            caption = TextClip(text, fontsize = 20, 
                                color = 'black', font="Amiri-Bold")
            caption = caption.set_start(duration * i)
            caption = caption.set_duration(chunks)
            caption = caption.set_position(("center","bottom"))
            video_clips.append(caption)

        audio = s.speech.set_start(duration * i)
        audio_clips.append(audio)

    patched = CompositeVideoClip(video_clips)
    patched.duration = patched_duration
    patched.audio = CompositeAudioClip(audio_clips)

    return patched
