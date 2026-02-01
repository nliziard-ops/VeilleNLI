"""
Agent 3 - Synthèse IA
Modèle : GPT-5.2 Pro (OpenAI)
Rôle : Analyser recherche → Sélectionner 6 sujets → Synthétiser
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


# ================================================================================
# CONFIGURATION
# ================================================================================

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
GOOGLE_CREDENTIALS = json.loads(os.environ.get('GOOGLE_DRIVE_CREDENTIALS'))
FOLDER_ID = os.environ.get('GOOGLE_DRIVE_FOLDER_ID')

# Modèle GPT-5.2 Pro
MODEL_SYNTHESE = "gpt-5.2-pro"

INPUT_JSON = "recherche_ia_brute.json"
OUTPUT_MARKDOWN = "VeilleIA.md"


def charger_recherche_brute() -> Dict[str, Any]:
    if not os.path.exists(INPUT_JSON):
        raise FileNotFoundError(f"❌ {INPUT_JSON} introuvable")
    with open(INPUT_JSON, 'r', encoding='utf-8') as f:
        return json.load(f)


def generer_synthese_markdown(data: Dict[str, Any]) -> str:
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    articles = data.get('articles', [])
    if len(articles) == 0:
        return "# Veille IA\n\nAucune actualité.\n"
    
    articles_text = ""
    for i, art in enumerate(articles, 1):
        articles_text += f"\n[{i}] {art.get('titre')}\n"
        articles_text += f"Cat: {art.get('categorie')} | Source: {art.get('source')}\n"
        articles_text += f"URL: {art.get('url')}\n"
        articles_text += f"Résumé: {art.get('resume_court')}\n"
        articles_text += f"Synthèse: {art.get('synthese_complete')}\n"
    
    date_debut = data.get('periode', {}).get('debut', '2026-01-26')
    date_fin = data.get('periode', {}).get('fin', '2026-02-01')
    
    prompt = f"""Tu es analyste IA.

PÉRIODE : {date_debut} au {date_fin}

ARTICLES :
{articles_text}

MISSION :
1. Sélectionner 6 sujets principaux :
   - 3 tendances qui font parler (buzz, controverses)
   - 3 sujets technologiques (modèles, hardware, recherche)

2. Pour chaque sujet des 6 :
   - Résumé (3-4 lignes)
   - Synthèse approfondie (15-25 lignes)
   - Divergences entre sources
   - Sources avec URLs

3. Autres sujets en liste compacte

FORMAT MARKDOWN avec sections, sans emoji.
Génère maintenant."""

    print("🤖 Synthèse avec GPT-5.2 Pro...")
    
    try:
        response = client.responses.create(
            model=MODEL_SYNTHESE,
            input=prompt,
            max_tokens=8000
        )
        
        print(f"📊 Tokens : {response.usage.total_tokens}")
        return response.output_text.strip()
    
    except Exception as e:
        print(f"❌ Erreur GPT-5.2 Pro : {e}")
        traceback.print_exc()
        raise


def uploader_vers_drive(contenu: str) -> None:
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
    else:
        file_metadata = {'name': OUTPUT_MARKDOWN, 'parents': [FOLDER_ID]}
        service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    
    print(f"✅ {OUTPUT_MARKDOWN} uploadé")


def main():
    try:
        print("=" * 80)
        print("🤖 AGENT 3 - SYNTHÈSE IA (GPT-5.2 Pro)")
        print("=" * 80)
        
        data = charger_recherche_brute()
        synthese = generer_synthese_markdown(data)
        uploader_vers_drive(synthese)
        
        print("✅ TERMINÉ")
        sys.exit(0)
    except Exception as e:
        print(f"❌ ERREUR : {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
