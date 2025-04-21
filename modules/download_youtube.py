import subprocess
import sys

def scarica_da_youtube(link):
    print(f"⬇️ Scarico video da YouTube: {link}")
    comando = [
        "yt-dlp",
        "-f", "mp4",
        "--no-playlist",
        "--output", "lezione1.%(ext)s",
        link
    ]
    try:
        subprocess.run(comando, check=True)
        print("✅ Download completato: lezione1.mp4")
    except Exception as e:
        print(f"❌ Errore nel download: {e}")
        sys.exit(1)
