"""
Agent Validateur Markdown
Rôle : Vérifier et reformater les fichiers Markdown pour garantir 6 sujets principaux
Déclenché : Après génération par agents synthèse IA/News
"""

import os
import json
import sys
import re
from datetime import datetime
from typing import Dict, List, Tuple
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload
import io


# ================================================================================
# CONFIGURATION
# ================================================================================

GOOGLE_CREDENTIALS = json.loads(os.environ.get('GOOGLE_DRIVE_CREDENTIALS'))
FOLDER_ID = os.environ.get('GOOGLE_DRIVE_FOLDER_ID')

FICHIERS = ['VeilleIA.md', 'VeilleNews.md']


# ================================================================================
# CONNEXION GOOGLE DRIVE
# ================================================================================

def get_drive_service():
    """Initialise service Google Drive"""
    credentials = service_account.Credentials.from_service_account_info(
        GOOGLE_CREDENTIALS,
        scopes=['https://www.googleapis.com/auth/drive']
    )
    return build('drive', 'v3', credentials=credentials)


def telecharger_fichier(service, nom_fichier: str) -> str:
    """Télécharge un fichier depuis Google Drive"""
    query = f"name='{nom_fichier}' and '{FOLDER_ID}' in parents"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])
    
    if not files:
        raise FileNotFoundError(f"❌ {nom_fichier} introuvable sur Google Drive")
    
    file_id = files[0]['id']
    request = service.files().get_media(fileId=file_id)
    
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    
    done = False
    while not done:
        _, done = downloader.next_chunk()
    
    fh.seek(0)
    contenu = fh.read().decode('utf-8')
    
    print(f"✅ {nom_fichier} téléchargé : {len(contenu)} caractères")
    return contenu


def uploader_fichier(service, nom_fichier: str, contenu: str) -> None:
    """Upload un fichier vers Google Drive"""
    query = f"name='{nom_fichier}' and '{FOLDER_ID}' in parents"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])
    
    file_metadata = {'name': nom_fichier}
    media = MediaIoBaseUpload(
        io.BytesIO(contenu.encode('utf-8')),
        mimetype='text/markdown',
        resumable=True
    )
    
    if files:
        file_id = files[0]['id']
        service.files().update(fileId=file_id, media_body=media).execute()
        print(f"✅ {nom_fichier} mis à jour sur Google Drive")
    else:
        file_metadata['parents'] = [FOLDER_ID]
        service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f"✅ {nom_fichier} créé sur Google Drive")


# ================================================================================
# VALIDATION STRUCTURE
# ================================================================================

def parser_markdown(contenu: str) -> Dict:
    """Parse le Markdown et extrait les sections"""
    
    data = {
        'metadata': {},
        'titre': '',
        'edition': '',
        'introduction': '',
        'articles_principaux': [],
        'autres_sujets': []
    }
    
    lignes = contenu.split('\n')
    section_actuelle = None
    article_actuel = None
    
    for ligne in lignes:
        ligne = ligne.strip()
        
        # Metadata YAML
        if ligne.startswith('agent:'): data['metadata']['agent'] = ligne.replace('agent:', '').strip()
        if ligne.startswith('date:'): data['metadata']['date'] = ligne.replace('date:', '').strip()
        if ligne.startswith('catégorie:'): data['metadata']['categorie'] = ligne.replace('catégorie:', '').strip()
        
        # Titre principal
        if ligne.startswith('# ') and not data['titre']:
            data['titre'] = ligne.replace('# ', '').strip()
        
        # Édition
        if ligne.startswith('**Édition') or ligne.startswith('**Edition'):
            data['edition'] = ligne.replace('**', '').strip()
        
        # Introduction
        if ligne.startswith('## Introduction'):
            section_actuelle = 'introduction'
            continue
        
        if section_actuelle == 'introduction' and ligne and not ligne.startswith('##'):
            data['introduction'] += ligne + ' '
        
        # Articles principaux (détection : ## [THEME] – Titre)
        match = re.match(r'^##\s+\[?([^\]–-]+)\]?\s*[–-]\s*(.+)', ligne)
        if match and '## Autres sujets' not in ligne and '## Introduction' not in ligne:
            if article_actuel:
                data['articles_principaux'].append(article_actuel)
            
            article_actuel = {
                'theme': match.group(1).strip(),
                'titre': match.group(2).strip(),
                'contenu_brut': []
            }
            section_actuelle = 'article_principal'
            continue
        
        # Section "Autres sujets"
        if '## Autres sujets' in ligne:
            if article_actuel:
                data['articles_principaux'].append(article_actuel)
                article_actuel = None
            section_actuelle = 'autres_sujets'
            continue
        
        # Contenu article principal
        if section_actuelle == 'article_principal' and article_actuel and ligne:
            article_actuel['contenu_brut'].append(ligne)
        
        # Autres sujets (format: ### Titre)
        if section_actuelle == 'autres_sujets' and ligne.startswith('### '):
            titre_autre = ligne.replace('### ', '').strip()
            data['autres_sujets'].append({
                'titre': titre_autre,
                'contenu': []
            })
        elif section_actuelle == 'autres_sujets' and data['autres_sujets'] and ligne:
            data['autres_sujets'][-1]['contenu'].append(ligne)
    
    # Ajouter dernier article
    if article_actuel:
        data['articles_principaux'].append(article_actuel)
    
    data['introduction'] = data['introduction'].strip()
    
    return data


