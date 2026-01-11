"""
Agent 2 - Synthétiseur News
Modèle : GPT-4o (qualité maximale)
Rôle : Lire JSON filtré → Générer synthèse Markdown → Upload Google Drive
Structure : 6 sujets détaillés + autres sujets en bref
"""

import os
import json
import sys
import traceback
from datetime import datetime, timedelta
from typing import Dict, Any, List
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

# Modèle premium pour synthèse qualitative
MODEL_SYNTHESE = "gpt-4o-2024-11-20"

# Fichiers d'entrée/sortie
INPUT_JSON = "articles_filtres_news.json"
OUTPUT_MARKDOWN = "VeilleNews.md"


# ================================================================================
# CHARGEMENT DONNÉES FILTRÉES
# ================================================================================

def charger_articles_filtres() -> Dict[str, Any]:
    """Charge le JSON produit par Agent 1"""
    if not os.path.exists(INPUT_JSON):
        raise FileNotFoundError(f"❌ Fichier {INPUT_JSON} introuvable")
    
    with open(INPUT_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"✅ JSON chargé : {len(data['articles'])} articles")
    return data


# ================================================================================
# TRI ET SÉLECTION DES ARTICLES
# ================================================================================

def trier_articles(articles: List[Dict[str, Any]]) -> tuple:
    """
    Trie les articles par pertinence et sépare en 2 groupes
    Returns: (top_6, autres)
    """
    # Trier par pertinence décroissante
    articles_tries = sorted(articles, key=lambda x: x['pertinence'], reverse=True)
    
    # Séparer
    top_6 = articles_tries[:6]
    autres = articles_tries[6:]
    
    print(f"📊 Top 6 articles : {len(top_6)}")
    print(f"📊 Autres sujets : {len(autres)}")
    
    return top_6, autres


# ================================================================================
# GÉNÉRATION SYNTHÈSE MARKDOWN GPT-4o
# ================================================================================

