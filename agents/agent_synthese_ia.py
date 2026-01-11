"""
Agent 2 - Synthétiseur IA
Modèle : GPT-4o (qualité maximale)
Rôle : Lire JSON filtré → Générer synthèse Markdown → Upload Google Drive
"""

import os
import json
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

# Modèle premium pour synthèse qualitative
MODEL_SYNTHESE = "gpt-4o-2024-11-20"

# Fichiers d'entrée/sortie - utiliser répertoire courant
INPUT_JSON = "articles_filtres_ia.json"
OUTPUT_MARKDOWN = "VeilleIA.md"


# ================================================================================
# CHARGEMENT DONNÉES FILTRÉES
# ================================================================================

def charger_articles_filtres() -> Dict[str, Any]:
    """
    Charge le JSON produit par Agent 1
    
    Returns:
        Dictionnaire avec articles filtrés et métadonnées
    """
    if not os.path.exists(INPUT_JSON):
        raise FileNotFoundError(f"❌ Fichier {INPUT_JSON} introuvable. Agent 1 doit s'exécuter avant Agent 2.")
    
    with open(INPUT_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"✅ JSON chargé : {len(data['articles'])} articles")
    print(f"📊 Thèmes : {', '.join(data.get('themes', {}).keys())}")
    
    return data


# ================================================================================
# GÉNÉRATION SYNTHÈSE MARKDOWN GPT-4o
# ================================================================================

