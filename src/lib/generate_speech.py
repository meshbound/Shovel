import os
import time
import math
import pyttsx3
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
            audio_path = self.generate_placeholder_speech(text)
            return AudioFileClip(audio_path)
        
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

        audio = self.write_to_timestamped_file(response.audio_content)
        return audio
    
    @staticmethod
    def generate_placeholder_speech(text) -> str:
        # Initialize the TTS engine
        engine = pyttsx3.init()

        # Set properties (optional)
        engine.setProperty('rate', 150)  # Speed of speech
        engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)

        # Save to audio file (WAV format)
        filename = math.floor(time.time() * 1000)
        file_path = f"src/lib/audio_tmp/{filename}.wav"
        engine.save_to_file(text, file_path)

        # Wait for the file to be created
        while not engine.isBusy():
            time.sleep(0.1)

        # Run the TTS engine
        engine.runAndWait()

        return file_path

    @staticmethod
    def write_to_timestamped_file(data) -> AudioFileClip:
        filename = math.floor(time.time() * 1000)
        file_path = f"src/lib/audio_tmp/{filename}.mp3"
        with open(file_path, "wb") as out:
            out.write(data)

        return AudioFileClip(file_path)