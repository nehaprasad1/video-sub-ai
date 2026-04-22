# Video Sub AI 🎥

AI tool that converts video speech into subtitles using Whisper.

---

## 🚀 Features
- Video upload  
- Speech-to-text conversion  
- Automatic subtitle generation (.srt)  

---

## 🛠️ Tech Stack
Python · FastAPI · Whisper · FFmpeg · HTML/CSS/JS  

---

## 🔄 Workflow

1. User uploads a video through the web interface  
2. Backend saves the video locally  
3. FFmpeg extracts audio from the video  
4. Whisper AI processes the audio and detects speech  
5. Speech is converted into timestamped text segments  
6. Segments are formatted into `.srt` subtitle file  
7. Subtitles are sent back and displayed in the frontend video player  

---

## 👨‍💻 Author
AI + Full Stack Project
