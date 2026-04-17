import whisper
from utils import extract_audio
model = whisper.load_model("base")

def transcribe_audio(audio_path):
    res = model.transcribe(audio_path)
    return res