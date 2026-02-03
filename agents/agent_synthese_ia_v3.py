"""
Agent Synthèse IA v3 - ANALYSE COMPLÈTE
Modèle : GPT-5.2 Pro (OpenAI Responses API)
Rôle : Sélectionner 6 sujets + Synthétiser selon template
Max tokens : 8000
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
MAX_TOKENS = 8000
INPUT_JSON = "recherche_ia_brute.json"
OUTPUT_MARKDOWN = "VeilleIA.md"


def generer_synthese_markdown(data: Dict[str, Any]) -> str:
    """
    Analyse TOUS les articles et génère le markdown structuré.
    Sélectionne 6 sujets principaux + liste "Autres sujets".
    """
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    articles = data.get('articles', [])
    nb_articles = len(articles)
    
    if nb_articles == 0:
        print("⚠️  Aucun article à analyser")
        return f"""---
agent: Synthèse IA v3
date: {datetime.now().strftime('%Y-%m-%d')}
catégorie: Intelligence Artificielle
---

# Veille IA – Semaine du {data.get('periode', {}).get('debut', 'N/A')} au {data.get('periode', {}).get('fin', 'N/A')}

**Aucune actualité collectée cette semaine.**
"""
    
    print(f"📊 Analyse de {nb_articles} articles collectés")
    
    # Construction du contexte pour l'agent de synthèse
    articles_text = ""
    for i, art in enumerate(articles, 1):
        articles_text += f"\n[ARTICLE {i}]\n"
        articles_text += f"Titre: {art.get('titre', 'N/A')}\n"
        articles_text += f"Source: {art.get('source', 'N/A')}\n"
        articles_text += f"URL: {art.get('url', 'N/A')}\n"
        articles_text += f"Date: {art.get('date_publication', 'N/A')}\n"
        articles_text += f"Catégorie: {art.get('categorie', 'N/A')}\n"
        articles_text += f"Contenu: {art.get('contenu_brut', 'N/A')}\n"
        articles_text += "-" * 80 + "\n"
    
    # PROMPT DE SYNTHÈSE STRUCTURÉE
    prompt = f"""Tu es un analyste IA expert. Tu dois analyser TOUS les articles collectés et produire une veille structurée.

ARTICLES COLLECTÉS ({nb_articles} au total) :
{articles_text}

PÉRIODE : {data.get('periode', {}).get('debut', 'N/A')} au {data.get('periode', {}).get('fin', 'N/A')}

MISSION :
1. Sélectionne les 6 sujets LES PLUS PERTINENTS selon ces critères :
   - Couverture multi-sources (plusieurs sources parlent du même sujet = priorité)
   - Importance/impact dans le domaine IA
   - Nouveauté/fraîcheur de l'information
   - Équilibre : 3 sujets "buzz/tendances" + 3 sujets "tech/recherche"

2. Pour chaque sujet des TOP 6 :
   - Résumé : 3-4 lignes synthétiques
   - Points de vue croisés : analyse comparative des sources (si multi-sources)
   - Analyse & implications : impacts sectoriels, opportunités, risques
   - Signaux faibles : tendances émergentes détectées
   - Sources : liste des URLs

3. Pour les autres articles (non top 6) :
   - Liste compacte dans "Autres sujets de la semaine"
   - Format : Titre + Thème + Résumé 1-2 lignes + Source + URL

4. Synthèse finale :
   - Points clés de la semaine
   - Divergences d'analyse notables
   - Signaux faibles & opportunités
   - Risques & menaces
   - À surveiller la semaine prochaine

FORMAT MARKDOWN STRICT (sans emojis) :

---
agent: Synthèse IA v3
date: {datetime.now().strftime('%Y-%m-%d')}
catégorie: Intelligence Artificielle
---

# Veille IA & LLM – Semaine du {data.get('periode', {}).get('debut', 'N/A')} au {data.get('periode', {}).get('fin', 'N/A')}

**Édition [Nom thématique]**

