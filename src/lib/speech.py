from moviepy.editor import AudioFileClip

class SpeechGenerator:
    def __init__(self):
        pass

    def generate_speech(self, text: str) -> AudioFileClip:
        print(f"Generating speech from text: {text}")
        audio = AudioFileClip('src/lib/test_audio.wav')
        return audio