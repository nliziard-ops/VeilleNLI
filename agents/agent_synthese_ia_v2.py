"""
Agent 3 - Synthèse IA
Modèle : GPT-5.2 Pro (OpenAI Responses API)
Rôle : Sélectionner 6 sujets + Synthétiser
"""

import os
import json
import sys
import traceback
from datetime import datetime
from typing import Dict, Any
from openai import OpenAI
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
GOOGLE_CREDENTIALS = json.loads(os.environ.get('GOOGLE_DRIVE_CREDENTIALS'))
FOLDER_ID = os.environ.get('GOOGLE_DRIVE_FOLDER_ID')

MODEL_SYNTHESE = "gpt-5.2-pro"
INPUT_JSON = "recherche_ia_brute.json"
OUTPUT_MARKDOWN = "VeilleIA.md"

def generer_synthese_markdown(data: Dict[str, Any]) -> str:
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    articles = data.get('articles', [])
    if len(articles) == 0:
        return "# Veille IA\n\nAucune actualité.\n"
    
    articles_text = ""
    for i, art in enumerate(articles, 1):
        articles_text += f"\n[{i}] {art.get('titre')}\n"
        articles_text += f"Cat: {art.get('categorie')} | Source: {art.get('source')} | URL: {art.get('url')}\n"
        articles_text += f"{art.get('synthese_complete')}\n"
    
    prompt = f"""Analyste IA. Articles : {articles_text}

6 sujets (3 tendances buzz + 3 tech). Pour chaque : résumé 3-4 lignes, synthèse 15-25 lignes, divergences sources, URLs.
Autres : liste compacte.
Markdown, sans emoji."""

    print("🤖 GPT-5.2 Pro...")
    
    try:
        # SYNTAXE OFFICIELLE OPENAI - Responses API
        response = client.responses.create(
            model=MODEL_SYNTHESE,
            input=prompt,
            max_tokens=8000
        )
        
        print(f"📊 Tokens : {response.usage.total_tokens}")
        return response.output_text.strip()
    except Exception as e:
        print(f"❌ Erreur : {e}")
        traceback.print_exc()
        raise

def uploader_vers_drive(contenu: str) -> None:
    credentials = service_account.Credentials.from_service_account_info(
        GOOGLE_CREDENTIALS, scopes=['https://www.googleapis.com/auth/drive']
    )
    service = build('drive', 'v3', credentials=credentials)
    
    query = f"name='{OUTPUT_MARKDOWN}' and '{FOLDER_ID}' in parents"
    results = service.files().list(q=query, fields="files(id)").execute()
    files = results.get('files', [])
    
    media = MediaIoBaseUpload(io.BytesIO(contenu.encode('utf-8')), mimetype='text/markdown', resumable=True)
    
    if files:
        service.files().update(fileId=files[0]['id'], media_body=media).execute()
    else:
        service.files().create(body={'name': OUTPUT_MARKDOWN, 'parents': [FOLDER_ID]}, media_body=media).execute()
    
    print(f"✅ {OUTPUT_MARKDOWN} uploadé")

def main():
    try:
        print("=" * 80)
        print("🤖 AGENT 3 - GPT-5.2 PRO")
        print("=" * 80)
        
        with open(INPUT_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        synthese = generer_synthese_markdown(data)
        uploader_vers_drive(synthese)
        
        print("✅ TERMINÉ")
        sys.exit(0)
    except Exception as e:
        print(f"❌ {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
