"""
Agent 3 - Synthèse IA (ANALYSE COMPLÈTE)
Modèle : GPT-5.2 Pro (OpenAI Responses API)
Rôle : Analyse TOUS les articles bruts, sélectionne Top 6 + max 30 autres, génère markdown structuré
Critères sélection : Couverture multi-sources → Impact potentiel → Importance/buzz
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

# ============================================
# CONFIGURATION
# ============================================
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
GOOGLE_CREDENTIALS = json.loads(os.environ.get('GOOGLE_DRIVE_CREDENTIALS'))
FOLDER_ID = os.environ.get('GOOGLE_DRIVE_FOLDER_ID')

MODEL_SYNTHESE = "gpt-5.2-pro"
INPUT_JSON = "recherche_ia_brute.json"
OUTPUT_MARKDOWN = "VeilleIA.md"

# ============================================
# FONCTION PRINCIPALE
# ============================================
def generer_synthese_markdown(data: Dict[str, Any]) -> str:
    """
    Analyse TOUS les articles bruts et génère markdown structuré.
    
    Traitement :
    1. Parcourt TOUS les articles
    2. Sélectionne Top 6 selon : Couverture multi-sources → Impact → Importance
    3. Classe max 30 autres articles par pertinence
    4. Génère markdown selon template exact
    
    Args:
        data: JSON brut de l'agent Recherche
        
    Returns:
        Contenu markdown formaté
    """
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    articles = data.get('articles', [])
    if len(articles) == 0:
        return """# Veille IA – Semaine du XX au XX

Aucune actualité collectée cette semaine.

---

**Fin de l'édition**
*Veille générée par OpenAI GPT-5.2 Pro*"""
    
    # Construction du texte complet des articles pour l'analyse
    articles_text = f"## ARTICLES COLLECTÉS ({len(articles)} au total)\n\n"
    for i, art in enumerate(articles, 1):
        articles_text += f"### Article {i}\n"
        articles_text += f"**ID**: {art.get('id', 'N/A')}\n"
        articles_text += f"**Titre**: {art.get('titre', 'N/A')}\n"
        articles_text += f"**Source**: {art.get('source', 'N/A')}\n"
        articles_text += f"**URL**: {art.get('url', 'N/A')}\n"
        articles_text += f"**Date**: {art.get('date_publication', 'N/A')}\n"
        articles_text += f"**Contenu**:\n{art.get('contenu_brut', 'N/A')}\n\n"
        articles_text += "---\n\n"
    
    periode = data.get('periode', {})
    date_debut = periode.get('debut', 'XX/XX/XXXX')
    date_fin = periode.get('fin', 'XX/XX/XXXX')
    
    # Prompt d'analyse complète
    prompt = f"""Tu es un analyste expert en Intelligence Artificielle et LLM.

Tu reçois {len(articles)} articles bruts collectés du {date_debut} au {date_fin}.

{articles_text}

## MISSION

Analyse TOUS ces articles et génère un rapport markdown structuré selon le template EXACT suivant :

## ÉTAPE 1 : SÉLECTION TOP 6
Critères (dans cet ordre) :
1. **Couverture multi-sources** : Sujets mentionnés par plusieurs sources différentes
2. **Impact potentiel** : Technologies/annonces qui vont avoir un impact majeur
3. **Importance/buzz** : Sujets qui font le plus parler

Répartition souhaitée : 3 tendances buzz + 3 sujets techniques/recherche

## ÉTAPE 2 : AUTRES SUJETS
- Maximum 30 articles restants
- Classés par pertinence décroissante
- Format compact (titre + thème + résumé 1-2 lignes + source + URL)

## TEMPLATE MARKDOWN STRICT

