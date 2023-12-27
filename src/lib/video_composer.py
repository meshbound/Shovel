from lib.util import random_file_from_dir, get_subdir_path
from lib.config import get_config
from lib.video_outline import VideoOutline
from moviepy.video.fx import resize
from moviepy.editor import *
import random
import math

def patch_video(outline: VideoOutline) -> VideoFileClip:
    padding = float(get_config()["video"]["padding"])
    caption_chunks = int(get_config()["video"]["caption_chunks"])
    caption_speed = float(get_config()["video"]["caption_speed"])
    font = get_config()["video"]["font"]
    font_size = float(get_config()["video"]["font_size"])
    music_lead = float(get_config()["video"]["music_lead"])

    patched_duration = 0
    video_clips = []
    audio_clips = []

    for i in range (0, len(outline.shots)):
        s = outline.shots[i]
        duration = s.speech.duration + padding

        image = s.image.set_start(patched_duration)
        image = image.set_duration(duration)
        image = resize.resize(image, width=1080, height=1080)
        video_clips.append(image)
        
        words = s.text.split()
        wps = float(len(words)) / duration
        spw = 1.0 / wps
        twps = math.ceil(wps) * caption_chunks
        patched_caption_duration = 0
        while len(words) > 0:
            caption_duration = 0
            curr = []
            if len(words) - twps > 0:
                curr = words[:twps]
                words = words[twps:]
            else:
                caption_duration = 0.5
                curr = words
                words = []

            caption_duration += spw * len(curr) * 1.0 / caption_speed
            text = " ".join(curr)
            zoom_fun = lambda t: 1 / (1.0 + math.e**(-20.0*(t-0.2)))

            caption = TextClip(text, fontsize=font_size,
                                color="black", font=font, 
                                stroke_width=30, stroke_color="black")
            caption = caption.set_start(patched_duration + patched_caption_duration)
            caption = caption.set_duration(caption_duration)
            caption = resize.resize(caption, zoom_fun)
            caption = caption.set_position(("center", 1070))
            video_clips.append(caption)

            caption = TextClip(text, fontsize=font_size,
                                color="white", font=font)
            caption = caption.set_start(patched_duration + patched_caption_duration)
            caption = caption.set_duration(caption_duration)
            caption = resize.resize(caption, zoom_fun)
            caption = caption.set_position(("center", 1080))
            video_clips.append(caption)
            patched_caption_duration += caption_duration

        audio = s.speech.set_start(patched_duration)
        audio_clips.append(audio)
        patched_duration += duration

    backgrounds_path = get_subdir_path(get_config(), "background_assets")
    background_select = random_file_from_dir(backgrounds_path)
    background = ImageClip(f"{backgrounds_path}/{background_select}")
    video_clips.insert(0, background)

    bottoms_path = get_subdir_path(get_config(), "bottom_assets")
    bottom_select = random_file_from_dir(bottoms_path)
    if bottom_select != None:
        bottom = VideoFileClip(f"{bottoms_path}/{bottom_select}")
        bottom = bottom.subclip(random.randint(0, math.floor(bottom.duration) 
                                            - math.ceil(patched_duration)))
        bottom = bottom.set_position(("center",1080))
        bottom = resize.resize(bottom, width=1080, height=840)
        video_clips.insert(1, bottom)

    music_path = get_subdir_path(get_config(), "music_assets")
    music_select = random_file_from_dir(music_path)
    if music_select != None:
        music = AudioFileClip(f"{music_path}/{music_select}")
        music = music.subclip(music_lead, music_lead + patched_duration)
        audio_clips.append(music)

    patched = CompositeVideoClip(video_clips)
    patched.duration = patched_duration
    patched.audio = CompositeAudioClip(audio_clips)

    return patched