def generer_synthese_markdown(data: Dict[str, Any]) -> str:
    """
    Utilise GPT-4o pour générer une synthèse Markdown élégante
    
    Args:
        data: Données JSON de l'Agent 1
        
    Returns:
        Contenu Markdown complet de la veille
    """
    
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    # Préparer les données pour le prompt
    articles_par_theme = {}
    for article in data['articles']:
        theme = article['theme']
        if theme not in articles_par_theme:
            articles_par_theme[theme] = []
        articles_par_theme[theme].append(article)
    
    # Créer un texte structuré des articles
    articles_text = ""
    for theme, articles in articles_par_theme.items():
        articles_text += f"\n## {theme}\n\n"
        for art in articles:
            articles_text += f"**{art['titre']}**\n"
            articles_text += f"Source: {art['source']} | URL: {art['url']}\n"
            articles_text += f"Snippet: {art['snippet']}\n"
            articles_text += f"Pertinence: {art['pertinence']}/10 | Tags: {', '.join(art['tags'])}\n\n"
    
    # Récupérer les dates
    date_debut = datetime.strptime(data['periode']['debut'], '%Y-%m-%d')
    date_fin = datetime.strptime(data['periode']['fin'], '%Y-%m-%d')
    
    prompt = f"""Tu es un journaliste expert en IA/LLM qui produit une veille hebdomadaire de très haute qualité pour un cadre supérieur français, ingénieur, vivant à Nantes.

**PÉRIODE ANALYSÉE** : du {date_debut.strftime('%d/%m/%Y')} au {date_fin.strftime('%d/%m/%Y')}

**ARTICLES PRÉ-FILTRÉS À SYNTHÉTISER** :
{articles_text}

**STATISTIQUES** :
- {data['statistiques']['articles_bruts']} articles initiaux collectés
- {data['statistiques']['articles_finaux']} articles pertinents sélectionnés
- {len(articles_par_theme)} thèmes couverts

**TA MISSION** :
Produire une synthèse Markdown professionnelle, sobre et élégante selon le format ci-dessous.

**PROFIL DU LECTEUR** :
- Cadre supérieur, ingénieur, basé à Nantes
- Centres d'intérêt : LLM, IA générative, open source, cloud/hardware, économie du secteur, recherche scientifique, régulation européenne, cybersécurité, applications entreprises, risques environnementaux et sociétaux

**FORMAT DE SORTIE MARKDOWN** :
```markdown
---
agent: Veille IA (2 agents OpenAI)
date: {date_fin.strftime('%Y-%m-%d')}
catégorie: Intelligence Artificielle
modèles: GPT-4o-mini (collecte) + GPT-4o (synthèse)
---

# **Veille IA & LLM – Semaine du {date_debut.strftime('%d/%m/%Y')} au {date_fin.strftime('%d/%m/%Y')}**
**Édition [Nom créatif sobre]** *(ex: Édition Tensor, Édition Gradient, Chronique des Modèles)*

---

## **Introduction**

[Paragraphe de 4-5 lignes résumant :
- Le climat global de la semaine IA/LLM
- Les tendances clés observées
- Les signaux faibles émergents
- Le ton général (innovation, régulation, consolidation, etc.)]

---

## **Table des matières**

1. [Thème 1]
2. [Thème 2]
3. [...]
10. Synthèse finale

---

## **[THÈME] – [Titre du sujet principal]**

### **Résumé**
[5 lignes maximum : faits essentiels, enjeux, impacts potentiels]

### **Points de vue croisés**

**Source 1 – [Nom du média]**
[Angle éditorial, analyse principale, 3-4 lignes]

**Source 2 – [Nom du média]**
[Divergences, critiques, nuances, 3-4 lignes]

**Source 3 – [Nom du média]** (si disponible)
[Apport complémentaire ou technique, 3-4 lignes]

### **Analyse & implications**
- Impacts sectoriels : [...]
- Opportunités : [...]
- Risques potentiels : [...]

### **Fiabilité & signaux faibles**
- [Points incertains ou non confirmés]
- [Rumeurs à surveiller]
- [Indicateurs d'évolution]

### **Sources**
- [Titre source 1] – [URL complète]
- [Titre source 2] – [URL complète]
- [Titre source 3] – [URL complète]

---

[Répéter pour chaque thème majeur - couvrir TOUS les articles fournis]

---

## **Synthèse finale**

### **Points clés de la semaine**
1. [Événement majeur 1]
2. [Événement majeur 2]
3. [Événement majeur 3]
4. [...]

### **Divergences d'analyse notables**
- [Point de désaccord entre sources ou visions contradictoires]

### **Signaux faibles & opportunités**
- [Tendances émergentes détectées]
- [Technologies ou approches prometteuses]

### **Risques & menaces**
- [Points d'attention cybersécurité, éthique, régulation]
- [Menaces concurrentielles ou technologiques]

### **À surveiller la semaine prochaine**
- [Sujets en développement]
- [Événements annoncés]

---

**Fin de l'édition**
*Veille générée automatiquement par système 2-agents OpenAI*
*Agent 1 (GPT-4o-mini) : Collecte et filtrage | Agent 2 (GPT-4o) : Synthèse*
```

**CONSIGNES CRITIQUES** :

1. **Style** : sobre, professionnel, élégant, aucun emoji
2. **Ton** : précis, concis, factuel, analytique
3. **Sources** : toujours citer avec titres et URLs complètes
4. **Reformulation** : jamais de copier-coller des snippets, toujours reformuler
5. **Fiabilité** : signaler clairement les incertitudes et points non confirmés
6. **Exhaustivité** : traiter TOUS les articles fournis (pas de sélection supplémentaire)
7. **Équilibre** : donner à chaque thème un poids proportionnel à son importance
8. **Volume** : viser une lecture de 12-15 minutes
9. **Nantes** : si des articles concernent Nantes/région Ouest, créer une section dédiée
10. **Neutralité** : présenter les faits et analyses sans jugement de valeur

**IMPORTANT** : 
- Utilise les scores de pertinence pour hiérarchiser l'importance des sujets
- Les articles à pertinence 8-10 méritent un traitement approfondi
- Les articles à pertinence 5-7 peuvent être regroupés ou traités plus brièvement
- Maintiens une cohérence narrative entre les sections

**COMMENCE MAINTENANT**

Génère la veille IA complète en Markdown, sans préambule, sans commentaire méta, directement le contenu final."""

    print("🤖 Génération de la synthèse Markdown avec GPT-4o...")
    
    try:
        response = client.chat.completions.create(
            model=MODEL_SYNTHESE,
            messages=[
                {
                    "role": "system",
                    "content": "Tu es un journaliste expert en IA/LLM qui produit des veilles hebdomadaires de très haute qualité. Tu réponds UNIQUEMENT en Markdown, sans préambule, sans métadonnées supplémentaires."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,  # Équilibre créativité/précision
            max_tokens=8000   # Synthèse détaillée
        )
        
        # Extraire le Markdown
        markdown_content = response.choices[0].message.content.strip()
        
        # Statistiques
        tokens_used = response.usage.total_tokens
        print(f"📊 Tokens utilisés : {tokens_used} (prompt: {response.usage.prompt_tokens}, completion: {response.usage.completion_tokens})")
        
        # Estimation du coût (GPT-4o : ~$0.03/1K input, ~$0.06/1K output)
        cost_input = (response.usage.prompt_tokens / 1000) * 0.03
        cost_output = (response.usage.completion_tokens / 1000) * 0.06
        cost_total = cost_input + cost_output
        print(f"💰 Coût estimé : ${cost_total:.4f}")
        
        print(f"✅ Synthèse générée : {len(markdown_content)} caractères")
        
        return markdown_content
    
    except Exception as e:
        print(f"❌ Erreur GPT-4o : {e}")
        raise


# ================================================================================
# UPLOAD GOOGLE DRIVE
# ================================================================================

def uploader_vers_drive(contenu_markdown: str) -> None:
    """
    Upload le fichier Markdown vers Google Drive
    
    Args:
        contenu_markdown: Contenu Markdown à uploader
    """
    
    print("☁️  Upload vers Google Drive...")
    
    # Authentification
    credentials = service_account.Credentials.from_service_account_info(
        GOOGLE_CREDENTIALS,
        scopes=['https://www.googleapis.com/auth/drive']
    )
    
    service = build('drive', 'v3', credentials=credentials)
    
    # Vérifier si le fichier existe déjà
    query = f"name='{OUTPUT_MARKDOWN}' and '{FOLDER_ID}' in parents"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])
    
    # Créer le média en mémoire
    file_metadata = {'name': OUTPUT_MARKDOWN}
    media = MediaIoBaseUpload(
        io.BytesIO(contenu_markdown.encode('utf-8')),
        mimetype='text/markdown',
        resumable=True
    )
    
    if files:
        # Mettre à jour le fichier existant
        file_id = files[0]['id']
        service.files().update(
            fileId=file_id,
            media_body=media
        ).execute()
        print(f"✅ Fichier {OUTPUT_MARKDOWN} mis à jour sur Google Drive")
    else:
        # Créer un nouveau fichier
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
    """Point d'entrée principal de l'agent synthétiseur"""
    
    print("=" * 80)
    print("🤖 AGENT 2 - SYNTHÉTISEUR IA (GPT-4o)")
    print("=" * 80)
    print(f"⏰ Exécution : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()
    
    # Vérifier les clés API
    if not OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY manquante")
        return
    
    if not GOOGLE_CREDENTIALS:
        print("❌ GOOGLE_DRIVE_CREDENTIALS manquantes")
        return
    
    # Étape 1 : Charger les données filtrées
    print("📂 ÉTAPE 1/3 : Chargement du JSON filtré (Agent 1)")
    print("-" * 80)
    data = charger_articles_filtres()
    print()
    
    # Étape 2 : Générer la synthèse Markdown
    print("📝 ÉTAPE 2/3 : Génération synthèse Markdown (GPT-4o)")
    print("-" * 80)
    synthese = generer_synthese_markdown(data)
    print()
    
    # Étape 3 : Upload vers Google Drive
    print("☁️  ÉTAPE 3/3 : Upload vers Google Drive")
    print("-" * 80)
    uploader_vers_drive(synthese)
    print()
    
    # Résumé final
    print("=" * 80)
    print("✅ AGENT 2 TERMINÉ AVEC SUCCÈS")
    print("=" * 80)
    print(f"📊 Statistiques finales :")
    print(f"   - Articles synthétisés : {len(data['articles'])}")
    print(f"   - Thèmes couverts : {len(data.get('themes', {}))}")
    print(f"   - Taille synthèse : {len(synthese)} caractères")
    print()
    print(f"☁️  Fichier sur Google Drive : {OUTPUT_MARKDOWN}")
    print()


if __name__ == "__main__":
    main()
