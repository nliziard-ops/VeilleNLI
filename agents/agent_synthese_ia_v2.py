"""
Agent 3 - Synthèse IA
Modèle : GPT-4 Turbo (ChatGPT)
Rôle : Analyser recherche brute → Sélectionner 6 sujets principaux → Synthétiser avec divergences sources

Sélection 6 sujets :
- 3 premiers : Tendances qui font parler (buzz, controverses, ruptures)
- 3 suivants : Sujets technologiques (avancées, modèles, hardware)

Structure par sujet : Résumé court, synthèse approfondie, divergences entre sources, toutes sources citées
Autres sujets : Liste compacte avec titre, résumé court, source unique
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

# Modèle ChatGPT-4 Turbo pour synthèse analytique
MODEL_SYNTHESE = "gpt-4-turbo-preview"

# Fichiers
INPUT_JSON = "recherche_ia_brute.json"
OUTPUT_MARKDOWN = "VeilleIA.md"


# ================================================================================
# CHARGEMENT DONNÉES RECHERCHE
# ================================================================================

def charger_recherche_brute() -> Dict[str, Any]:
    """Charge le JSON produit par Agent 1 (Recherche IA)"""
    if not os.path.exists(INPUT_JSON):
        raise FileNotFoundError(f"❌ Fichier {INPUT_JSON} introuvable")
    
    with open(INPUT_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"✅ JSON chargé : {len(data.get('articles', []))} articles")
    return data


# ================================================================================
# GÉNÉRATION SYNTHÈSE MARKDOWN GPT-4 TURBO
# ================================================================================

def generer_synthese_markdown(data: Dict[str, Any]) -> str:
    """
    Utilise GPT-4 Turbo pour :
    1. Sélectionner 6 sujets prioritaires (3 tendances + 3 tech)
    2. Synthétiser en profondeur avec divergences sources
    3. Lister les autres sujets en mode compact
    """
    
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    articles = data.get('articles', [])
    
    if len(articles) == 0:
        print("⚠️  Aucun article à synthétiser")
        return "# Veille IA\n\nAucune actualité collectée cette semaine.\n"
    
    # Préparer texte articles bruts
    articles_text = ""
    for i, art in enumerate(articles, 1):
        articles_text += f"\n**[{i}] {art.get('titre', 'Sans titre')}**\n"
        articles_text += f"Catégorie: {art.get('categorie', 'Non classé')}\n"
        articles_text += f"Source: {art.get('source', 'Inconnue')} | URL: {art.get('url', '#')}\n"
        articles_text += f"Résumé court: {art.get('resume_court', '')}\n"
        articles_text += f"Synthèse complète:\n{art.get('synthese_complete', '')}\n\n"
    
    date_debut = data.get('periode', {}).get('debut', datetime.now().strftime('%Y-%m-%d'))
    date_fin = data.get('periode', {}).get('fin', datetime.now().strftime('%Y-%m-%d'))
    
    prompt = f"""Tu es un analyste expert en Intelligence Artificielle qui produit une veille hebdomadaire pour un cadre supérieur français, ingénieur, vivant à Nantes.

**PÉRIODE** : du {date_debut} au {date_fin}

**ARTICLES COLLECTÉS (recherche brute factuelle)** :
{articles_text}

**TA MISSION - SÉLECTION ET SYNTHÈSE** :

1. **Sélectionner 6 sujets principaux** parmi tous les articles :
   - **3 premiers sujets** : TENDANCES QUI FONT PARLER (buzz médiatique, controverses, ruptures stratégiques, annonces marquantes)
   - **3 sujets suivants** : SUJETS TECHNOLOGIQUES (avancées techniques, nouveaux modèles, hardware, recherche scientifique)

2. **Pour chaque sujet des 6** :
   - **Résumé court** (3-4 lignes max) : L'essentiel à retenir
   - **Synthèse approfondie** (15-25 lignes) : 
     * Contexte et enjeux
     * Faits clés et chiffres
     * Impacts sectoriels
     * Analyse critique
   - **Divergences entre sources** : Points de désaccord, angles différents, débats
   - **Sources citées** : TOUTES les sources utilisées avec URLs complètes

3. **Pour les autres sujets** (en liste compacte) :
   - Titre court
   - Résumé court (2-3 lignes max)
   - Synthèse (5-8 lignes)
   - Source avec URL (une seule source principale)

**STRUCTURE MARKDOWN OBLIGATOIRE** :

