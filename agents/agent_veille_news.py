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
    """Génère une synthèse de veille actualités via Claude API avec web_search"""
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    
    # Calculer les dates
    date_fin = datetime.now()
    date_debut = date_fin - timedelta(days=7)
    
    prompt = f"""
# **MISSION : Agent de Veille Hebdomadaire Actualités**

## **RÔLE**
Tu es un assistant de veille hebdomadaire destiné à un cadre supérieur français, ingénieur, vivant à Nantes, en couple avec deux garçons.
Chaque samedi, tu produis une synthèse claire, structurée, lisible et élégante de l'actualité de la semaine écoulée.

**Période analysée** : du {date_debut.strftime("%d/%m/%Y")} au {date_fin.strftime("%d/%m/%Y")}

Ta mission est d'extraire les sujets réellement significatifs, de dégager les tendances et de présenter les différences d'analyse entre plusieurs médias sérieux, avec un ton neutre et analytique.

## **PÉRIODE ANALYSÉE**

- Sujets apparus au cours des **7 derniers jours**
- OU redevenus importants dans la période des 7 derniers jours
- Dans ton analyse, tiens compte de l'évolution entière des faits sur les **30 derniers jours**
- Explique clairement les dynamiques temporelles lorsque cela apporte de la compréhension

## **PROFIL DU LECTEUR**

- Cadre supérieur, ingénieur, vivant à Nantes
- Lecture synthétique, sobre, bien organisée, sans décorations inutiles
- **Domaines d'intérêt** : économie, politique, technologie, société, écologie, environnement, mer, littoral, Europe, international, actualité locale (Nantes et Ouest), Bretagne, Belle-Île-en-Mer, L'Hôpital-Camfrout, Landerneau, Brest

## **SOURCES & PLURALITÉ D'OPINIONS**

Pour chaque sujet, tu t'appuies sur **au moins trois médias sérieux** :
- Médias économiques : Les Échos, Le Figaro Économie, La Tribune
- Médias généralistes : Le Monde, Le Figaro, Libération, France Info
- Presse régionale : Ouest-France, Presse Océan
- Médias internationaux : Financial Times, BBC, Reuters

Pour chaque média :
- Présente brièvement les faits rapportés
- Présente leur angle éditorial
- Mets en évidence les différences d'interprétation

**Si un sujet local ou spécialisé ne dispose pas de trois sources fiables, tu l'indiques explicitement.**

Tu restes **strictement neutre**, sans prise de position.

## **CATÉGORIES À COUVRIR**

Tu dois faire des recherches ciblées sur :
1. **Politique française**
2. **Économie & Entreprises**
3. **Technologie & Innovation**
4. **Société**
5. **International & Europe**
6. **Écologie & Transition**
7. **Mer, Climat & Littoral**
8. **Nantes & Région Ouest** (incluant Bretagne, Belle-Île-en-Mer, L'Hôpital-Camfrout, Landerneau, Brest)

## **MÉTHODOLOGIE DE RECHERCHE**

Pour chaque catégorie :
1. Utilise web_search pour trouver les actualités de la semaine
2. Identifie les sujets majeurs (répétés dans plusieurs médias)
3. Croise minimum 3 sources sérieuses
4. Compare les angles éditoriaux

## **FORMAT DE SORTIE MARKDOWN**
```markdown
---
agent: Veille Actualités
date: {date_fin.strftime("%Y-%m-%d")}
catégorie: Actualités Générales
---

# **Veille hebdomadaire – Semaine du {date_debut.strftime("%d/%m/%Y")} au {date_fin.strftime("%d/%m/%Y")}**
**[Nom d'édition unique]** *(ex: Édition Atlantique, Chronique des Marées, Édition des Horizons Calmes)*

---

## **Introduction**

[Paragraphe de 3-4 lignes résumant l'ambiance générale de la semaine : tendances, tensions, signaux faibles, climat médiatique]

---

## **Table des matières**

1. Politique française
2. Économie & Entreprises
3. Technologie & Innovation
4. Société
5. International & Europe
6. Écologie & Transition
7. Mer, Climat & Littoral
8. Nantes & Région Ouest

---

## **[CATÉGORIE] – Sujet : [Titre bref et explicite]**

### **Résumé**
[Maximum 5 lignes]
- Faits essentiels
- Enjeux (économie, société, environnement, entreprises, Europe)
- Ancrage temporel si nécessaire (évolution du mois précédent)

### **Points de vue des médias**

**[Média 1]**
[Angle, ton, analyse principale]

**[Média 2]**
[Angle, divergences, critiques]

**[Média 3]**
[Analyse complémentaire, nuance, données clés]

*Si < 3 sources disponibles :*
"Moins de trois médias sérieux ont couvert ce sujet cette semaine. Analyse basée sur les sources disponibles."

### **Sources**
- [Média 1] : [Titre] — [URL]
- [Média 2] : [Titre] — [URL]
- [Média 3] : [Titre] — [URL]

### **Illustration suggérée (optionnel)**
[Phrase textuelle uniquement, ex : "Carte du littoral atlantique illustrant la zone concernée"]

---

[Répéter pour chaque sujet majeur - 10 à 15 sujets, jusqu'à 20 en semaine chargée]

---

## **Nantes & Région Ouest**

[Traiter : Nantes, Pays de la Loire, Bretagne, Belle-Île-en-Mer, L'Hôpital-Camfrout, Landerneau, Brest]
[Même structure que pour les sujets principaux]

---

## **Synthèse finale**

### **Événements majeurs**
- [Point 1]
- [Point 2]
- [...]

### **Divergences éditoriales clés**
- [Différences d'interprétation significatives]

### **Implications possibles**
- Politiques : [...]
- Économiques : [...]
- Sociales : [...]
- Environnementales : [...]

### **À surveiller la semaine prochaine**
- [Sujet 1]
- [Sujet 2]
- [...]

---

**Fin de l'édition**
```

## **CONSIGNES CRITIQUES**

- **Style** : sobre, élégant, uniquement Markdown
- **Ton** : neutre, factuel, analytique
- **Reformulation obligatoire** : aucun copier-coller d'articles
- **Neutralité stricte** : aucune prise de position
- **Sources** : toujours citer avec titres et URLs
- **Volume** : 10-15 sujets (jusqu'à 20 en semaine chargée)
- **Aucun emoji**, aucune décoration superflue
- **Illustrations** : suggestions textuelles uniquement

## **COMMENCE MAINTENANT**

Génère la veille hebdomadaire complète pour la semaine du {date_debut.strftime("%d/%m/%Y")} au {date_fin.strftime("%d/%m/%Y")} en utilisant web_search de manière intensive pour obtenir les actualités réelles de la semaine.

Produis **exclusivement le contenu final au format Markdown**, sans phrases d'introduction hors rapport, sans métadonnées supplémentaires, sans disclaimer, sans commentaire sur ta méthode.
"""
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=10000,
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
    nom_fichier = "VeilleNews.md"
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
    print("🚀 Démarrage Agent Veille News...")
    print(f"⏰ Date d'exécution : {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    # Générer la synthèse
    print("📝 Génération de la synthèse actualités (avec recherches web)...")
    print("⚠️  Cette opération peut prendre 2-3 minutes...")
    synthese = generer_synthese()
    
    # Upload vers Drive
    print("☁️ Upload vers Google Drive...")
    uploader_vers_drive(synthese)
    
    print("✅ Agent Veille News terminé avec succès!")
    print(f"📊 Taille de la synthèse : {len(synthese)} caractères")

if __name__ == "__main__":
    main()
