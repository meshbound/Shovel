import lib.generate_image as generate_image
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
        image_generator = generate_image.ImageGenerator(use_placeholder=True)
        speech_generator = generate_speech.SpeechGenerator(use_placeholder=True)

        print("Generating video outline...")

        for shot_outline in shot_outlines:
            generated_image = image_generator.generate_image(shot_outline.prompt)
            generated_speech = speech_generator.generate_speech(shot_outline.text)
            shot = Shot(shot_outline.text, generated_speech, generated_image)
            shots.append(shot)

        return VideoOutline(shots)