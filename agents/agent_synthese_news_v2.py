"""
Agent 4 - Synthèse News
Modèle : GPT-4 Turbo (ChatGPT)
Rôle : Analyser recherche brute → Sélectionner 6 sujets (2 int + 2 nat + 2 local) → Synthétiser avec divergences

Sélection 6 sujets obligatoire :
- 2 sujets internationaux
- 2 sujets nationaux (France)
- 2 sujets locaux (Bretagne/Pays de Loire/Mer)

Structure par sujet : Résumé court, synthèse approfondie, divergences entre sources, toutes sources citées
Autres sujets : Liste compacte avec titre, résumé court, synthèse, source unique
"""

import os
import json
import sys
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

# Modèle ChatGPT-4 Turbo pour synthèse analytique
MODEL_SYNTHESE = "gpt-4-turbo-preview"

# Fichiers
INPUT_JSON = "recherche_news_brute.json"
OUTPUT_MARKDOWN = "VeilleNews.md"


# ================================================================================
# CHARGEMENT DONNÉES RECHERCHE
# ================================================================================

def charger_recherche_brute() -> Dict[str, Any]:
    """Charge le JSON produit par Agent 2 (Recherche News)"""
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
    1. Sélectionner 6 sujets : 2 internationaux + 2 nationaux + 2 locaux
    2. Synthétiser en profondeur avec divergences sources
    3. Lister les autres sujets en mode compact
    """
    
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    articles = data.get('articles', [])
    
    if len(articles) == 0:
        print("⚠️  Aucun article à synthétiser")
        return "# Veille News\n\nAucune actualité collectée cette semaine.\n"
    
    # Préparer texte articles bruts
    articles_text = ""
    for i, art in enumerate(articles, 1):
        articles_text += f"\n**[{i}] {art.get('titre', 'Sans titre')}**\n"
        articles_text += f"Catégorie: {art.get('categorie', 'Non classé')} | Zone: {art.get('zone_geo', 'Non spécifiée')}\n"
        articles_text += f"Source: {art.get('source', 'Inconnue')} | URL: {art.get('url', '#')}\n"
        articles_text += f"Résumé court: {art.get('resume_court', '')}\n"
        articles_text += f"Synthèse complète:\n{art.get('synthese_complete', '')}\n\n"
    
    date_debut = data.get('periode', {}).get('debut', datetime.now().strftime('%Y-%m-%d'))
    date_fin = data.get('periode', {}).get('fin', datetime.now().strftime('%Y-%m-%d'))
    
    prompt = f"""Tu es un journaliste expert en actualités internationales, nationales et locales qui produit une veille hebdomadaire pour un cadre supérieur français, ingénieur, vivant à Nantes.

**PÉRIODE** : du {date_debut} au {date_fin}

**ARTICLES COLLECTÉS (recherche brute factuelle)** :
{articles_text}

**TA MISSION - SÉLECTION ET SYNTHÈSE** :

1. **Sélectionner EXACTEMENT 6 sujets principaux** selon cette répartition OBLIGATOIRE :
   - **2 sujets INTERNATIONAUX** (géopolitique, économie mondiale, crises)
   - **2 sujets NATIONAUX** (France : politique, économie, société)
   - **2 sujets LOCAUX** (Bretagne/Pays de Loire/Nantes : politique locale, économie régionale, sports maritimes, mer)

2. **Pour chaque sujet des 6** :
   - **Résumé court** (3-4 lignes max) : L'essentiel à retenir
   - **Synthèse approfondie** (15-25 lignes) : 
     * Contexte et enjeux
     * Faits clés et chiffres
     * Impacts politiques/économiques/sociaux
     * Analyse critique
   - **Divergences entre sources** : Points de désaccord, angles différents, positions politiques
   - **Sources citées** : TOUTES les sources utilisées avec URLs complètes

3. **Pour les autres sujets** (en liste compacte) :
   - Titre court
   - Résumé court (2-3 lignes max)
   - Synthèse (5-8 lignes)
   - Source avec URL (une seule source principale)

**STRUCTURE MARKDOWN OBLIGATOIRE** :