def generer_synthese_markdown(data: Dict[str, Any]) -> str:
    """Utilise GPT-4o pour générer une synthèse Markdown avec structure 6+autres"""
    
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    # Trier les articles
    top_6, autres = trier_articles(data['articles'])
    
    # Préparer texte TOP 6
    top_6_text = ""
    for i, art in enumerate(top_6, 1):
        top_6_text += f"\n**[{i}] {art['titre']}**\n"
        top_6_text += f"Source: {art['source']} | URL: {art['url']}\n"
        top_6_text += f"Thème: {art['theme']}\n"
        top_6_text += f"Snippet: {art['snippet']}\n"
        top_6_text += f"Pertinence: {art['pertinence']}/10 | Tags: {', '.join(art['tags'])}\n\n"
    
    # Préparer texte AUTRES
    autres_text = ""
    for art in autres:
        autres_text += f"\n**{art['titre']}**\n"
        autres_text += f"Source: {art['source']} | URL: {art['url']}\n"
        autres_text += f"Thème: {art['theme']}\n"
        autres_text += f"Snippet: {art['snippet'][:150]}...\n"
        autres_text += f"Pertinence: {art['pertinence']}/10\n\n"
    
    date_debut = datetime.strptime(data['periode']['debut'], '%Y-%m-%d')
    date_fin = datetime.strptime(data['periode']['fin'], '%Y-%m-%d')
    
    prompt = f"""Tu es un journaliste expert en actualités françaises/internationales qui produit une veille hebdomadaire pour un cadre supérieur français, ingénieur, vivant à Nantes.

**PÉRIODE** : du {date_debut.strftime('%d/%m/%Y')} au {date_fin.strftime('%d/%m/%Y')}

**ARTICLES PRINCIPAUX (Top 6 - traitement détaillé)** :
{top_6_text}

**AUTRES ARTICLES (traitement bref)** :
{autres_text}

**STRUCTURE DU MARKDOWN À GÉNÉRER** :

```markdown
---
agent: Veille Actualités (2 agents OpenAI)
date: {date_fin.strftime('%Y-%m-%d')}
catégorie: Actualités Générales
modèles: GPT-4o-mini (collecte) + GPT-4o (synthèse)
---

# Veille hebdomadaire – Semaine du {date_debut.strftime('%d/%m/%Y')} au {date_fin.strftime('%d/%m/%Y')}

**Édition [Nom créatif sobre]**

---

## Introduction

[4-5 lignes : ambiance générale, tendances, tensions, climat médiatique]

---

## [SUJET 1/6] – [Titre accrocheur]

### Résumé
[5 lignes max : faits essentiels, enjeux, impacts]

### Points de vue des médias

**[Média 1]**
[Angle éditorial, ton, analyse, 3-4 lignes]

**[Média 2]**
[Divergences, critiques, 3-4 lignes]

**[Média 3]** (si disponible)
[Analyse complémentaire, 3-4 lignes]

### Implications
- Politiques : [...]
- Économiques : [...]
- Sociales : [...]
- Environnementales : [...]

### Sources
- [Titre] – [URL complète]

---

[RÉPÉTER POUR SUJETS 2, 3, 4, 5, 6]

---

## Autres sujets de la semaine

### [Titre court sujet A]
**Thème** : [Thème]
**Résumé** : [2-3 lignes]
**Source** : [Nom média] – [URL]

### [Titre court sujet B]
**Thème** : [Thème]
**Résumé** : [2-3 lignes]
**Source** : [Nom média] – [URL]

[Continuer pour tous les autres articles]

---

## Synthèse finale

### Événements majeurs
1. [Point 1]
2. [Point 2]
3. [Point 3]

### Divergences éditoriales clés
- [Différences d'interprétation entre médias]

### Implications possibles
- Politiques : [...]
- Économiques : [...]
- Sociales : [...]
- Environnementales : [...]

### À surveiller la semaine prochaine
- [Sujet 1]
- [Sujet 2]

---

**Fin de l'édition**
*Veille générée automatiquement par système 2-agents OpenAI*
```

**CONSIGNES CRITIQUES** :

1. **Top 6** : Traitement COMPLET avec résumé, points de vue médias, implications, sources
2. **Autres sujets** : Format BREF avec thème, résumé court (2-3 lignes), source unique
3. **Style** : Sobre, professionnel, élégant, pas d'emoji
4. **Sources** : URLs complètes obligatoires
5. **Reformulation** : Jamais de copier-coller
6. **Neutralité stricte** : Présenter faits sans jugement
7. **Équilibre** : Top 6 = 80% du contenu, Autres = 20%

**IMPORTANT** :
- Les 6 premiers sujets doivent être ultra-détaillés
- Les autres sujets sont juste listés pour traçabilité
- Maintenir cohérence narrative

Génère le Markdown complet maintenant, sans préambule."""

    print("🤖 Génération synthèse Markdown avec GPT-4o...")
    
    try:
        response = client.chat.completions.create(
            model=MODEL_SYNTHESE,
            messages=[
                {
                    "role": "system",
                    "content": "Tu es un journaliste expert en actualités. Tu réponds UNIQUEMENT en Markdown, sans préambule."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=6000
        )
        
        markdown_content = response.choices[0].message.content.strip()
        
        print(f"📊 Tokens utilisés : {response.usage.total_tokens}")
        
        cost_input = (response.usage.prompt_tokens / 1000) * 0.03
        cost_output = (response.usage.completion_tokens / 1000) * 0.06
        cost_total = cost_input + cost_output
        print(f"💰 Coût estimé : ${cost_total:.4f}")
        
        print(f"✅ Synthèse générée : {len(markdown_content)} caractères")
        
        return markdown_content
    
    except Exception as e:
        print(f"❌ Erreur GPT-4o : {e}")
        traceback.print_exc()
        raise


# ================================================================================
# UPLOAD GOOGLE DRIVE
# ================================================================================

def uploader_vers_drive(contenu_markdown: str) -> None:
    """Upload vers Google Drive"""
    
    print("☁️  Upload vers Google Drive...")
    
    credentials = service_account.Credentials.from_service_account_info(
        GOOGLE_CREDENTIALS,
        scopes=['https://www.googleapis.com/auth/drive']
    )
    
    service = build('drive', 'v3', credentials=credentials)
    
    query = f"name='{OUTPUT_MARKDOWN}' and '{FOLDER_ID}' in parents"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])
    
    file_metadata = {'name': OUTPUT_MARKDOWN}
    media = MediaIoBaseUpload(
        io.BytesIO(contenu_markdown.encode('utf-8')),
        mimetype='text/markdown',
        resumable=True
    )
    
    if files:
        file_id = files[0]['id']
        service.files().update(
            fileId=file_id,
            media_body=media
        ).execute()
        print(f"✅ Fichier {OUTPUT_MARKDOWN} mis à jour sur Google Drive")
    else:
        file_metadata['parents'] = [FOLDER_ID]
        service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        print(f"✅ Fichier {OUTPUT_MARKDOWN} créé sur Google Drive")


# ================================================================================
# MAIN
# ================================================================================

def main():
    """Point d'entrée principal"""
    
    try:
        print("=" * 80)
        print("🤖 AGENT 2 - SYNTHÉTISEUR NEWS (GPT-4o)")
        print("=" * 80)
        print(f"⏰ Exécution : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print()
        
        if not OPENAI_API_KEY:
            print("❌ OPENAI_API_KEY manquante")
            sys.exit(1)
        
        if not GOOGLE_CREDENTIALS:
            print("❌ GOOGLE_DRIVE_CREDENTIALS manquantes")
            sys.exit(1)
        
        print("📂 ÉTAPE 1/3 : Chargement JSON filtré")
        print("-" * 80)
        data = charger_articles_filtres()
        print()
        
        print("📝 ÉTAPE 2/3 : Génération synthèse (6 détaillés + autres)")
        print("-" * 80)
        synthese = generer_synthese_markdown(data)
        print()
        
        print("☁️  ÉTAPE 3/3 : Upload Google Drive")
        print("-" * 80)
        uploader_vers_drive(synthese)
        print()
        
        print("=" * 80)
        print("✅ AGENT 2 NEWS TERMINÉ AVEC SUCCÈS")
        print("=" * 80)
        print(f"📊 {len(data['articles'])} articles synthétisés")
        print(f"☁️  Fichier : {OUTPUT_MARKDOWN}")
        print()
        
        sys.exit(0)
    
    except Exception as e:
        print("\n" + "=" * 80)
        print("❌ ERREUR FATALE")
        print("=" * 80)
        print(f"Type : {type(e).__name__}")
        print(f"Message : {e}")
        traceback.print_exc()
        print("=" * 80)
        sys.exit(1)


if __name__ == "__main__":
    main()
