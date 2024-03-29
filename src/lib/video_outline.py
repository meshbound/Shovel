import lib.generate_image as generate_image
import lib.generate_speech as generate_speech
from lib.config import get_config
import asyncio

from moviepy.editor import ImageClip, AudioFileClip


class Shot:
    def __init__(self, text: str, speech: AudioFileClip, image: ImageClip):
        self.text = text
        self.speech = speech
        self.image = image
    
    def __str__(self) -> str:
        return f"\"{self.text}\""


class ShotOutline:
    def __init__(self, text: str, prompt: str):
        self.text = text
        self.prompt = prompt


class ShotOutlineMeta:
    def __init__(self, title: str, description: str, shot_outlines: list[ShotOutline]):
        self.title = title
        self.description = description
        self.shot_outlines = shot_outlines


class VideoOutline:
    def __init__(self, title: str, description: str, shots: list[Shot]) -> None:
        self.title = title
        self.description = description
        self.shots = shots

    @staticmethod
    async def generate(shot_outline_meta: ShotOutlineMeta):
        shots = []
        image_gen_use_placeholder = (get_config()["image_gen"]["use_placeholder"] == "True")
        speech_gen_use_placeholder = (get_config()["speech_gen"]["use_placeholder"] == "True")
        image_generator = generate_image.ImageGenerator(image_gen_use_placeholder)
        speech_generator = generate_speech.SpeechGenerator(speech_gen_use_placeholder)

        print("Generating video outline...")

        image_generation_coroutines: list[asyncio.Future] = []
        speech_generation_coroutines: list[asyncio.Future] = []
        shot_outlines = shot_outline_meta.shot_outlines
        for i, shot_outline in enumerate(shot_outlines):
            print(f"Queuing shot {i+1}/{len(shot_outlines)}")
            print(shot_outline.text)
            print(shot_outline.prompt)
            speech_future = asyncio.ensure_future(speech_generator.generate_speech(shot_outline.text))
            image_future = asyncio.ensure_future(image_generator.generate_image(shot_outline.prompt))
            speech_generation_coroutines.append(speech_future)
            image_generation_coroutines.append(image_future)

        print("Waiting for shots to be generated...")
        await asyncio.gather(*image_generation_coroutines)
        await asyncio.gather(*speech_generation_coroutines)

        for i, shot_outline in enumerate(shot_outlines):
            generated_speech = speech_generation_coroutines[i].result()
            generated_image = image_generation_coroutines[i].result()
            shot = Shot(shot_outline.text, generated_speech, generated_image)
            print("Shot:", shot)
            shots.append(shot)

        title = shot_outline_meta.title
        description = shot_outline_meta.description
        return VideoOutline(title, description, shots)