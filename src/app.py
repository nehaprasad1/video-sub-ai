import os
from fastapi import FastAPI, UploadFile, File
from faster_whisper import WhisperModel
from src.utils import extract_audio

app = FastAPI()

# Load model once
model = WhisperModel("small")

def format_time(seconds):
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{hrs:02}:{mins:02}:{secs:02},{ms:03}"

def create_srt(segments, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        for i, segment in enumerate(segments):
            f.write(f"{i+1}\n")
            f.write(f"{format_time(segment.start)} --> {format_time(segment.end)}\n")
            f.write(segment.text.strip() + "\n\n")

@app.post("/transcribe")
async def transcribe_video(file: UploadFile = File(...)):
    # create folders
    os.makedirs("input", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    video_path = f"input/{file.filename}"

    # save uploaded file
    with open(video_path, "wb") as f:
        f.write(await file.read())

    audio_path = "input/audio.wav"

    # extract audio
    extract_audio(video_path, audio_path)

    # transcribe + translate
    segments, info = model.transcribe(
        audio_path,
        task="translate",
        beam_size=5,
        vad_filter=True
    )

    segments = list(segments)

    # create subtitles
    srt_path = "output/subtitles.srt"
    create_srt(segments, srt_path)

    return {
        "message": "Transcription complete",
        "file": file.filename,
        "language_detected": info.language,
        "srt_file": srt_path
    }