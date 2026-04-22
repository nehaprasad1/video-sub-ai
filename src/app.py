import os
from src.utils import extract_audio
from faster_whisper import WhisperModel

# Use tiny model for low-end systems
model = WhisperModel("tiny")
# model = WhisperModel("small")

def transcribe_audio(audio_path):
    segments, info = model.transcribe(audio_path)
    return list(segments)   # IMPORTANT FIX

def save_transcript(segments, output_file="output/transcript.txt"):
    os.makedirs("output", exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        for segment in segments:
            f.write(segment.text.strip() + " ")

def format_time(seconds):
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{hrs:02}:{mins:02}:{secs:02},{ms:03}"  # correct SRT format

def create_srt(segments, output_file="output/subtitles.srt"):
    os.makedirs("output", exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        for i, segment in enumerate(segments):
            f.write(f"{i+1}\n")
            f.write(f"{format_time(segment.start)} --> {format_time(segment.end)}\n")
            f.write(segment.text.strip() + "\n\n")

def process_video(video_path):
    audio_path = "input/audio.wav"

    print("Extracting audio...")
    extract_audio(video_path, audio_path)

    print("Transcribing audio...")
    segments = transcribe_audio(audio_path)

    print("Saving transcript...")
    save_transcript(segments)

    print("Generating subtitles...")
    create_srt(segments)

    print("Done! Files saved in output/")

if __name__ == "__main__":
    video_file = "input/sample.mp4"
    process_video(video_file)