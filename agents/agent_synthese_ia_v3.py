"""
Agent Synthèse IA v3 - Analyse COMPLÈTE
Modèle : GPT-5.2 Pro (OpenAI Responses API)
Rôle : Analyser TOUS les articles, sélectionner Top 6 + Autres
Budget : 8000 tokens max
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
MAX_TOKENS = 8000
INPUT_JSON = "recherche_ia_brute.json"
OUTPUT_MARKDOWN = "VeilleIA.md"


def generer_synthese_markdown(data: Dict[str, Any]) -> str:
    """
    Génère le markdown de synthèse à partir du JSON brut.
    Sélectionne 6 sujets principaux + liste les autres.
    """
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    articles = data.get('articles', [])
    nb_articles = len(articles)
    
    if nb_articles == 0:
        print("⚠️  Aucun article à analyser")
        return f"""---
agent: Synthèse IA v3 (GPT-5.2 Pro)
date: {datetime.now().strftime('%Y-%m-%d')}
catégorie: Intelligence Artificielle
---

# Veille IA – Aucune actualité disponible

**Période :** {data.get('periode', {}).get('debut', '')} au {data.get('periode', {}).get('fin', '')}

Aucune actualité n'a été collectée pour cette période.
"""
    
    print(f"📊 Analyse de {nb_articles} articles...")
    
    # Construction du contexte pour l'agent de synthèse
    articles_text = ""
    for i, art in enumerate(articles, 1):
        articles_text += f"\n--- ARTICLE {i}/{nb_articles} ---\n"
        articles_text += f"Titre: {art.get('titre', 'N/A')}\n"
        articles_text += f"Source: {art.get('source', 'N/A')}\n"
        articles_text += f"URL: {art.get('url', 'N/A')}\n"
        articles_text += f"Date: {art.get('date_publication', 'N/A')}\n"
        articles_text += f"Catégorie: {art.get('categorie_auto', 'N/A')}\n"
        articles_text += f"Contenu:\n{art.get('contenu_brut', 'N/A')}\n"
    
    # Prompt de synthèse
    periode_debut = data.get('periode', {}).get('debut', 'N/A')
    periode_fin = data.get('periode', {}).get('fin', 'N/A')
    
    prompt = f"""Tu es un analyste IA senior. Tu dois analyser TOUS les articles ci-dessous et produire une veille structurée.

ARTICLES À ANALYSER ({nb_articles} articles) :
{articles_text}

MISSION :
1. Sélectionne les 6 sujets les PLUS IMPORTANTS selon ces critères :
   - Couverture multi-sources (plusieurs sources parlent du même sujet = prioritaire)
   - Importance / impact (buzz médiatique, annonces majeures)
   - Nouveauté (infos vraiment récentes, pas de redites)
   - Diversité : 3 sujets "tendances/buzz" + 3 sujets "techniques/recherche"

2. Pour CHAQUE sujet des 6 sélectionnés, génère :
   - Résumé : 3-4 lignes max
   - Points de vue croisés : si plusieurs sources, comparer les angles
   - Analyse & implications : impacts sectoriels, opportunités, risques
   - Signaux faibles : tendances émergentes détectées
   - Sources : liste des URLs utilisées

3. Pour les AUTRES articles (non top 6) :
   - Liste compacte avec titre, thème, résumé 1 ligne, source + URL

FORMAT MARKDOWN STRICT :
---
agent: Synthèse IA v3 (GPT-5.2 Pro)
date: {datetime.now().strftime('%Y-%m-%d')}
catégorie: Intelligence Artificielle
---

# Veille IA & LLM – Semaine du {periode_debut} au {periode_fin}

## Introduction
[2-3 paragraphes de contexte général de la semaine]

---

## [SUJET 1/6] – [Titre du sujet]

### Résumé
[3-4 lignes]

### Points de vue croisés
**[Source1]**
[Analyse angle source 1]

**[Source2]**
[Analyse angle source 2]

### Analyse & implications
- Impacts sectoriels : [...]
- Opportunités : [...]
- Risques potentiels : [...]

### Signaux faibles
- [Point 1]
- [Point 2]

### Sources
- "[Titre article]" – [URL]

---

[... Répéter pour SUJET 2/6 à SUJET 6/6 ...]

---

## Autres sujets de la semaine

### [Titre sujet secondaire]
**Thème** : [Catégorie]
**Résumé** : [1 ligne]
**Source** : [[Nom source]] – [URL]

