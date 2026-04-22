import os
import uuid
from fastapi import FastAPI, UploadFile, File, Query
from faster_whisper import WhisperModel
from src.utils import extract_audio
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Serve output files (subtitles)
app.mount("/output", StaticFiles(directory="output"), name="output")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model once (important for speed)
model = WhisperModel("small")


# ---------- UTIL FUNCTIONS ----------

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


# ---------- MAIN API ----------

@app.post("/transcribe")
async def transcribe_video(file: UploadFile = File(...)):

    # create folders
    os.makedirs("input", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    # unique filenames (VERY IMPORTANT)
    file_id = str(uuid.uuid4())

    video_path = f"input/{file_id}.mp4"
    audio_path = f"input/{file_id}.wav"
    srt_path = f"output/{file_id}.srt"

    # save uploaded video
    with open(video_path, "wb") as f:
        f.write(await file.read())

    # extract audio
    extract_audio(video_path, audio_path)

    # whisper transcription + translation
    segments, info = model.transcribe(
        audio_path,
        task="translate",
        beam_size=5,
        vad_filter=True
    )

    segments = list(segments)

    # create subtitle file
    create_srt(segments, srt_path)

    return {
        "message": "Transcription complete",
        "file": file.filename,
        "language_detected": info.language,
        "srt_file": os.path.basename(srt_path),
        "video_id": file_id
    }


# ---------- GET SUBTITLE API ----------

@app.get("/subtitle")
def get_subtitle(file: str = Query(...)):

    path = f"output/{file}"

    if not os.path.exists(path):
        return {"error": "Subtitle file not found"}

    with open(path, "r", encoding="utf-8") as f:
        return {"srt": f.read()}