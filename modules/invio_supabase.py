import os
from dotenv import load_dotenv
import requests
import json
from datetime import datetime

load_dotenv()
SUPABASE_URL = os.getenv(\"SUPABASE_URL\")
SUPABASE_KEY = os.getenv(\"SUPABASE_KEY\")
SUPABASE_TABLE = \"contenuti_studiati\"

def invia_a_supabase(nome_file, contenuto, output_ai):
    if not SUPABASE_URL or not SUPABASE_KEY:
        return 400, \"Chiavi mancanti nel .env\"
    headers = {
        \"apikey\": SUPABASE_KEY,
        \"Authorization\": f\"Bearer {SUPABASE_KEY}\",
        \"Content-Type\": \"application/json\"
    }
    data = {
        \"file_name\": nome_file,
        \"contenuto_originale\": contenuto[:3000],
        \"output_ai\": output_ai,
        \"data_studio\": datetime.now().isoformat()
    }
    try:
        response = requests.post(f\"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}\", headers=headers, data=json.dumps(data))
        return response.status_code, response.text
    except Exception as e:
        return 500, str(e)
