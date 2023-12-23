from generation.script_gen.outline import VideoOutline
from moviepy.editor import *

def patch_video(outline: VideoOutline) -> VideoFileClip:
    
    clips = [s.image.set_duration(s.speech.duration)
             for s in outline.shots]
    
    patched = concatenate_videoclips(clips, method="compose") # first combine all the image frames

    #for s in outline.shots:
    #    s.text
    return patched

