import asyncio
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
    async def generate(shot_outlines: list[ShotOutline]):
        shots = []
        image_generator = generate_image.ImageGenerator(use_placeholder=True)
        speech_generator = generate_speech.SpeechGenerator(use_placeholder=True)

        print("Generating video outline...")

        image_generation_coroutines: list[asyncio.Future] = []
        speech_generation_coroutines: list[asyncio.Future] = []
        for i, shot_outline in enumerate(shot_outlines):
            print(f"Queuing shot {i+1}/{len(shot_outlines)}")
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
            shots.append(shot)

        return VideoOutline(shots)