---

## Introduction

[Paragraphe de contexte global de la semaine]

---

## [SUJET 1/6] – [Titre du sujet]

### Résumé
[3-4 lignes synthétiques]

### Points de vue croisés

**[Source1]**
[Analyse de cette source]

**[Source2]**
[Analyse de cette source]

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

[RÉPÉTER POUR SUJETS 2/6, 3/6, 4/6, 5/6, 6/6]

---

## Autres sujets de la semaine

### [Titre sujet secondaire]
**Thème** : [Catégorie]
**Résumé** : [1-2 lignes]
**Source** : [Nom source] – [URL]

[RÉPÉTER pour les autres articles non retenus dans le top 6]

---

## Synthèse finale

### Points clés de la semaine
[Liste numérotée]

### Divergences d'analyse notables
[Analyse]

### Signaux faibles & opportunités
[Liste]

### Risques & menaces
[Analyse]

### À surveiller la semaine prochaine
[Liste]

---

**Fin de l'édition**
*Veille générée par Synthèse IA v3 (OpenAI GPT-5.2 Pro)*

IMPORTANT : Réponds UNIQUEMENT le markdown, sans texte avant/après.
"""

    print("=" * 80)
    print("🧠 SYNTHÈSE ANALYTIQUE - GPT-5.2 PRO")
    print(f"🎯 Max tokens : {MAX_TOKENS}")
    print("=" * 80)
    
    try:
        # SYNTAXE OFFICIELLE OPENAI - Responses API
        response = client.responses.create(
            model=MODEL_SYNTHESE,
            input=prompt,
            max_tokens=MAX_TOKENS
        )
        
        tokens_used = response.usage.total_tokens
        print(f"📊 Tokens utilisés : {tokens_used}/{MAX_TOKENS}")
        
        markdown_content = response.output_text.strip()
        
        print(f"✅ Markdown généré : {len(markdown_content)} caractères")
        
        return markdown_content
    
    except Exception as e:
        print(f"❌ Erreur synthèse : {e}")
        traceback.print_exc()
        raise


def uploader_vers_drive(contenu: str) -> None:
    """Upload du markdown vers Google Drive"""
    print("\n📤 Upload vers Google Drive...")
    
    credentials = service_account.Credentials.from_service_account_info(
        GOOGLE_CREDENTIALS, 
        scopes=['https://www.googleapis.com/auth/drive']
    )
    service = build('drive', 'v3', credentials=credentials)
    
    # Recherche fichier existant
    query = f"name='{OUTPUT_MARKDOWN}' and '{FOLDER_ID}' in parents"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])
    
    media = MediaIoBaseUpload(
        io.BytesIO(contenu.encode('utf-8')), 
        mimetype='text/markdown', 
        resumable=True
    )
    
    if files:
        # Mise à jour
        file_id = files[0]['id']
        service.files().update(fileId=file_id, media_body=media).execute()
        print(f"✅ {OUTPUT_MARKDOWN} mis à jour (ID: {file_id})")
    else:
        # Création
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


def main():
    """Point d'entrée principal"""
    try:
        print("\n" + "=" * 80)
        print("🤖 AGENT SYNTHÈSE IA v3 - ANALYSE COMPLÈTE")
        print("=" * 80 + "\n")
        
        # Lecture du JSON brut
        print(f"📥 Lecture de {INPUT_JSON}...")
        with open(INPUT_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ {len(data.get('articles', []))} articles chargés")
        
        # Génération synthèse
        synthese = generer_synthese_markdown(data)
        
        # Upload vers Google Drive
        uploader_vers_drive(synthese)
        
        print("\n" + "=" * 80)
        print("✅ SYNTHÈSE TERMINÉE")
        print("=" * 80 + "\n")
        
        sys.exit(0)
    
    except FileNotFoundError:
        print(f"❌ Fichier {INPUT_JSON} introuvable")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ ERREUR FATALE : {e}\n")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
