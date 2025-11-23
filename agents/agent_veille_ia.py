import anthropic
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import json
from datetime import datetime, timedelta
import io

# Configuration
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')
GOOGLE_CREDENTIALS = json.loads(os.environ.get('GOOGLE_DRIVE_CREDENTIALS'))
FOLDER_ID = os.environ.get('GOOGLE_DRIVE_FOLDER_ID')

def generer_synthese():
    """Génère une synthèse de veille IA via Claude API avec web_search"""
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    
    # Calculer les dates
    date_fin = datetime.now()
    date_debut = date_fin - timedelta(days=7)
    
    prompt = f"""
# **MISSION : Agent de Veille Hebdomadaire IA**

## **CONTEXTE**
Tu es un assistant de **veille IA hebdomadaire** destiné à un cadre supérieur français, ingénieur, vivant à Nantes.

**Période analysée** : du {date_debut.strftime("%d/%m/%Y")} au {date_fin.strftime("%d/%m/%Y")}

**Profil du lecteur** :
- Cadre supérieur, ingénieur, basé à Nantes
- Centres d'intérêt : LLM, IA générative, open source, cloud/hardware, économie du secteur, recherche scientifique, régulation européenne, cybersécurité, applications entreprises, risques environnementaux et sociétaux

## **TA MISSION**

1. **Rechercher les actualités IA/LLM** de la semaine écoulée en utilisant l'outil web_search
2. **Identifier 10-15 sujets majeurs** réellement significatifs
3. **Croiser minimum 3 sources** par sujet
4. **Mettre en avant les différences d'analyse** entre les sources
5. **Avertir sur les points non vérifiés** ou incertains
6. **Produire une synthèse structurée en Markdown** selon le format ci-dessous

## **CATÉGORIES À COUVRIR**

Tu dois faire des recherches ciblées sur :
1. Nouveaux modèles LLM et technologies
2. Open source & écosystèmes
3. Recherche scientifique & papers
4. Régulation & gouvernance (UE/US/monde)
5. Industrie, investissements & mouvements de marché
6. Cybersécurité, risques & incidents
7. Applications & usages entreprises
8. Hardware, compute & optimisation
9. **Nantes & Région Ouest** (obligatoire - précise si rien trouvé)

## **MÉTHODOLOGIE DE RECHERCHE**

Pour chaque catégorie importante :
1. Utilise web_search pour trouver les actualités de la semaine
2. Identifie les sujets majeurs (répétés dans plusieurs médias ou ayant généré un bruit notable)
3. Croise minimum 3 sources sérieuses
4. Compare les angles éditoriaux et divergences

## **FORMAT DE SORTIE MARKDOWN**
```markdown
---
agent: Veille IA
date: {date_fin.strftime("%Y-%m-%d")}
catégorie: Intelligence Artificielle
---

# **Veille IA & LLM – Semaine du {date_debut.strftime("%d/%m/%Y")} au {date_fin.strftime("%d/%m/%Y")}**
**Édition [Nom créatif sobre]** *(ex: Édition Tensor, Édition Gradient, Chronique des Modèles)*

---

## **Introduction**

[Paragraphe de 3-4 lignes résumant le climat global, les tendances clés, les signaux faibles]

---

## **Table des matières**

1. Nouveautés technologiques & nouvelles approches
2. Modèles & Publications LLM
3. Open Source & Écosystèmes
4. Recherche scientifique & papers
5. Régulation & Gouvernance
6. Industrie, investissements & marché
7. Cybersécurité, risques & incidents
8. Applications & usages
9. Hardware, compute & optimisation
10. Europe & France
11. Nantes & Région Ouest

---

## **[CATÉGORIE] – [Titre du sujet]**

### **Résumé**
[5 lignes max : faits essentiels, enjeux, impacts potentiels]

### **Points de vue croisés**

**Source 1 – [Nom du média/site]**
[Angle éditorial, analyse principale]

**Source 2 – [Nom du média/site]**
[Divergences, critiques, nuances]

**Source 3 – [Nom du média/site]**
[Apport complémentaire ou technique]

### **Fiabilité & signaux faibles**
- [Points incertains ou non confirmés]
- [Rumeurs à surveiller]
- [Indicateurs d'évolution ou risques]

### **Sources**
- [Titre source 1] – [URL]
- [Titre source 2] – [URL]
- [Titre source 3] – [URL]

### **Illustration suggérée (optionnel)**
[Si pertinent : description sobre d'une image conceptuelle, schéma, architecture]

---

[Répéter pour chaque sujet majeur - 10 à 15 sujets]

---

## **Nantes & Région Ouest**

[Recherche obligatoire sur actualités IA/tech dans la région. Si rien trouvé, indiquer : "Aucune actualité IA/LLM significative identifiée cette semaine dans la région Nantes/Ouest."]

---

## **Synthèse finale**

### **Points clés de la semaine**
1. [Événement majeur 1]
2. [Événement majeur 2]
3. [...]

### **Divergences d'analyse notables**
- [Point de désaccord entre sources]

### **Signaux faibles & opportunités**
- [Tendances émergentes]

### **Risques & menaces**
- [Points d'attention]

### **À surveiller la semaine prochaine**
- [Sujets en développement]

---

**Fin de l'édition**
```

## **CONSIGNES CRITIQUES**

- **Style** : sobre, professionnel, élégant, aucun emoji
- **Ton** : précis, concis, factuel
- **Sources** : toujours citer avec titres et URLs
- **Réécris toujours** : jamais de copier-coller
- **Fiabilité** : signaler clairement les incertitudes
- **Priorité** : sujets répétés dans plusieurs médias OU ayant généré un bruit notable
- **Volume** : lecture 10-15 minutes
- **Recherche Nantes** : OBLIGATOIRE même si rien trouvé (le préciser)

## **COMMENCE MAINTENANT**

Génère la veille IA complète pour la semaine du {date_debut.strftime("%d/%m/%Y")} au {date_fin.strftime("%d/%m/%Y")} en utilisant web_search de manière intensive pour obtenir les actualités réelles de la semaine.
"""
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8000,
        tools=[{
            "type": "web_search_20250305",
            "name": "web_search"
        }],
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )
    
    # Extraire le texte de la réponse (peut contenir plusieurs blocs)
    contenu = ""
    for block in message.content:
        if block.type == "text":
            contenu += block.text
    
    return contenu

