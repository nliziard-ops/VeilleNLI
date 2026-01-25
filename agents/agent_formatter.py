"""
Agent Formatter
Modèle : GPT-4o-mini (économique)
Rôle : Fusionner research_ia.md + research_news.md → VeilleIA.md et VeilleNews.md formatés
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

# Modèle économique pour mise en forme
MODEL_FORMATTER = "gpt-4o-mini-2024-07-18"

# Fichiers d'entrée (générés par Deep Research)
INPUT_RESEARCH_IA = "research_ia.md"
INPUT_RESEARCH_NEWS = "research_news.md"

# Fichiers de sortie
OUTPUT_VEILLE_IA = "VeilleIA.md"
OUTPUT_VEILLE_NEWS = "VeilleNews.md"


# ================================================================================
# CHARGEMENT DES RECHERCHES
# ================================================================================

def charger_research(filepath: str) -> str:
    """
    Charge un fichier Markdown de recherche
    
    Args:
        filepath: Chemin du fichier
        
    Returns:
        Contenu Markdown
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"❌ Fichier {filepath} introuvable")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"✅ Fichier chargé : {filepath} ({len(content)} caractères)")
    return content


# ================================================================================
# MISE EN FORME VEILLE IA
# ================================================================================

def formatter_veille_ia(research_content: str) -> str:
    """
    Transforme research_ia.md en VeilleIA.md au format attendu
    
    Args:
        research_content: Contenu brut de la recherche Deep
        
    Returns:
        Markdown formaté selon le template VeilleIA
    """
    
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    date_fin = datetime.now()
    date_debut = date_fin - timedelta(days=7)
    
    prompt = f"""Tu es un éditeur expert qui transforme une recherche brute en synthèse élégante.

**CONTENU BRUT À TRAITER** :
{research_content}

**TA MISSION** :
Transformer cette recherche en une synthèse Markdown structurée selon le format ci-dessous.

**STRUCTURE ATTENDUE** :

```markdown
---
agent: Deep Research IA (OpenAI Extended Thinking)
date: {date_fin.strftime('%Y-%m-%d')}
catégorie: Intelligence Artificielle
modèle: o1-2024-12-17
---

# Veille IA & LLM – Semaine du {date_debut.strftime('%d/%m/%Y')} au {date_fin.strftime('%d/%m/%Y')}

**Édition [Nom créatif sobre basé sur tendance de la semaine]**

---

## Introduction

[4-5 lignes : climat de la semaine IA, tendances clés, signaux faibles détectés]

---

## [SUJET 1/6] – [Titre accrocheur basé sur l'article le plus pertinent]

### Résumé
[5 lignes max : faits essentiels, enjeux, impacts]

### Points de vue croisés

**[Source 1]**
[Angle éditorial, analyse, 3-4 lignes]

**[Source 2]** (si disponible dans la recherche)
[Divergences, critiques, 3-4 lignes]

**[Source 3]** (si disponible)
[Apport complémentaire, 3-4 lignes]

### Analyse & implications
- Impacts sectoriels : [...]
- Opportunités : [...]
- Risques potentiels : [...]

### Signaux faibles
- [Points incertains, rumeurs, indicateurs émergents]

### Sources
- [Titre] – [URL complète]

---

[RÉPÉTER POUR SUJETS 2, 3, 4, 5, 6 - Sélectionner les 6 articles les PLUS PERTINENTS]

---

## Autres sujets de la semaine

### [Titre court sujet A]
**Thème** : [Thème]
**Résumé** : [2-3 lignes]
**Source** : [Nom média] – [URL]

### [Titre court sujet B]
[...]

[Continuer pour TOUS les autres articles de la recherche]

---

## Synthèse finale

### Points clés de la semaine
1. [Point 1]
2. [Point 2]
3. [Point 3]

### Divergences d'analyse notables
- [Différences entre sources si détectées]

### Signaux faibles & opportunités
- [Tendances émergentes, innovations en gestation]

### Risques & menaces
- [Points d'attention, controverses]

### À surveiller la semaine prochaine
- [Sujets en développement, annonces attendues]

---

**Fin de l'édition**
*Veille générée par Deep Research OpenAI o1*
```

**CONSIGNES CRITIQUES** :

1. **Sélection Top 6** : Choisis les 6 articles LES PLUS PERTINENTS (score 8-10) de la recherche
2. **Autres sujets** : Liste TOUS les autres articles en format bref
3. **Style** : Sobre, professionnel, élégant, ZÉRO emoji
4. **Sources** : URLs complètes OBLIGATOIRES
5. **Reformulation** : JAMAIS de copier-coller exact
6. **Équilibre** : Top 6 = 75% du contenu, Autres = 15%, Synthèse = 10%
7. **Nom d'édition** : Sobre et lié à la tendance principale (ex: "Édition Reasoning", "Édition Multimodal")

**IMPORTANT** :
- Maintenir cohérence narrative
- Extraire vraies divergences entre sources
- Signaux faibles = indices subtils de tendances futures
- Synthèse finale doit apporter une vraie plus-value analytique

Génère le Markdown complet maintenant, sans préambule.
"""

    print("🤖 Mise en forme Veille IA avec GPT-4o-mini...")
    
    try:
        response = client.chat.completions.create(
            model=MODEL_FORMATTER,
            messages=[
                {
                    "role": "system",
                    "content": "Tu es un éditeur expert en synthèse IA. Tu réponds UNIQUEMENT en Markdown, sans préambule."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=8000
        )
        
        markdown_content = response.choices[0].message.content.strip()
        
        # Nettoyer les backticks markdown si présents
        if markdown_content.startswith('```markdown'):
            lines = markdown_content.split('\n')
            markdown_content = '\n'.join(lines[1:-1]) if len(lines) > 2 else markdown_content
            markdown_content = markdown_content.replace('```markdown', '').replace('```', '').strip()
        
        print(f"✅ Mise en forme terminée")
        print(f"📊 Tokens utilisés : {response.usage.total_tokens}")
        
        cost_input = (response.usage.prompt_tokens / 1000) * 0.00015
        cost_output = (response.usage.completion_tokens / 1000) * 0.0006
        cost_total = cost_input + cost_output
        
        print(f"💰 Coût estimé : ${cost_total:.4f}")
        
        return markdown_content
    
    except Exception as e:
        print(f"❌ Erreur GPT-4o-mini : {e}")
        traceback.print_exc()
        raise


# ================================================================================
# MISE EN FORME VEILLE NEWS
# ================================================================================

def formatter_veille_news(research_content: str) -> str:
    """
    Transforme research_news.md en VeilleNews.md au format attendu
    
    Args:
        research_content: Contenu brut de la recherche Deep
        
    Returns:
        Markdown formaté selon le template VeilleNews
    """
    
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    date_fin = datetime.now()
    date_debut = date_fin - timedelta(days=7)
    
    prompt = f"""Tu es un éditeur expert qui transforme une recherche brute en synthèse élégante.

**CONTENU BRUT À TRAITER** :
{research_content}

**TA MISSION** :
Transformer cette recherche en une synthèse Markdown structurée selon le format ci-dessous.

**STRUCTURE ATTENDUE** :

```markdown
---
agent: Deep Research News (OpenAI Extended Thinking)
date: {date_fin.strftime('%Y-%m-%d')}
catégorie: Actualités
modèle: o1-2024-12-17
---

# Actualités – Semaine du {date_debut.strftime('%d/%m/%Y')} au {date_fin.strftime('%d/%m/%Y')}

**Édition [Nom créatif sobre basé sur événement marquant]**

---

## Introduction

[4-5 lignes : climat de la semaine, événements marquants, ton général]

---

## [SUJET 1/6] – [Titre accrocheur de l'événement le plus important]

### Résumé
[5 lignes max : faits, contexte, conséquences]

### Contexte et enjeux
[4-5 lignes : mise en perspective, historique si pertinent]

### Points de vue croisés

**[Source 1]**
[Angle éditorial, 3-4 lignes]

**[Source 2]** (si disponible)
[Autre perspective, 3-4 lignes]

### Implications
- [Impacts politiques/économiques/sociaux]
- [Conséquences locales/nationales/internationales]

### Sources
- [Titre] – [URL complète]

---

[RÉPÉTER POUR SUJETS 2, 3, 4, 5, 6 - Sélectionner les 6 PLUS IMPORTANTS]

---

## Autres actualités de la semaine

### [Titre court actualité A]
**Catégorie** : [International/National/Local/Sport]
**Résumé** : [2-3 lignes]
**Source** : [Nom média] – [URL]

### [Titre court actualité B]
[...]

[Continuer pour TOUS les autres articles]

---

## Synthèse finale

### Faits marquants de la semaine
1. [Événement 1]
2. [Événement 2]
3. [Événement 3]

### Tendances observées
- [Tendances politiques/économiques/sociales]

### Focus local Bretagne & Pays de la Loire
- [Résumé des actualités régionales importantes]

### Focus sport maritime
- [Résumé des événements voile/surf/sports nautiques]

### À suivre la semaine prochaine
- [Événements attendus, développements à surveiller]

---

**Fin de l'édition**
*Veille générée par Deep Research OpenAI o1*
```

**CONSIGNES CRITIQUES** :

1. **Sélection Top 6** : Choisis les 6 événements LES PLUS IMPORTANTS (pertinence 8-10)
2. **Équilibre** : Mélanger International/National/Local dans le Top 6
3. **Sport maritime** : Au moins 1 sujet dans le Top 6 si actualité forte
4. **Autres actualités** : Lister TOUS les autres articles en format bref
5. **Style** : Journalistique sobre, ZÉRO emoji
6. **URLs complètes** : OBLIGATOIRE
7. **Reformulation** : JAMAIS de copier-coller

**IMPORTANT** :
- Synthèse finale doit valoriser actualités locales ET sport maritime
- Nom d'édition sobre lié à l'événement principal
- Maintenir équilibre géographique et thématique

Génère le Markdown complet maintenant, sans préambule.
"""

    print("🤖 Mise en forme Veille News avec GPT-4o-mini...")
    
    try:
        response = client.chat.completions.create(
            model=MODEL_FORMATTER,
            messages=[
                {
                    "role": "system",
                    "content": "Tu es un éditeur expert en synthèse actualités. Tu réponds UNIQUEMENT en Markdown, sans préambule."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=8000
        )
        
        markdown_content = response.choices[0].message.content.strip()
        
        # Nettoyer les backticks
        if markdown_content.startswith('```markdown'):
            lines = markdown_content.split('\n')
            markdown_content = '\n'.join(lines[1:-1]) if len(lines) > 2 else markdown_content
            markdown_content = markdown_content.replace('```markdown', '').replace('```', '').strip()
        
        print(f"✅ Mise en forme terminée")
        print(f"📊 Tokens utilisés : {response.usage.total_tokens}")
        
        cost_input = (response.usage.prompt_tokens / 1000) * 0.00015
        cost_output = (response.usage.completion_tokens / 1000) * 0.0006
        cost_total = cost_input + cost_output
        
        print(f"💰 Coût estimé : ${cost_total:.4f}")
        
        return markdown_content
    
    except Exception as e:
        print(f"❌ Erreur GPT-4o-mini : {e}")
        traceback.print_exc()
        raise


# ================================================================================
# UPLOAD GOOGLE DRIVE
# ================================================================================

def uploader_vers_drive(contenu_markdown: str, filename: str) -> None:
    """
    Upload vers Google Drive
    
    Args:
        contenu_markdown: Contenu à uploader
        filename: Nom du fichier (VeilleIA.md ou VeilleNews.md)
    """
    
    print(f"☁️  Upload vers Google Drive : {filename}...")
    
    credentials = service_account.Credentials.from_service_account_info(
        GOOGLE_CREDENTIALS,
        scopes=['https://www.googleapis.com/auth/drive']
    )
    
    service = build('drive', 'v3', credentials=credentials)
    
    query = f"name='{filename}' and '{FOLDER_ID}' in parents"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])
    
    file_metadata = {'name': filename}
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
        print(f"✅ Fichier {filename} mis à jour sur Google Drive")
    else:
        file_metadata['parents'] = [FOLDER_ID]
        service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        print(f"✅ Fichier {filename} créé sur Google Drive")


# ================================================================================
# MAIN
# ================================================================================

def main():
    """Point d'entrée principal"""
    
    try:
        print("=" * 80)
        print("📝 AGENT FORMATTER - Mise en forme finale")
        print("=" * 80)
        print(f"⏰ Exécution : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print()
        
        if not OPENAI_API_KEY:
            print("❌ OPENAI_API_KEY manquante")
            sys.exit(1)
        
        if not GOOGLE_CREDENTIALS:
            print("❌ GOOGLE_DRIVE_CREDENTIALS manquantes")
            sys.exit(1)
        
        # ========== TRAITEMENT VEILLE IA ==========
        print("📂 PARTIE 1/2 : VEILLE IA")
        print("-" * 80)
        
        print("📖 Chargement de la recherche IA...")
        research_ia = charger_research(INPUT_RESEARCH_IA)
        
        print("🎨 Mise en forme VeilleIA.md...")
        veille_ia = formatter_veille_ia(research_ia)
        
        print("☁️  Upload Google Drive...")
        uploader_vers_drive(veille_ia, OUTPUT_VEILLE_IA)
        print()
        
        # ========== TRAITEMENT VEILLE NEWS ==========
        print("📂 PARTIE 2/2 : VEILLE NEWS")
        print("-" * 80)
        
        print("📖 Chargement de la recherche News...")
        research_news = charger_research(INPUT_RESEARCH_NEWS)
        
        print("🎨 Mise en forme VeilleNews.md...")
        veille_news = formatter_veille_news(research_news)
        
        print("☁️  Upload Google Drive...")
        uploader_vers_drive(veille_news, OUTPUT_VEILLE_NEWS)
        print()
        
        # ========== RÉSUMÉ ==========
        print("=" * 80)
        print("✅ AGENT FORMATTER TERMINÉ")
        print("=" * 80)
        print(f"📄 {OUTPUT_VEILLE_IA} → Google Drive")
        print(f"📄 {OUTPUT_VEILLE_NEWS} → Google Drive")
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
