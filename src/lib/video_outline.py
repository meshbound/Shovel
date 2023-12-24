import lib.image as image
import lib.generate_speech as generate_speech

from moviepy.editor import ImageClip, AudioFileClip


class Shot:
    def __init__(self, text: str, speech: AudioFileClip, image: ImageClip):
        self.text = text
        self.speech = speech
        self.image = image


class ShotOutline:
    def __init__(self, text: str, prompt: str):
        self.text = text
        self.prompt = prompt


class VideoOutline:
    def __init__(self, shots: list[Shot]) -> None:
        self.shots = shots

    @staticmethod
    def generate(shot_outlines: list[ShotOutline]):
        shots = []
        image_generator = image.ImageGenerator()
        speech_generator = generate_speech.SpeechGenerator()

        print("Generating video outline...")

        for shot_outline in shot_outlines:
            generated_image = image_generator.generate_image(shot_outline.prompt, use_placeholder=True)
            generated_speech = speech_generator.generate_speech(shot_outline.text, use_placeholder=True)
            shot = Shot(shot_outline.text, generated_speech, generated_image)
            shots.append(shot)

        return VideoOutline(shots)