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
    
    # Construction contexte concis
    articles_text = ""
    for i, art in enumerate(articles, 1):
        articles_text += f"\n[{i}] {art.get('titre', 'N/A')}\n"
        articles_text += f"Zone: {art.get('zone_geo')} | Source: {art.get('source')} | URL: {art.get('url')}\n"
        articles_text += f"Contenu: {art.get('contenu_brut', '')[:300]}...\n"
    
    periode_debut = data.get('periode', {}).get('debut', 'N/A')
    periode_fin = data.get('periode', {}).get('fin', 'N/A')
    
    prompt = f"""Journaliste senior spécialisé en veille média. {nb_articles} articles couvrant international, national, local Bretagne/Pays de Loire :
{articles_text}

MISSION:
1. Sélectionne 6 sujets d'actualité selon cette répartition STRICTE :
   - 2 INTERNATIONAL (géopolitique, économie mondiale, tech internationale)
   - 2 NATIONAL (France : politique, économie, société, tech)
   - 2 LOCAL (Bretagne/Pays de Loire : Nantes, Rennes, sports maritimes - voile, surf, kitesurf, wingfoil)
   
   Critères de sélection :
   - Multi-sources prioritaire
   - Importance/impact
   - Nouveauté

2. Pour chaque des 6 sujets :
   - Résumé (3-4 lignes)
   - Points de vue croisés (si multi-sources)
   - Analyse & implications
   - Signaux faibles
   - Sources (URLs complètes)

3. Autres articles : liste compacte (titre, zone, 1 ligne, source+URL)

MARKDOWN STRICT (respecte EXACTEMENT ce format) :
---
agent: Synthèse News v3
date: {datetime.now().strftime('%Y-%m-%d')}
---

# Veille News – Semaine du {periode_debut} au {periode_fin}

## Introduction
[2-3 paragraphes présentant les tendances de la semaine : 2 sujets internationaux, 2 nationaux, 2 locaux Bretagne]

---

## [SUJET 1/6] – [Titre du sujet international]

### Résumé
[3-4 lignes décrivant les faits principaux]

### Points de vue croisés
**[Source1]**
[Analyse du point de vue de la source 1]

**[Source2]** (si multi-sources)
[Analyse du point de vue de la source 2]

### Analyse & implications
- Impacts sectoriels : [Analyse]
- Opportunités : [Analyse]
- Risques potentiels : [Analyse]

### Signaux faibles
- [Point d'attention 1]
- [Point d'attention 2]

### Sources
- "[Titre article]" – [URL complète]
- "[Titre article 2]" – [URL complète] (si plusieurs)

---

## [SUJET 2/6] – [Titre du sujet international]

[... même structure que SUJET 1/6 ...]

---

## [SUJET 3/6] – [Titre du sujet national]

[... même structure que SUJET 1/6 ...]

---

## [SUJET 4/6] – [Titre du sujet national]

[... même structure que SUJET 1/6 ...]

---

## [SUJET 5/6] – [Titre du sujet local Bretagne]

[... même structure que SUJET 1/6 ...]

---

## [SUJET 6/6] – [Titre du sujet local Bretagne]

[... même structure que SUJET 1/6 ...]

---

## Autres sujets

### [Titre article 1]
**Zone** : [International/National/Local]
**Résumé** : [1 ligne décrivant le sujet]
**Source** : [Nom source] – [URL]

### [Titre article 2]
**Zone** : [International/National/Local]
**Résumé** : [1 ligne décrivant le sujet]
**Source** : [Nom source] – [URL]

[... autres articles non sélectionnés dans le top 6 ...]

---

## Synthèse finale

### Points clés
[Liste des 3-4 éléments majeurs de la semaine]

### Divergences
[Contradictions ou différences d'approche entre sources]

### Signaux faibles
[Tendances émergentes à surveiller]

### Risques
[Risques identifiés dans l'actualité]

### À surveiller
[Dossiers à suivre la semaine prochaine]

---

*Veille générée par Synthèse News v3*

RÈGLES ABSOLUES :
- PAS D'EMOJI
- URLs COMPLÈTES et VALIDES
- CONCIS (pas de blabla)
- RESPECT STRICT des séparateurs `---`
- 6 SUJETS EXACTS (2+2+2)
- LOCAL = Bretagne/Pays de Loire (Nantes, Rennes, sports maritimes)"""

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
