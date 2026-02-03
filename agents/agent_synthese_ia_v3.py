"""
Agent Synthèse IA v3 - Analyse COMPLÈTE
Modèle : GPT-5.2 Pro (OpenAI Responses API)
Rôle : Analyser TOUS les articles, sélectionner Top 6 + Autres
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
INPUT_JSON = "recherche_ia_brute.json"
OUTPUT_MARKDOWN = "VeilleIA.md"

def generer_synthese_markdown(data: Dict[str, Any]) -> str:
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    articles = data.get('articles', [])
    nb_articles = len(articles)
    
    if nb_articles == 0:
        return f"""---
agent: Synthèse IA v3
date: {datetime.now().strftime('%Y-%m-%d')}
---

# Veille IA – Aucune actualité disponible
"""
    
    print(f"📊 Analyse de {nb_articles} articles...")
    
    # Construction contexte concis
    articles_text = ""
    for i, art in enumerate(articles, 1):
        articles_text += f"\n[{i}] {art.get('titre', 'N/A')}\n"
        articles_text += f"Source: {art.get('source')} | URL: {art.get('url')}\n"
        articles_text += f"Catégorie: {art.get('categorie_auto')}\n"
        articles_text += f"Contenu: {art.get('contenu_brut', '')[:300]}...\n"
    
    periode_debut = data.get('periode', {}).get('debut', 'N/A')
    periode_fin = data.get('periode', {}).get('fin', 'N/A')
    
    prompt = f"""Analyste IA senior. {nb_articles} articles :
{articles_text}

MISSION:
1. Sélectionne 6 sujets (3 buzz + 3 tech) selon :
   - Multi-sources prioritaire
   - Importance/impact
   - Nouveauté

2. Pour chaque des 6 :
   - Résumé (3-4 lignes)
   - Points de vue croisés
   - Analyse & implications
   - Signaux faibles
   - Sources (URLs)

3. Autres articles : liste compacte (titre, thème, 1 ligne, source+URL)

MARKDOWN STRICT :
---
agent: Synthèse IA v3
date: {datetime.now().strftime('%Y-%m-%d')}
---

# Veille IA – Semaine du {periode_debut} au {periode_fin}

## Introduction
[2-3 paragraphes]

---

## [SUJET 1/6] – [Titre]

### Résumé
[3-4 lignes]

### Points de vue croisés
**[Source1]**
[Analyse]

### Analyse & implications
- Impacts sectoriels :
- Opportunités :
- Risques potentiels :

### Signaux faibles
- [Point 1]

### Sources
- "[Titre]" – [URL]

---

[... SUJET 2/6 à 6/6 ...]

---

## Autres sujets

### [Titre]
**Thème** : [Cat]
**Résumé** : [1 ligne]
**Source** : [Nom] – [URL]

---

## Synthèse finale

### Points clés
### Divergences
### Signaux faibles
### Risques
### À surveiller

---

*Veille générée par Synthèse IA v3*

PAS D'EMOJI. URLs valides. CONCIS."""

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
        print("🤖 AGENT SYNTHÈSE IA v3")
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
        print("✅ SYNTHÈSE IA TERMINÉE")
        print("=" * 80)
        sys.exit(0)
    
    except Exception as e:
        print(f"\n❌ ÉCHEC : {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
