"""
Agent 2 - Synthétiseur Actualités
Modèle : GPT-4o (qualité maximale)
Rôle : Lire JSON filtré → Générer synthèse Markdown → Upload Google Drive
"""

import os
import sys
import json
import traceback
from datetime import datetime, timedelta
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

# Modèle premium pour synthèse
MODEL_SYNTHESE = "gpt-4o-2024-11-20"

# Fichiers
INPUT_JSON = "articles_filtres_news.json"
OUTPUT_MARKDOWN = "VeilleNews.md"


# ================================================================================
# CHARGEMENT DONNÉES
# ================================================================================

def charger_articles_filtres() -> Dict[str, Any]:
    """Charge le JSON produit par Agent 1"""
    if not os.path.exists(INPUT_JSON):
        raise FileNotFoundError(f"❌ Fichier {INPUT_JSON} introuvable")
    
    with open(INPUT_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"✅ JSON chargé : {len(data['articles'])} articles")
    print(f"📊 Thèmes : {', '.join(data.get('themes', {}).keys())}")
    
    return data


# ================================================================================
# GÉNÉRATION SYNTHÈSE
# ================================================================================

def generer_synthese_markdown(data: Dict[str, Any]) -> str:
    """Génère synthèse Markdown avec GPT-4o"""
    
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    # Préparer articles par thème
    articles_par_theme = {}
    for article in data['articles']:
        theme = article['theme']
        if theme not in articles_par_theme:
            articles_par_theme[theme] = []
        articles_par_theme[theme].append(article)
    
    # Créer texte structuré
    articles_text = ""
    for theme, articles in articles_par_theme.items():
        articles_text += f"\n## {theme}\n\n"
        for art in articles:
            articles_text += f"**{art['titre']}**\n"
            articles_text += f"Source: {art['source']} | URL: {art['url']}\n"
            articles_text += f"Snippet: {art['snippet']}\n"
            articles_text += f"Pertinence: {art['pertinence']}/10 | Tags: {', '.join(art['tags'])}\n\n"
    
    date_debut = datetime.strptime(data['periode']['debut'], '%Y-%m-%d')
    date_fin = datetime.strptime(data['periode']['fin'], '%Y-%m-%d')
    
    prompt = f"""Tu es un journaliste expert en actualités françaises et internationales. Tu produis une veille hebdomadaire de très haute qualité pour un cadre supérieur français, ingénieur, vivant à Nantes.

**PÉRIODE ANALYSÉE** : du {date_debut.strftime('%d/%m/%Y')} au {date_fin.strftime('%d/%m/%Y')}

**ARTICLES PRÉ-FILTRÉS À SYNTHÉTISER** :
{articles_text}

**STATISTIQUES** :
- {data['statistiques']['articles_bruts']} articles collectés
- {data['statistiques']['articles_finaux']} articles sélectionnés
- {len(articles_par_theme)} thèmes couverts

**PROFIL DU LECTEUR** :
- Cadre supérieur, ingénieur, Nantes
- Centres d'intérêt : économie, politique, technologie, société, écologie, environnement, mer, littoral, Europe, international, Nantes/Ouest, Bretagne

**FORMAT DE SORTIE MARKDOWN** :
```markdown
---
agent: Veille Actualités (2 agents OpenAI)
date: {date_fin.strftime('%Y-%m-%d')}
catégorie: Actualités Générales
modèles: GPT-4o-mini (collecte) + GPT-4o (synthèse)
---

# **Veille hebdomadaire – Semaine du {date_debut.strftime('%d/%m/%Y')} au {date_fin.strftime('%d/%m/%Y')}**
**Édition [Nom créatif sobre]** *(ex: Édition Atlantique, Chronique des Marées)*

---

## **Introduction**

[Paragraphe de 4-5 lignes résumant :
- Ambiance générale de la semaine
- Tendances clés
- Tensions ou signaux faibles
- Climat médiatique]

---

## **Table des matières**

1. [Thème 1]
2. [Thème 2]
3. [...]
9. Synthèse finale

---

## **[THÈME] – [Titre du sujet]**

### **Résumé**
[Maximum 5 lignes : faits, enjeux, impacts, contexte temporel]

### **Points de vue des médias**

**[Média 1]**
[Angle éditorial, analyse, 3-4 lignes]

**[Média 2]**
[Divergences, critiques, nuances, 3-4 lignes]

**[Média 3]** (si disponible)
[Apport complémentaire, 3-4 lignes]

### **Implications**
- Politiques : [...]
- Économiques : [...]
- Sociales : [...]
- Environnementales : [...]

### **Sources**
- [Titre] – [URL]
- [Titre] – [URL]
- [Titre] – [URL]

---

[Répéter pour chaque thème - couvrir TOUS les articles]

---

## **Synthèse finale**

### **Événements majeurs**
1. [Événement 1]
2. [Événement 2]
3. [...]

### **Divergences éditoriales clés**
- [Différences d'interprétation entre médias]

### **Implications possibles**
- Politiques : [...]
- Économiques : [...]
- Sociales : [...]
- Environnementales : [...]

### **À surveiller la semaine prochaine**
- [Sujet 1]
- [...]

---

**Fin de l'édition**
*Veille générée automatiquement par système 2-agents OpenAI*
*Agent 1 (GPT-4o-mini) : Collecte | Agent 2 (GPT-4o) : Synthèse*
```

**CONSIGNES CRITIQUES** :

1. **Style** : sobre, professionnel, élégant, aucun emoji
2. **Ton** : neutre, factuel, analytique
3. **Sources** : toujours citer avec URLs complètes
4. **Reformulation** : jamais de copier-coller
5. **Neutralité stricte** : présenter faits sans jugement
6. **Exhaustivité** : traiter TOUS les articles fournis
7. **Équilibre** : poids proportionnel à l'importance
8. **Volume** : viser lecture de 10-12 minutes
9. **Nantes/Ouest** : si articles, section dédiée

**IMPORTANT** :
- Scores de pertinence : 8-10 → traitement approfondi, 5-7 → plus bref
- Maintenir cohérence narrative entre sections

**COMMENCE MAINTENANT**

Génère la veille actualités complète en Markdown, sans préambule, directement le contenu final."""

    print("🤖 Génération synthèse Markdown avec GPT-4o...")
    
    try:
        response = client.chat.completions.create(
            model=MODEL_SYNTHESE,
            messages=[
                {
                    "role": "system",
                    "content": "Tu es un journaliste expert en actualités qui produit des veilles hebdomadaires de très haute qualité. Tu réponds UNIQUEMENT en Markdown, sans préambule."
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
        
        # Vérifier clés
        if not OPENAI_API_KEY:
            print("❌ OPENAI_API_KEY manquante")
            sys.exit(1)
        
        if not GOOGLE_CREDENTIALS:
            print("❌ GOOGLE_DRIVE_CREDENTIALS manquantes")
            sys.exit(1)
        
        # Charger données
        print("📂 ÉTAPE 1/3 : Chargement JSON filtré")
        print("-" * 80)
        data = charger_articles_filtres()
        print()
        
        # Générer synthèse
        print("📝 ÉTAPE 2/3 : Génération synthèse Markdown")
        print("-" * 80)
        synthese = generer_synthese_markdown(data)
        print()
        
        # Upload
        print("☁️  ÉTAPE 3/3 : Upload Google Drive")
        print("-" * 80)
        uploader_vers_drive(synthese)
        print()
        
        # Résumé
        print("=" * 80)
        print("✅ AGENT 2 NEWS TERMINÉ AVEC SUCCÈS")
        print("=" * 80)
        print(f"📊 Statistiques :")
        print(f"   - Articles synthétisés : {len(data['articles'])}")
        print(f"   - Thèmes couverts : {len(data.get('themes', {}))}")
        print(f"   - Taille synthèse : {len(synthese)} caractères")
        print()
        print(f"☁️  Fichier Google Drive : {OUTPUT_MARKDOWN}")
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