def uploader_vers_drive(contenu_markdown):
    """Upload le fichier markdown vers Google Drive"""
    # Authentification
    credentials = service_account.Credentials.from_service_account_info(
        GOOGLE_CREDENTIALS,
        scopes=['https://www.googleapis.com/auth/drive']
    )
    
    service = build('drive', 'v3', credentials=credentials)
    
    # Vérifier si le fichier existe déjà
    nom_fichier = "VeilleIA.md"
    query = f"name='{nom_fichier}' and '{FOLDER_ID}' in parents"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])
    
    # Créer le média en mémoire
    file_metadata = {'name': nom_fichier}
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
        print(f"✅ Fichier {nom_fichier} mis à jour")
    else:
        # Créer un nouveau fichier
        file_metadata['parents'] = [FOLDER_ID]
        service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        print(f"✅ Fichier {nom_fichier} créé")

def main():
    print("🚀 Démarrage Agent Veille IA...")
    print(f"⏰ Date d'exécution : {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    # Générer la synthèse
    print("📝 Génération de la synthèse IA (avec recherches web)...")
    print("⚠️  Cette opération peut prendre 2-3 minutes...")
    synthese = generer_synthese()
    
    # Upload vers Drive
    print("☁️ Upload vers Google Drive...")
    uploader_vers_drive(synthese)
    
    print("✅ Agent Veille IA terminé avec succès!")
    print(f"📊 Taille de la synthèse : {len(synthese)} caractères")

if __name__ == "__main__":
    main()