```markdown
---
agent: Synthèse IA (OpenAI GPT-5.2 Pro)
date: {datetime.now().strftime('%Y-%m-%d')}
catégorie: Intelligence Artificielle
modèle: {MODEL_SYNTHESE}
---

# Veille IA & LLM – Semaine du {date_debut} au {date_fin}

**Édition [Thème de la semaine]**

---

## Introduction

[Synthèse globale de la semaine : principales tendances, signaux faibles, contexte général. 4-5 lignes.]

---

## [SUJET 1/6] – [Titre du sujet]

### Résumé
[3-4 lignes décrivant l'essentiel du sujet]

### Points de vue croisés

**[Source 1]**
[Analyse du point de vue de cette source, 2-3 lignes]

**[Source 2]**
[Analyse du point de vue de cette source, 2-3 lignes]

**[Source 3]** (si applicable)
[Analyse du point de vue de cette source, 2-3 lignes]

### Analyse & implications
- **Impacts sectoriels** : [Conséquences pour les entreprises/industrie]
- **Opportunités** : [Opportunités business/technologiques]
- **Risques potentiels** : [Risques identifiés]

### Signaux faibles
- [Signal faible 1]
- [Signal faible 2]

### Sources
- "Titre article 1" – URL1
- "Titre article 2" – URL2

---

[... RÉPÉTER pour SUJET 2/6, 3/6, 4/6, 5/6, 6/6 ...]

---

## Autres sujets de la semaine

### [Titre sujet secondaire 1]
**Thème** : [Catégorie]
**Résumé** : [1-2 lignes]
**Source** : [Nom source] – URL

### [Titre sujet secondaire 2]
**Thème** : [Catégorie]
**Résumé** : [1-2 lignes]
**Source** : [Nom source] – URL

[... Jusqu'à 30 sujets maximum, classés par pertinence décroissante ...]

---

## Synthèse finale

### Points clés de la semaine
1. [Point clé 1]
2. [Point clé 2]
3. [Point clé 3]

### Divergences d'analyse notables
[Si des sources présentent des analyses contradictoires]

### Signaux faibles & opportunités
[Tendances émergentes à surveiller]

### Risques & menaces
[Risques identifiés dans les actualités]

### À surveiller la semaine prochaine
[Éléments à suivre de près]

---

**Fin de l'édition**
*Veille générée par OpenAI GPT-5.2 Pro*
```

## RÈGLES STRICTES
- Respecte EXACTEMENT le template ci-dessus
- Aucun emoji
- Markdown propre et structuré
- Pour chaque sujet principal : résumé + points de vue croisés + analyse + signaux faibles + sources
- Autres sujets : format compact
- Synthèse finale obligatoire

Génère le markdown complet maintenant."""

    print("🤖 GPT-5.2 Pro - Analyse complète en cours...")
    
    try:
        # Appel API OpenAI Responses
        response = client.responses.create(
            model=MODEL_SYNTHESE,
            input=prompt,
            max_tokens=16000  # Budget large pour synthèse complète
        )
        
        tokens_utilises = response.usage.total_tokens
        print(f"📊 Tokens utilisés : {tokens_utilises}")
        
        markdown_content = response.output_text.strip()
        
        # Nettoyage markdown (suppression des balises ```markdown si présentes)
        if markdown_content.startswith('```'):
            lines = markdown_content.split('\n')
            markdown_content = '\n'.join(lines[1:-1]) if len(lines) > 2 else markdown_content
            markdown_content = markdown_content.replace('```markdown', '').replace('```', '').strip()
        
        print(f"✅ Markdown généré ({len(markdown_content)} caractères)")
        return markdown_content
    
    except Exception as e:
        print(f"❌ Erreur génération markdown : {e}")
        traceback.print_exc()
        raise

# ============================================
# UPLOAD GOOGLE DRIVE
# ============================================
def uploader_vers_drive(contenu: str) -> None:
    """
    Upload le fichier markdown vers Google Drive.
    
    Args:
        contenu: Contenu markdown à uploader
    """
    print("📤 Upload vers Google Drive...")
    
    credentials = service_account.Credentials.from_service_account_info(
        GOOGLE_CREDENTIALS,
        scopes=['https://www.googleapis.com/auth/drive']
    )
    service = build('drive', 'v3', credentials=credentials)
    
    # Recherche fichier existant
    query = f"name='{OUTPUT_MARKDOWN}' and '{FOLDER_ID}' in parents"
    results = service.files().list(q=query, fields="files(id)").execute()
    files = results.get('files', [])
    
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
        created_file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        print(f"✅ {OUTPUT_MARKDOWN} créé (ID: {created_file.get('id')})")

# ============================================
# MAIN
# ============================================
def main():
    """Point d'entrée principal"""
    try:
        print("=" * 80)
        print("🤖 AGENT 3 - SYNTHÈSE IA (ANALYSE COMPLÈTE)")
        print("=" * 80)
        print(f"Modèle : {MODEL_SYNTHESE}")
        print(f"Mode : Analyse + Sélection + Génération markdown")
        print("=" * 80)
        
        # Lecture JSON brut
        print(f"\n📥 Lecture {INPUT_JSON}...")
        with open(INPUT_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        nb_articles = len(data.get('articles', []))
        print(f"✅ {nb_articles} articles bruts chargés")
        
        # Génération synthèse
        print("\n🔄 Génération synthèse markdown...")
        synthese = generer_synthese_markdown(data)
        
        # Upload vers Google Drive
        print("\n📤 Upload vers Google Drive...")
        uploader_vers_drive(synthese)
        
        print("\n✅ SYNTHÈSE TERMINÉE")
        print(f"📄 Fichier : {OUTPUT_MARKDOWN}")
        print(f"📊 Longueur : {len(synthese)} caractères")
        
        sys.exit(0)
    
    except FileNotFoundError:
        print(f"\n❌ ERREUR : {INPUT_JSON} introuvable")
        print("Vérifiez que l'agent Recherche a bien été exécuté avant.")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ ÉCHEC : {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