def valider_structure(data: Dict) -> Tuple[bool, List[str]]:
    """Valide la structure : doit contenir 6 articles principaux"""
    
    erreurs = []
    
    if not data['metadata']:
        erreurs.append("❌ Metadata YAML manquante")
    
    if not data['titre']:
        erreurs.append("❌ Titre principal manquant")
    
    if not data['introduction']:
        erreurs.append("⚠️  Introduction manquante")
    
    nb_articles = len(data['articles_principaux'])
    if nb_articles < 6:
        erreurs.append(f"❌ Seulement {nb_articles} articles principaux (minimum : 6)")
    
    for i, art in enumerate(data['articles_principaux'], 1):
        if not art['theme']:
            erreurs.append(f"❌ Article {i} : thème manquant")
        if not art['titre']:
            erreurs.append(f"❌ Article {i} : titre manquant")
        if len(art['contenu_brut']) < 5:
            erreurs.append(f"⚠️  Article {i} : contenu trop court")
    
    valide = len([e for e in erreurs if e.startswith('❌')]) == 0
    
    return valide, erreurs


# ================================================================================
# REFORMATAGE AUTOMATIQUE
# ================================================================================

def reformater_markdown(data: Dict) -> str:
    """Reformate le Markdown pour garantir structure correcte"""
    
    print("🔧 Reformatage du Markdown...")
    
    # Si moins de 6 articles principaux, promouvoir des "autres sujets"
    nb_manquants = 6 - len(data['articles_principaux'])
    
    if nb_manquants > 0 and data['autres_sujets']:
        print(f"⚡ Promotion de {nb_manquants} sujets vers articles principaux")
        
        for i in range(min(nb_manquants, len(data['autres_sujets']))):
            autre = data['autres_sujets'].pop(0)
            
            # Convertir en article principal
            article_converti = {
                'theme': 'Actualité',
                'titre': autre['titre'],
                'contenu_brut': autre['contenu']
            }
            data['articles_principaux'].append(article_converti)
    
    # Reconstruction Markdown
    markdown = []
    
    # Metadata
    if data['metadata']:
        markdown.append('---')
        for key, val in data['metadata'].items():
            markdown.append(f"{key}: {val}")
        markdown.append('---')
        markdown.append('')
    
    # Titre
    if data['titre']:
        markdown.append(f"# {data['titre']}")
        markdown.append('')
    
    # Édition
    if data['edition']:
        markdown.append(data['edition'])
        markdown.append('')
        markdown.append('---')
        markdown.append('')
    
    # Introduction
    if data['introduction']:
        markdown.append('## Introduction')
        markdown.append('')
        markdown.append(data['introduction'])
        markdown.append('')
        markdown.append('---')
        markdown.append('')
    
    # Articles principaux
    for art in data['articles_principaux'][:6]:  # Max 6
        markdown.append(f"## {art['theme']} – {art['titre']}")
        markdown.append('')
        markdown.extend(art['contenu_brut'])
        markdown.append('')
        markdown.append('---')
        markdown.append('')
    
    # Autres sujets
    if data['autres_sujets']:
        markdown.append('## Autres sujets de la semaine')
        markdown.append('')
        
        for autre in data['autres_sujets']:
            markdown.append(f"### {autre['titre']}")
            markdown.extend(autre['contenu'])
            markdown.append('')
        
        markdown.append('---')
        markdown.append('')
    
    # Fin
    markdown.append("**Fin de l'édition**")
    markdown.append("*Veille générée automatiquement par système 2-agents OpenAI*")
    
    return '\n'.join(markdown)


# ================================================================================
# MAIN
# ================================================================================

def main():
    """Point d'entrée principal"""
    
    try:
        print("=" * 80)
        print("🔍 AGENT VALIDATEUR MARKDOWN")
        print("=" * 80)
        print(f"⏰ Exécution : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print()
        
        service = get_drive_service()
        
        fichiers_corriges = 0
        
        for nom_fichier in FICHIERS:
            print(f"\n📄 Traitement : {nom_fichier}")
            print("-" * 80)
            
            # Télécharger
            contenu = telecharger_fichier(service, nom_fichier)
            
            # Parser
            print("🔍 Parsing Markdown...")
            data = parser_markdown(contenu)
            
            print(f"   ├─ Articles principaux : {len(data['articles_principaux'])}")
            print(f"   └─ Autres sujets : {len(data['autres_sujets'])}")
            
            # Valider
            print("✅ Validation structure...")
            valide, erreurs = valider_structure(data)
            
            if erreurs:
                print("⚠️  Problèmes détectés :")
                for err in erreurs:
                    print(f"   {err}")
            
            # Reformater si nécessaire
            if not valide or len(data['articles_principaux']) < 6:
                print("🔧 Reformatage nécessaire...")
                contenu_corrige = reformater_markdown(data)
                
                # Re-valider
                data_corrigee = parser_markdown(contenu_corrige)
                valide_apres, _ = valider_structure(data_corrigee)
                
                if valide_apres or len(data_corrigee['articles_principaux']) >= 6:
                    uploader_fichier(service, nom_fichier, contenu_corrige)
                    fichiers_corriges += 1
                    print("✅ Fichier corrigé et uploadé")
                else:
                    print("⚠️  Correction impossible, fichier conservé tel quel")
            else:
                print("✅ Structure valide, aucune correction nécessaire")
        
        print("\n" + "=" * 80)
        print("✅ VALIDATION TERMINÉE")
        print("=" * 80)
        print(f"📊 Fichiers traités : {len(FICHIERS)}")
        print(f"🔧 Fichiers corrigés : {fichiers_corriges}")
        print()
        
        sys.exit(0)
    
    except Exception as e:
        print("\n" + "=" * 80)
        print("❌ ERREUR FATALE")
        print("=" * 80)
        print(f"Type : {type(e).__name__}")
        print(f"Message : {e}")
        import traceback
        traceback.print_exc()
        print("=" * 80)
        sys.exit(1)


if __name__ == "__main__":
    main()
