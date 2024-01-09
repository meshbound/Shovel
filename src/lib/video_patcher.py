from lib.util import random_file_from_dir, get_subdir_path
from lib.config import get_config
from lib.audio_silence import get_silence
from lib.video_text import text_to_image
from lib.video_outline import VideoOutline
from moviepy.video.fx import resize, loop
from moviepy.editor import *
import random
import math

def patch_video(outline: VideoOutline) -> VideoFileClip:
    padding = float(get_config()["video"]["padding"])
    caption_chunks = int(get_config()["video"]["caption_chunks"])
    caption_speed = float(get_config()["video"]["caption_speed"])
    caption_steal = int(get_config()["video"]["caption_steal"])
    font_name = get_config()["video"]["font_name"]
    font_size = int(get_config()["video"]["font_size"])
    font_color = get_config()["video"]["font_color"]
    outline_ratio = float(get_config()["video"]["outline_ratio"])
    outline_color = get_config()["video"]["outline_color"]
    music_lead = float(get_config()["video"]["music_lead"])

    patched_duration = 0
    video_clips = []
    audio_clips = []

    for i in range (0, len(outline.shots)):
        
        s = outline.shots[i]
        speech = s.speech
        image = s.image
        text = s.text

        silence_start, silence_end = get_silence(speech)
        duration = speech.duration + padding

        image = image.set_start(patched_duration)
        image = image.set_duration(duration)
        image = resize.resize(image, width=1080, height=1080)
        video_clips.append(image)
        
        words = text.split()
        trimmed_duration = speech.duration - (silence_start + silence_end)
        wps = float(len(words)) / trimmed_duration
        spw = 1.0 / wps
        twps = math.ceil(wps) * caption_chunks
        patched_caption_duration = silence_start
        last_ended = True
        while len(words) > 0:
            curr = []
            ended = True
            if len(words) - twps > 0:
                actual, ended = grab_until_ending(words, twps)
                stolen, ended = ((0, True) if ended
                          else grab_until_ending(words[actual:], caption_steal))
                if not ended:
                    stolen = 0
                curr = words[:actual + stolen]
                words = words[stolen + actual:]
            else:
                curr = words
                words = []

            caption_duration = (spw * len(curr) * 1.0 / (caption_speed if not ended else 1.0))
            caption_text = " ".join(curr)
            zoom_fun = lambda t: 1 / (1.0 + math.e**(-20.0*(t-0.2)))

            caption = text_to_image(text=caption_text, font_size=font_size, font_name=font_name,
                                    font_color=font_color, outline_ratio=outline_ratio,
                                    outline_color=outline_color)
            caption = caption.set_start(patched_duration + patched_caption_duration)
            caption = caption.set_duration(caption_duration)
            if last_ended:
                
                caption = resize.resize(caption, zoom_fun)
            caption = caption.set_position(("center", 1040))
            video_clips.append(caption)
            
            patched_caption_duration += caption_duration
            last_ended = ended

        audio = speech.set_start(patched_duration)
        audio_clips.append(audio)
        patched_duration += duration

    overlays_path = get_subdir_path(get_config(), "overlay_assets")
    overlay_select = random_file_from_dir(overlays_path)
    overlay = ImageClip(f"{overlays_path}/{overlay_select}")
    video_clips.append(overlay)

    backgrounds_path = get_subdir_path(get_config(), "background_assets")
    background_select = random_file_from_dir(backgrounds_path)
    background = ImageClip(f"{backgrounds_path}/{background_select}")
    video_clips.insert(0, background)

    bottoms_path = get_subdir_path(get_config(), "bottom_assets")
    bottom_select = random_file_from_dir(bottoms_path)
    if bottom_select != None:
        bottom = VideoFileClip(f"{bottoms_path}/{bottom_select}")
        bottom = bottom.subclip(random.randint(0, max(0, math.floor(bottom.duration) 
                                                      - math.ceil(patched_duration))))
        bottom = loop.loop(bottom, duration=patched_duration)
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

def grab_until_ending(next_words: [str], max: int) -> ([str], bool):
    endings = [".",",","?","!"]
    grabbed = 0
    for word in next_words:
        if grabbed < max:
            grabbed += 1
            if ends_with_any(word, endings):
                return grabbed, True
        else:
            break
    return grabbed, False

def ends_with_any(word: str, endings: [str]):
    for end in endings:
        if word.endswith(end):
            return True
    return False