import whisper

def trascrivi_audio(percorso_file):
    model = whisper.load_model("base")
    result = model.transcribe(percorso_file)
    return result["text"]