[... Répéter pour tous les autres articles ...]

---

## Synthèse finale

### Points clés de la semaine
[Liste 3-5 points clés]

### Divergences d'analyse notables
[Si des sources divergent sur un sujet]

### Signaux faibles & opportunités
[Tendances émergentes détectées]

### Risques & menaces
[Éléments d'attention]

### À surveiller la semaine prochaine
[Pistes de veille future]

---

**Fin de l'édition**
*Veille générée par Synthèse IA v3 (GPT-5.2 Pro)*

IMPORTANT :
- Pas d'emoji dans le markdown
- URLs complètes et valides
- Respect strict de la structure
- Synthèses denses et factuelles
"""

    print(f"🤖 Lancement GPT-5.2 Pro (max {MAX_TOKENS} tokens)...")
    
    try:
        # Appel OpenAI Responses API (pas de web search ici)
        response = client.responses.create(
            model=MODEL_SYNTHESE,
            input=prompt,
            max_tokens=MAX_TOKENS
        )
        
        tokens_used = response.usage.total_tokens
        print(f"📊 Tokens utilisés : {tokens_used}/{MAX_TOKENS}")
        
        markdown_content = response.output_text.strip()
        
        # Vérification basique
        if len(markdown_content) < 500:
            print("⚠️  ATTENTION : Markdown généré très court")
        
        if "SUJET 1/6" not in markdown_content:
            print("⚠️  ATTENTION : Structure [SUJET 1/6] non détectée")
        
        return markdown_content
    
    except Exception as e:
        print(f"❌ Erreur génération markdown : {e}")
        traceback.print_exc()
        raise


def uploader_vers_drive(contenu: str) -> None:
    """Upload du markdown vers Google Drive"""
    print(f"📤 Upload vers Google Drive : {OUTPUT_MARKDOWN}...")
    
    try:
        credentials = service_account.Credentials.from_service_account_info(
            GOOGLE_CREDENTIALS,
            scopes=['https://www.googleapis.com/auth/drive']
        )
        service = build('drive', 'v3', credentials=credentials)
        
        # Recherche du fichier existant
        query = f"name='{OUTPUT_MARKDOWN}' and '{FOLDER_ID}' in parents"
        results = service.files().list(q=query, fields="files(id)").execute()
        files = results.get('files', [])
        
        # Préparation du média
        media = MediaIoBaseUpload(
            io.BytesIO(contenu.encode('utf-8')),
            mimetype='text/markdown',
            resumable=True
        )
        
        # Update ou Create
        if files:
            file_id = files[0]['id']
            service.files().update(fileId=file_id, media_body=media).execute()
            print(f"✅ {OUTPUT_MARKDOWN} mis à jour (ID: {file_id})")
        else:
            file_metadata = {
                'name': OUTPUT_MARKDOWN,
                'parents': [FOLDER_ID]
            }
            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            print(f"✅ {OUTPUT_MARKDOWN} créé (ID: {file.get('id')})")
    
    except Exception as e:
        print(f"❌ Erreur upload Google Drive : {e}")
        traceback.print_exc()
        raise


def main():
    """Point d'entrée principal"""
    try:
        print("=" * 80)
        print("🤖 AGENT SYNTHÈSE IA v3 - ANALYSE COMPLÈTE")
        print("=" * 80)
        print(f"📂 Input : {INPUT_JSON}")
        print(f"📄 Output : {OUTPUT_MARKDOWN}")
        print(f"💰 Budget : {MAX_TOKENS} tokens max")
        print()
        
        # Lecture du JSON brut
        if not os.path.exists(INPUT_JSON):
            print(f"❌ Fichier introuvable : {INPUT_JSON}")
            sys.exit(1)
        
        with open(INPUT_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📊 {data.get('nb_articles', 0)} articles à analyser")
        print()
        
        # Génération synthèse
        markdown = generer_synthese_markdown(data)
        
        print()
        print(f"✅ Markdown généré ({len(markdown)} caractères)")
        
        # Upload vers Google Drive
        uploader_vers_drive(markdown)
        
        print()
        print("=" * 80)
        print("✅ SYNTHÈSE IA TERMINÉE")
        print("=" * 80)
        
        sys.exit(0)
    
    except Exception as e:
        print()
        print(f"❌ ÉCHEC : {e}")
        print("=" * 80)
        sys.exit(1)


if __name__ == "__main__":
    main()
