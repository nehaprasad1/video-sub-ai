import os
from src.utils import extract_audio
from faster_whisper import WhisperModel

model = WhisperModel("tiny")
#model = WhisperModel("small")

def transcribe_audio(audio_path):
    segments, info = model.transcribe(audio_path)
    return segments

def save_transcript(segments, output_file="output/transcript.txt"):
    os.makedirs("output", exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        for segment in segments:
            f.write(segment.text.strip() + " ")

def process_video(video_path):
    audio_path = "input/audio.wav"

    print("Extracting audio...")
    extract_audio(video_path, audio_path)

    print("Transcribing audio...")
    segments = transcribe_audio(audio_path)

    print("Saving transcript...")
    save_transcript(segments)

    print("Done! Transcript saved in output/transcript.txt")

if __name__ == "__main__":
    video_file = "input/sample.mp4"
    process_video(video_file)