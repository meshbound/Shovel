from . import image
from . import speech
from ..script_gen.outline import VideoOutline, ShotOutline, Shot

def generate_video_outline(shot_outlines: list[ShotOutline]) -> VideoOutline:
    shots = []
    image_generator = image.ImageGenerator()
    speech_generator = speech.SpeechGenerator()

    print("Generating video outline...")

    for shot_outline in shot_outlines:
        generated_image = image_generator.generate_image(shot_outline.prompt)
        generated_speech = speech_generator.generate_speech(shot_outline.text)
        shot = Shot(shot_outline.text, generated_speech, generated_image)
        shots.append(shot)

    return VideoOutline(shots)