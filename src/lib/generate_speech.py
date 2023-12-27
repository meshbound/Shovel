import os
import time
import math
from google.cloud import texttospeech
from moviepy.editor import AudioFileClip

class SpeechGenerator:
    def __init__(self, use_placeholder: bool = False):
        self.use_placeholder = use_placeholder
        if use_placeholder:
            return
        auth_file_name = os.listdir("src/auth/google/")[0]
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "src/auth/google/" + auth_file_name
        self.client = texttospeech.TextToSpeechClient()

    def generate_speech(self, text: str) -> AudioFileClip:
        print(f"Generating speech from text: {text}")

        if self.use_placeholder:
            return AudioFileClip('src/lib/test_audio.wav')
        
        input_text = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Studio-Q"
        )
        audio_config=texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        response = self.client.synthesize_speech(
            input=input_text,
            voice=voice,
            audio_config=audio_config
        )

        filename = math.floor(time.time() * 1000)
        file_path = f"src/lib/audio_tmp/{filename}.mp3"
        with open(file_path, "wb") as out:
            out.write(response.audio_content)

        audio = AudioFileClip(file_path)

        return audio