```markdown
---
agent: Synthèse News (2-agents OpenAI pipeline)
date: {date_fin}
catégorie: Actualités
modèles: GPT-4 Turbo (recherche + synthèse)
---

# Veille Actualités – Semaine du {date_debut} au {date_fin}

**Édition [Nom sobre et évocateur]**

---

## Introduction

[5-6 lignes : climat général de la semaine, tendances dominantes internationales/nationales/locales, signaux faibles]

---

## [SUJET 1/6] – [Titre accrocheur - INTERNATIONAL]

### Résumé
[3-4 lignes : faits essentiels, enjeux, impacts]

### Synthèse approfondie
[15-25 lignes :
- Contexte : Quels événements ont conduit à cette situation ?
- Faits clés : Qui a fait quoi ? Quels développements ? Quels chiffres ?
- Impacts : Sur la géopolitique, l'économie mondiale, les populations
- Analyse critique : Pourquoi c'est important, conséquences potentielles]

### Divergences entre sources
[Si pertinent : Points de désaccord entre médias, analyses contradictoires, positions politiques différentes]

### Sources
- [Titre article 1] – [Source] – [URL complète]
- [Titre article 2] – [Source] – [URL complète]
- [...]

---

## [SUJET 2/6] – [Titre – INTERNATIONAL]

[Répéter structure ci-dessus]

---

## [SUJET 3/6] – [Titre – NATIONAL FRANCE]

[Répéter structure ci-dessus]

---

## [SUJET 4/6] – [Titre – NATIONAL FRANCE]

[Répéter structure ci-dessus]

---

## [SUJET 5/6] – [Titre – LOCAL BRETAGNE/PAYS DE LOIRE]

[Répéter structure ci-dessus - focus local]

---

## [SUJET 6/6] – [Titre – LOCAL BRETAGNE/PAYS DE LOIRE]

[Répéter structure ci-dessus - focus local]

---

## Autres sujets de la semaine

### [Titre court sujet A]
**Catégorie** : [International/National/Local]
**Résumé** : [2-3 lignes]
**Synthèse** : [5-8 lignes - contexte, faits, enjeux]
**Source** : [Nom média] – [URL complète]

### [Titre court sujet B]
**Catégorie** : [International/National/Local]
**Résumé** : [2-3 lignes]
**Synthèse** : [5-8 lignes]
**Source** : [Nom média] – [URL complète]

[Continuer pour tous les autres articles]

---

## Synthèse finale

### Points clés de la semaine
1. [Point 1 - international]
2. [Point 2 - national]
3. [Point 3 - local]

### Divergences d'analyse notables
- [Désaccords entre sources sur un sujet]

### Signaux faibles & tendances
- [Tendances émergentes à surveiller]

### Impacts locaux (Bretagne/Pays de Loire)
- [Conséquences des actualités internationales/nationales sur la région]

### À surveiller la semaine prochaine
- [Sujets en développement]

---

**Fin de l'édition**
*Veille générée par système 2-agents OpenAI : Recherche factuelle + Synthèse analytique*
```

**CONSIGNES CRITIQUES** :

1. **Sélection des 6 sujets** :
   - RÉPARTITION OBLIGATOIRE : 2 int + 2 nat + 2 local
   - Privilégier les sujets les plus importants/impactants
   - Diversité thématique
   - Pour le local : focus Nantes, Brest, Belle-Île-en-Mer, sports maritimes

2. **Synthèse approfondie** (15-25 lignes) :
   - Contexte clair
   - Faits mesurables
   - Analyse critique
   - Impacts concrets

3. **Divergences entre sources** :
   - Montrer les désaccords politiques/éditoriaux
   - Présenter plusieurs angles
   - Rester neutre et factuel

4. **Sources** :
   - CITER TOUTES les sources utilisées
   - URLs complètes obligatoires
   - Format : [Titre] – [Média] – [URL]

5. **Autres sujets** :
   - Liste compacte
   - Préciser catégorie (International/National/Local)
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
                    "content": "Tu es un journaliste expert en actualités. Tu réponds UNIQUEMENT en Markdown, sans préambule, sans balises code."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,  # Créativité modérée pour analyse
            max_tokens=12000  # 6 synthèses approfondies
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
        print("🤖 AGENT 4 - SYNTHÈSE NEWS (GPT-4 Turbo)")
        print("=" * 80)
        print(f"⏰ Exécution : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print()
        
        if not OPENAI_API_KEY:
            print("❌ OPENAI_API_KEY manquante")
            sys.exit(1)
        
        if not GOOGLE_CREDENTIALS:
            print("❌ GOOGLE_DRIVE_CREDENTIALS manquantes")
            sys.exit(1)
        
        print("📂 ÉTAPE 1/3 : Chargement recherche brute News")
        print("-" * 80)
        data = charger_recherche_brute()
        print()
        
        print("📝 ÉTAPE 2/3 : Sélection 6 sujets (2 int + 2 nat + 2 local) + synthèse")
        print("-" * 80)
        synthese = generer_synthese_markdown(data)
        print()
        
        print("☁️  ÉTAPE 3/3 : Upload Google Drive")
        print("-" * 80)
        uploader_vers_drive(synthese)
        print()
        
        print("=" * 80)
        print("✅ AGENT 4 SYNTHÈSE NEWS TERMINÉ")
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
