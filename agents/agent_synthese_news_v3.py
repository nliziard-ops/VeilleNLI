"""
Agent Synthèse News v3 - Analyse COMPLÈTE
Modèle : GPT-5.2 Pro (OpenAI Responses API)
Rôle : Analyser TOUS les articles, sélectionner Top 6 (2+2+2) + Autres
Note : GPT-5.2 Pro ne supporte pas max_tokens
"""

import os
import sys
import json
import traceback
from datetime import datetime
from typing import Dict, Any
from openai import OpenAI
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

# Configuration
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
GOOGLE_CREDENTIALS = json.loads(os.environ.get('GOOGLE_DRIVE_CREDENTIALS'))
FOLDER_ID = os.environ.get('GOOGLE_DRIVE_FOLDER_ID')

MODEL_SYNTHESE = "gpt-5.2-pro"
INPUT_JSON = "recherche_news_brute.json"
OUTPUT_MARKDOWN = "VeilleNews.md"

def generer_synthese_markdown(data: Dict[str, Any]) -> str:
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    articles = data.get('articles', [])
    nb_articles = len(articles)
    repartition = data.get('repartition', {})
    
    if nb_articles == 0:
        return f"""---
agent: Synthèse News v3
date: {datetime.now().strftime('%Y-%m-%d')}
---

# Veille News – Aucune actualité disponible
"""
    
    print(f"📊 Analyse de {nb_articles} articles")
    print(f"📍 {repartition.get('international', 0)} Int | {repartition.get('national', 0)} Nat | {repartition.get('local', 0)} Local")
    
    articles_text = ""
    for i, art in enumerate(articles, 1):
        articles_text += f"\n[{i}] {art.get('titre', 'N/A')}\n"
        articles_text += f"Zone: {art.get('zone_geo')} | Source: {art.get('source')} | URL: {art.get('url')}\n"
        articles_text += f"Contenu: {art.get('contenu_brut', '')[:300]}...\n"
    
    periode_debut = data.get('periode', {}).get('debut', 'N/A')
    periode_fin = data.get('periode', {}).get('fin', 'N/A')
    
    prompt = f"""Journaliste senior. {nb_articles} articles :
{articles_text}

MISSION:
1. Sélectionne 6 sujets (2 int + 2 nat + 2 local Bretagne) selon :
   - Multi-sources
   - Importance
   - Nouveauté

2. Pour chaque des 6 :
   - Résumé (3-4 lignes)
   - Points de vue croisés
   - Analyse & implications
   - Signaux faibles
   - Sources

3. Autres : liste compacte

MARKDOWN STRICT (structure identique à IA mais 2 Int + 2 Nat + 2 Local).
LOCAL: Nantes, sports maritimes.
PAS D'EMOJI. CONCIS."""

    print(f"🤖 Lancement GPT-5.2 Pro...")
    
    try:
        response = client.responses.create(
            model=MODEL_SYNTHESE,
            input=prompt
        )
        
        print(f"📊 Tokens : {response.usage.total_tokens}")
        return response.output_text.strip()
    
    except Exception as e:
        print(f"❌ Erreur : {e}")
        traceback.print_exc()
        raise

def uploader_vers_drive(contenu: str) -> None:
    print(f"📤 Upload Google Drive : {OUTPUT_MARKDOWN}...")
    
    try:
        credentials = service_account.Credentials.from_service_account_info(
            GOOGLE_CREDENTIALS,
            scopes=['https://www.googleapis.com/auth/drive']
        )
        service = build('drive', 'v3', credentials=credentials)
        
        query = f"name='{OUTPUT_MARKDOWN}' and '{FOLDER_ID}' in parents"
        results = service.files().list(q=query, fields="files(id)").execute()
        files = results.get('files', [])
        
        media = MediaIoBaseUpload(
            io.BytesIO(contenu.encode('utf-8')),
            mimetype='text/markdown',
            resumable=True
        )
        
        if files:
            service.files().update(fileId=files[0]['id'], media_body=media).execute()
            print(f"✅ {OUTPUT_MARKDOWN} mis à jour")
        else:
            service.files().create(
                body={'name': OUTPUT_MARKDOWN, 'parents': [FOLDER_ID]},
                media_body=media
            ).execute()
            print(f"✅ {OUTPUT_MARKDOWN} créé")
    
    except Exception as e:
        print(f"❌ Erreur : {e}")
        traceback.print_exc()
        raise

def main():
    try:
        print("=" * 80)
        print("🤖 AGENT SYNTHÈSE NEWS v3")
        print("=" * 80)
        
        if not os.path.exists(INPUT_JSON):
            print(f"❌ Fichier introuvable : {INPUT_JSON}")
            sys.exit(1)
        
        with open(INPUT_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📊 {data.get('nb_articles', 0)} articles à analyser")
        
        markdown = generer_synthese_markdown(data)
        uploader_vers_drive(markdown)
        
        print("\n" + "=" * 80)
        print("✅ SYNTHÈSE NEWS TERMINÉE")
        print("=" * 80)
        sys.exit(0)
    
    except Exception as e:
        print(f"\n❌ ÉCHEC : {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