```markdown
---
agent: Synthèse IA (2-agents OpenAI pipeline)
date: {date_fin}
catégorie: Intelligence Artificielle
modèles: GPT-4 Turbo (recherche + synthèse)
---

# Veille IA & LLM – Semaine du {date_debut} au {date_fin}

**Édition [Nom sobre et évocateur]**

---

## Introduction

[5-6 lignes : climat général de la semaine, tendances dominantes, signaux faibles à surveiller]

---

## [SUJET 1/6] – [Titre accrocheur - TENDANCE QUI FAIT PARLER]

### Résumé
[3-4 lignes : faits essentiels, enjeux, pourquoi ça fait parler]

### Synthèse approfondie
[15-25 lignes :
- Contexte : Quel événement a déclenché le buzz ?
- Faits clés : Qui a fait quoi ? Quels chiffres ? Quelles annonces ?
- Impacts : Sur l'industrie, les utilisateurs, les concurrents
- Analyse critique : Pourquoi c'est important, ruptures potentielles]

### Divergences entre sources
[Si pertinent : Points de désaccord entre médias, analyses contradictoires, débats en cours]

### Sources
- [Titre article 1] – [Source] – [URL complète]
- [Titre article 2] – [Source] – [URL complète]
- [...]

---

## [SUJET 2/6] – [Titre – TENDANCE QUI FAIT PARLER]

[Répéter structure ci-dessus]

---

## [SUJET 3/6] – [Titre – TENDANCE QUI FAIT PARLER]

[Répéter structure ci-dessus]

---

## [SUJET 4/6] – [Titre – SUJET TECHNOLOGIQUE]

[Répéter structure ci-dessus - focus technique]

---

## [SUJET 5/6] – [Titre – SUJET TECHNOLOGIQUE]

[Répéter structure ci-dessus - focus technique]

---

## [SUJET 6/6] – [Titre – SUJET TECHNOLOGIQUE]

[Répéter structure ci-dessus - focus technique]

---

## Autres sujets de la semaine

### [Titre court sujet A]
**Résumé** : [2-3 lignes]
**Synthèse** : [5-8 lignes - contexte, faits, enjeux]
**Source** : [Nom média] – [URL complète]

### [Titre court sujet B]
**Résumé** : [2-3 lignes]
**Synthèse** : [5-8 lignes]
**Source** : [Nom média] – [URL complète]

[Continuer pour tous les autres articles]

---

## Synthèse finale

### Points clés de la semaine
1. [Point 1 - tendance majeure]
2. [Point 2 - avancée technique]
3. [Point 3 - signal faible]

### Divergences d'analyse notables
- [Désaccords entre sources sur un sujet]

### Signaux faibles & opportunités
- [Tendances émergentes à surveiller]

### Risques & menaces
- [Points d'attention]

### À surveiller la semaine prochaine
- [Sujets en développement]

---

**Fin de l'édition**
*Veille générée par système 2-agents OpenAI : Recherche factuelle + Synthèse analytique*
```

**CONSIGNES CRITIQUES** :

1. **Sélection des 6 sujets** :
   - Sujets 1-3 : BUZZ, CONTROVERSES, RUPTURES STRATÉGIQUES
   - Sujets 4-6 : AVANCÉES TECHNIQUES, NOUVEAUX MODÈLES, HARDWARE
   - Privilégier la diversité thématique
   - Éviter doublons conceptuels

2. **Synthèse approfondie** (15-25 lignes) :
   - Contexte clair
   - Faits mesurables
   - Analyse critique
   - Impacts concrets

3. **Divergences entre sources** :
   - Montrer les désaccords
   - Présenter plusieurs angles
   - Rester neutre et factuel

4. **Sources** :
   - CITER TOUTES les sources utilisées
   - URLs complètes obligatoires
   - Format : [Titre] – [Média] – [URL]

5. **Autres sujets** :
   - Liste compacte
   - Résumé 2-3 lignes
   - Synthèse 5-8 lignes
   - Une seule source principale

6. **Style** :
   - Sobre, professionnel, élégant
   - Pas d'emoji
   - Reformulation intelligente (jamais de copier-coller)

**ÉQUILIBRE** :
- 6 sujets principaux = 75% du contenu
- Autres sujets = 25% du contenu

Génère le Markdown complet maintenant, sans préambule :"""

    print("🤖 Génération synthèse Markdown avec GPT-4 Turbo...")
    
    try:
        response = client.chat.completions.create(
            model=MODEL_SYNTHESE,
            messages=[
                {
                    "role": "system",
                    "content": "Tu es un analyste expert en IA/LLM. Tu réponds UNIQUEMENT en Markdown, sans préambule, sans balises code."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,  # Créativité modérée pour analyse
            max_tokens=12000  # Augmenté pour 6 synthèses approfondies
        )
        
        markdown_content = response.choices[0].message.content.strip()
        
        print(f"📊 Tokens utilisés : {response.usage.total_tokens}")
        
        cost_input = (response.usage.prompt_tokens / 1000) * 0.01
        cost_output = (response.usage.completion_tokens / 1000) * 0.03
        cost_total = cost_input + cost_output
        print(f"💰 Coût estimé : ${cost_total:.4f}")
        
        print(f"✅ Synthèse générée : {len(markdown_content)} caractères")
        
        return markdown_content
    
    except Exception as e:
        print(f"❌ Erreur GPT-4 Turbo : {e}")
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
        print("🤖 AGENT 3 - SYNTHÈSE IA (GPT-4 Turbo)")
        print("=" * 80)
        print(f"⏰ Exécution : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print()
        
        if not OPENAI_API_KEY:
            print("❌ OPENAI_API_KEY manquante")
            sys.exit(1)
        
        if not GOOGLE_CREDENTIALS:
            print("❌ GOOGLE_DRIVE_CREDENTIALS manquantes")
            sys.exit(1)
        
        print("📂 ÉTAPE 1/3 : Chargement recherche brute IA")
        print("-" * 80)
        data = charger_recherche_brute()
        print()
        
        print("📝 ÉTAPE 2/3 : Sélection 6 sujets + synthèse approfondie")
        print("-" * 80)
        synthese = generer_synthese_markdown(data)
        print()
        
        print("☁️  ÉTAPE 3/3 : Upload Google Drive")
        print("-" * 80)
        uploader_vers_drive(synthese)
        print()
        
        print("=" * 80)
        print("✅ AGENT 3 SYNTHÈSE IA TERMINÉ")
        print("=" * 80)
        print(f"📊 {len(data.get('articles', []))} articles analysés")
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
