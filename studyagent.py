# StudyAgent Completo – CLI + AI + Supabase (con supporto .env, whisper, salvataggio frame, analisi visiva con BLIP, salvataggio TXT e download YouTube)

import os
import sys
import subprocess
from datetime import datetime
import requests
import json
from dotenv import load_dotenv
import whisper
import cv2
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

# ✅ Carica variabili da file .env
load_dotenv()

# ✅ Parametri Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_TABLE = "contenuti_studiati"

# ✅ Carica BLIP per caption visive
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# ✅ Funzione per scaricare un video da YouTube
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
        print(f"❌ Errore nel download da YouTube: {e}")
        sys.exit(1)

# ✅ Funzione per inviare dati a Supabase
def invia_a_supabase(nome_file, contenuto, output_ai):
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ Errore: SUPABASE_URL o SUPABASE_KEY non impostati. Inseriscili nel file .env.")
        return 400, "Variabili mancanti"

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "file_name": nome_file,
        "contenuto_originale": contenuto[:3000],
        "output_ai": output_ai,
        "data_studio": datetime.now().isoformat()
    }
    try:
        response = requests.post(f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}", headers=headers, data=json.dumps(data))
        return response.status_code, response.text
    except Exception as e:
        return 500, str(e)

# ✅ Verifica connessione Supabase
def test_connessione():
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ Variabili d'ambiente mancanti: SUPABASE_URL o SUPABASE_KEY")
        return

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }
    try:
        res = requests.get(f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}?limit=1", headers=headers)
        if res.status_code == 200:
            print("✅ Connessione a Supabase riuscita! Tabella accessibile.")
        else:
            print(f"❌ Errore connessione Supabase: {res.text}")
    except Exception as e:
        print(f"❌ Errore connessione: {e}")

# ✅ Analisi AI simulata (GPT gratuito disattivato)
def analizza_contenuto_ai(testo):
    print("⚠️  GPT disattivato – risposta simulata generata localmente.")
    return """
📌 Riassunto:
Il contenuto tratta i fondamenti delle reti, concentrandosi sul modello OSI, indirizzamento IP, subnetting, trasmissione dei dati e protocolli.

🧠 Concetti chiave:
- Modello OSI a 7 livelli
- IP come protocollo di livello 3
- Subnet mask e indirizzamento
- Trasmissione fisica dei bit
- Protocollo TCP e connessione

❓ Quiz:
1. Quale livello del modello OSI si occupa della trasmissione fisica dei dati?
   a) Livello di rete
   b) Livello trasporto
   c) Livello fisico ✅
   d) Livello sessione

2. TCP è:
   a) Un protocollo senza connessione
   b) Un'applicazione di rete
   c) Un protocollo orientato alla connessione ✅
   d) Un tipo di hardware

3. La subnet mask serve a:
   a) Proteggere la rete
   b) Calcolare l'ora locale
   c) Definire il numero di host nella rete ✅
   d) Connettere dispositivi Bluetooth
"""

# ✅ Trascrizione audio/video con Whisper
def trascrivi_audio(percorso_file):
    print(f"🎧 Trascrivo il file con Whisper: {percorso_file}")
    model = whisper.load_model("base")
    result = model.transcribe(percorso_file)
    return result["text"]

# ✅ Estrazione + salvataggio frame + descrizione immagini con BLIP
def estrai_e_descrivi_frame(video_path):
    print("🖼️  Estrazione e salvataggio frame 1 ogni 4 secondi + descrizione...")
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    intervallo_frame = int(fps * 4)
    count, saved = 0, 0
    os.makedirs("frames", exist_ok=True)
    descrizioni = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if count % intervallo_frame == 0:
            file_path = f"frames/frame_{saved:03}.jpg"
            cv2.imwrite(file_path, frame)

            image = Image.open(file_path).convert("RGB")
            inputs = processor(image, return_tensors="pt")
            out = model.generate(**inputs)
            caption = processor.decode(out[0], skip_special_tokens=True)
            descrizioni.append(f"Frame {saved:03}: {caption}")
            print(f"📝 Frame {saved:03}: {caption}")
            saved += 1
        count += 1
    cap.release()
    return "\n".join(descrizioni)

# ✅ Main CLI – Usa file audio/video o testo simulato o scarica da YouTube
def main():
    print("📚 StudyAgent – CLI AI + Supabase + Whisper + Frame + BLIP")
    test_connessione()

    # Se è stato fornito un link YouTube da riga di comando
    if len(sys.argv) > 1 and sys.argv[1].startswith("http"):
                # ✅ Rimuove parametri URL come &list=... o &index=...
        link = sys.argv[1].split("&")[0]
        scarica_da_youtube(link)

    nome_file = "lezione1.mp4"

    if not os.path.exists(nome_file):
        print("❌ File non trovato. Uso contenuto simulato.")
        contenuto = """
        Titolo: Fondamenti di Reti

        1. Il modello OSI è composto da 7 livelli.
        2. IP è un protocollo di livello 3.
        3. La subnet mask definisce il numero di host in una rete.
        4. Il livello fisico gestisce bit e trasmissioni elettriche.
        5. TCP è un protocollo orientato alla connessione.
        """
        descrizione_frame = "Nessun frame disponibile."
    else:
        contenuto = trascrivi_audio(nome_file)
        descrizione_frame = estrai_e_descrivi_frame(nome_file)

    print("\n📖 Testo acquisito:")
    print(contenuto[:300])

    print("\n🤖 Invio al tutor AI...")
    output_ai = analizza_contenuto_ai(contenuto)

    print("\n📘 Risultato dell'analisi AI:")
    print(output_ai[:1000])

    print("\n🖼️ Riassunto visivo dei frame:")
    print(descrizione_frame[:1000])

    nome_txt = f"report_{os.path.splitext(nome_file)[0]}.txt"
    with open(nome_txt, "w", encoding="utf-8") as f:
        f.write("📖 Trascrizione del contenuto:\n")
        f.write(contenuto + "\n\n")
        f.write("📘 Analisi AI (simulata):\n")
        f.write(output_ai + "\n\n")
        f.write("🖼️ Riassunto visivo dei frame:\n")
        f.write(descrizione_frame)
    print(f"📁 File riassuntivo salvato: {nome_txt}")

    status, msg = invia_a_supabase(nome_file, contenuto, output_ai)
    if status == 201:
        print("✅ Contenuto + AI salvati su Supabase!")
    else:
        print(f"❌ Errore salvataggio: {msg}")

if __name__ == "__main__":
    main()
