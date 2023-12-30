from moviepy.editor import AudioClip
import librosa
import numpy as np
import os

def get_silence(sound: AudioClip, silence_threshold: float = 0.01, chunk_size: int = 10) -> AudioClip:
    temp_file = "./TEMP_CLN.mp3"
    sound.write_audiofile(temp_file)
    data, sample_rate = librosa.load(temp_file, sr=None)
    os.remove(temp_file)

    start = get_silence_helper(data, sample_rate, silence_threshold, chunk_size)
    end = get_silence_helper(data[::-1], sample_rate, silence_threshold, chunk_size)
    return start, end

def get_silence_helper(data: np.ndarray, sample_rate: float, silence_threshold: float, chunk_size: int):
    chunk_size_sample = int((chunk_size / 1000) * sample_rate)
    duration = 0
    for i in range(0, len(data) - chunk_size_sample, chunk_size_sample):
        chunk = data[i:i + chunk_size_sample]
        loudness = librosa.feature.rms(y=chunk)
        if loudness < silence_threshold:
            duration += chunk_size
        else:
            break
    return duration / 1000