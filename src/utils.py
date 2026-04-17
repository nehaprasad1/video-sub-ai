import ffmpeg
def extract_audio(video_path, audio_path="audio.wav"):
    (
        ffmpeg
        .input(video_path)
        .output(audio_path, format='wav')
        .run(overwrite_output=True)
    )