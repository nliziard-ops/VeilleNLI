#!/usr/bin/env python3
"""
Agent Générateur JSON - VeilleNLI  
Lit les fichiers Markdown depuis Google Drive et génère data.json pour le site dynamique
"""

import os
import json
import re
from datetime import datetime
from typing import Dict, List, Tuple
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Configuration
GOOGLE_CREDENTIALS = json.loads(os.environ.get('GOOGLE_DRIVE_CREDENTIALS'))
FOLDER_ID = os.environ.get('GOOGLE_DRIVE_FOLDER_ID')


def telecharger_fichiers_markdown() -> Dict[str, str]:
    """
    Télécharge les fichiers .md depuis Google Drive
    Returns: Dict avec nom_fichier -> contenu_markdown
    """
    print("📥 Connexion à Google Drive...")
    
    credentials = service_account.Credentials.from_service_account_info(
        GOOGLE_CREDENTIALS,
        scopes=['https://www.googleapis.com/auth/drive.readonly']
    )
    
    service = build('drive', 'v3', credentials=credentials)
    
    # Rechercher les fichiers de veille
    query = f"'{FOLDER_ID}' in parents and (name='VeilleIA.md' or name='VeilleNews.md')"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])
    
    if not files:
        print("⚠️  Aucun fichier de veille trouvé dans Google Drive")
        return {}
    
    fichiers_markdown = {}
    for file in files:
        content = service.files().get_media(fileId=file['id']).execute()
        contenu_decode = content.decode('utf-8')
        fichiers_markdown[file['name']] = contenu_decode
        print(f"   ✓ {file['name']} téléchargé ({len(contenu_decode)} caractères)")
    
    return fichiers_markdown


def extraire_metadata(contenu_md: str) -> Dict[str, str]:
    """
    Extrait les métadonnées du front matter YAML
    Returns: Dict avec agent, date, catégorie
    """
    metadata = {
        'agent': 'Agent Veille',
        'date': datetime.now().strftime('%Y-%m-%d'),
        'categorie': 'Veille'
    }
    
    # Chercher le front matter entre ---
    match = re.match(r'^---\n(.*?)\n---', contenu_md, re.DOTALL)
    if match:
        yaml_content = match.group(1)
        for ligne in yaml_content.split('\n'):
            if ':' in ligne:
                cle, valeur = ligne.split(':', 1)
                metadata[cle.strip()] = valeur.strip()
    
    return metadata


def extraire_titre_principal(contenu_md: str) -> Tuple[str, str]:
    """
    Extrait le titre principal (# niveau 1) et l'édition
    Returns: (titre, edition)
    """
    lignes = contenu_md.split('\n')
    titre = "Veille hebdomadaire"
    edition = ""
    
    for i, ligne in enumerate(lignes):
        # Chercher le titre de niveau 1
        if ligne.strip().startswith('# '):
            titre = ligne.strip()[2:].strip().replace('**', '')
            # L'édition est souvent sur la ligne suivante
            if i + 1 < len(lignes):
                ligne_suivante = lignes[i + 1].strip()
                if ligne_suivante.startswith('**Édition') or ligne_suivante.startswith('**Edition'):
                    edition = ligne_suivante.replace('**', '').strip()
            break
    
    return titre, edition


def extraire_introduction(contenu_md: str) -> str:
    """
    Extrait le paragraphe d'introduction
    Returns: texte de l'introduction
    """
    lignes = contenu_md.split('\n')
    introduction = ""
    capture = False
    
    for ligne in lignes:
        ligne_clean = ligne.strip()
        
        # Commencer après "## Introduction" ou "## **Introduction**"
        if '## ' in ligne_clean and 'introduction' in ligne_clean.lower():
            capture = True
            continue
        
        # Arrêter à la prochaine section ##
        if capture and ligne_clean.startswith('## '):
            break
        
        # Capturer le texte
        if capture and ligne_clean and not ligne_clean.startswith('---'):
            introduction += ligne_clean + " "
    
    return introduction.strip()


def parser_sujet(contenu_section: str, titre_section: str) -> Dict:
    """
    Parse une section complète de sujet
    Returns: Dict avec titre, resume, points_de_vue, fiabilite, sources
    """
    sujet = {
        'titre': titre_section,
        'resume': '',
        'resume_court': '',
        'resume_complet': '',
        'points_de_vue': [],
        'fiabilite': [],
        'sources': [],
        'contenu_complet': contenu_section
    }
    
    lignes = contenu_section.split('\n')
    section_actuelle = None
    source_actuelle = None
    
    for ligne in lignes:
        ligne_clean = ligne.strip()
        
        # Détecter les sous-sections (###)
        if ligne_clean.startswith('### '):
            section_actuelle = ligne_clean[4:].strip().lower().replace('**', '').replace('*', '')
            source_actuelle = None
            continue
        
        # Section Résumé
        if section_actuelle and 'résumé' in section_actuelle:
            if ligne_clean and not ligne_clean.startswith('#'):
                sujet['resume'] += ligne_clean + " "
        
        # Section Points de vue croisés
        elif section_actuelle and 'points de vue' in section_actuelle:
            # Détecter une nouvelle source (format **Source X – Nom**)
            if ligne_clean.startswith('**Source') or ligne_clean.startswith('**Média'):
                source_match = re.match(r'\*\*.*?–\s*(.*?)\*\*', ligne_clean)
                if source_match:
                    source_actuelle = {
                        'nom': source_match.group(1).strip(),
                        'texte': ''
                    }
                    sujet['points_de_vue'].append(source_actuelle)
            elif source_actuelle and ligne_clean and not ligne_clean.startswith('#'):
                source_actuelle['texte'] += ligne_clean + " "
        
        # Section Fiabilité & signaux faibles
        elif section_actuelle and ('fiabilité' in section_actuelle or 'signaux' in section_actuelle):
            if ligne_clean.startswith('-') or ligne_clean.startswith('•'):
                point = ligne_clean.lstrip('-•').strip()
                if point:
                    sujet['fiabilite'].append(point)
        
        # Section Sources
        elif section_actuelle and 'sources' in section_actuelle:
            # Format attendu : "- Titre – URL" ou "- Titre - URL"
            if ligne_clean.startswith('-') or ligne_clean.startswith('•'):
                source_text = ligne_clean.lstrip('-•').strip()
                # Séparer titre et URL
                separateurs = [' – ', ' - ', ' — ']
                for sep in separateurs:
                    if sep in source_text:
                        parts = source_text.split(sep, 1)
                        if len(parts) == 2:
                            titre_source = parts[0].strip()
                            url = parts[1].strip()
                            sujet['sources'].append({
                                'titre': titre_source,
                                'url': url
                            })
                        break
                else:
                    # Fallback : si c'est juste une URL
                    if source_text.startswith('http'):
                        sujet['sources'].append({
                            'titre': 'Source',
                            'url': source_text
                        })
    
    # Générer résumé court (40 premiers mots)
    sujet['resume'] = sujet['resume'].strip()
    mots = sujet['resume'].split()
    if len(mots) > 40:
        sujet['resume_court'] = ' '.join(mots[:40]) + '...'
        sujet['resume_complet'] = sujet['resume']
    else:
        sujet['resume_court'] = sujet['resume']
        sujet['resume_complet'] = sujet['resume']
    
    # Nettoyer les points de vue
    for pv in sujet['points_de_vue']:
        pv['texte'] = pv['texte'].strip()
    
    return sujet


def parser_sections(contenu_md: str) -> Tuple[List[Dict], List[Dict]]:
    """
    Parse toutes les sections du Markdown
    Returns: (sujets_importants (6 premiers), sujets_secondaires (reste))
    """
    lignes = contenu_md.split('\n')
    sections = []
    section_actuelle = None
    capture = False
    
    # Sections à exclure - LIGNE 236 CORRIGEE SANS APOSTROPHE
    exclusions = ["introduction", "table des matieres", "synthese finale", "fin de l edition", "fin de l edition"]
    
    for ligne in lignes:
        ligne_clean = ligne.strip()
        
        # Détecter les sections de niveau 2 (##)
        if ligne_clean.startswith('## '):
            titre = ligne_clean[3:].strip().replace('**', '')
            titre_lower = titre.lower()
            
            # Vérifier si on doit exclure cette section
            if any(excl in titre_lower for excl in exclusions):
                # Sauvegarder la section précédente avant d'exclure
                if section_actuelle and capture:
                    sections.append(section_actuelle)
                capture = False
                section_actuelle = None
                continue
            
            # Sauvegarder la section précédente
            if section_actuelle and capture:
                sections.append(section_actuelle)
            
            # Créer une nouvelle section
            section_actuelle = {
                'titre': titre,
                'contenu': ''
            }
            capture = True
        
        # Ajouter le contenu à la section actuelle
        elif section_actuelle and capture:
            section_actuelle['contenu'] += ligne + '\n'
    
    # Ajouter la dernière section
    if section_actuelle and capture:
        sections.append(section_actuelle)
    
    # Parser chaque section en sujet structuré
    sujets_structures = []
    for section in sections:
        sujet = parser_sujet(section['contenu'], section['titre'])
        sujets_structures.append(sujet)
    
    # Séparer en importants (6 premiers) et secondaires (reste)
    sujets_importants = sujets_structures[:6] if len(sujets_structures) >= 6 else sujets_structures
    sujets_secondaires = sujets_structures[6:] if len(sujets_structures) > 6 else []
    
    return sujets_importants, sujets_secondaires


def extraire_points_cles(contenu_md: str) -> List[str]:
    """
    Extrait les points clés de la synthèse finale
    Returns: Liste de points clés (max 5)
    """
    points = []
    lignes = contenu_md.split('\n')
    capture = False
    
    for ligne in lignes:
        ligne_clean = ligne.strip()
        
        # Détecter la section "Points clés"
        if '### ' in ligne_clean and ('points clés' in ligne_clean.lower() or 'points cles' in ligne_clean.lower()):
            capture = True
            continue
        
        # Arrêter à la prochaine sous-section ###
        if capture and ligne_clean.startswith('### '):
            break
        
        # Capturer les points (numérotés ou puces)
        if capture:
            # Format numéroté : "1. ", "2. ", etc.
            match_numero = re.match(r'^\d+\.\s+(.+)$', ligne_clean)
            if match_numero:
                points.append(match_numero.group(1).strip())
            # Format puce : "- " ou "• "
            elif ligne_clean.startswith('-') or ligne_clean.startswith('•'):
                point = ligne_clean.lstrip('-•').strip()
                if point:
                    points.append(point)
    
    return points[:5]  # Maximum 5 points


def generer_icone_categorie(titre: str) -> str:
    """
    Génère un emoji/icône adapté à la catégorie du sujet
    Returns: emoji string
    """
    titre_lower = titre.lower()
    
    # Mapping catégories -> icônes
    mappings = {
        'technolog': '⚙️',
        'modèle': '🤖',
        'llm': '🤖',
        'open source': '🇨🇳',
        'chine': '🇨🇳',
        'recherche': '🔬',
        'scientific': '🔬',
        'régulation': '⚖️',
        'gouvernance': '⚖️',
        'europe': '🇪🇺',
        'industrie': '💼',
        'investissement': '💼',
        'marché': '💼',
        'cybersécurité': '🔒',
        'sécurité': '🔒',
        'risque': '⚠️',
        'application': '💻',
        'usage': '💻',
        'hardware': '🔧',
        'compute': '🔧',
        'international': '🌍',
        'géopolitique': '🌍',
        'politique': '🏛️',
        'économie': '💰',
        'entreprise': '💼',
        'technologie': '💻',
        'innovation': '💡',
        'écologie': '🌱',
        'environnement': '🌱',
        'transition': '♻️',
        'nantes': '📍',
        'région': '📍'
    }
    
    for mot_cle, icone in mappings.items():
        if mot_cle in titre_lower:
            return icone
    
    return '📄'  # Icône par défaut


def traiter_fichier_markdown(nom_fichier: str, contenu_md: str) -> Dict:
    """
    Traite un fichier Markdown complet et retourne un objet structuré
    Returns: Dict avec toutes les données extraites
    """
    print(f"\n📊 Traitement de {nom_fichier}...")
    
    # Extraction des métadonnées
    metadata = extraire_metadata(contenu_md)
    print(f"   ✓ Métadonnées: {metadata['agent']} - {metadata['date']}")
    
    # Extraction du titre et édition
    titre, edition = extraire_titre_principal(contenu_md)
    print(f"   ✓ Titre: {titre}")
    if edition:
        print(f"   ✓ Édition: {edition}")
    
    # Extraction de l'introduction
    introduction = extraire_introduction(contenu_md)
    print(f"   ✓ Introduction: {len(introduction)} caractères")
    
    # Parser les sections
    sujets_importants, sujets_secondaires = parser_sections(contenu_md)
    print(f"   ✓ Sujets importants: {len(sujets_importants)}")
    print(f"   ✓ Sujets secondaires: {len(sujets_secondaires)}")
    
    # Ajouter des icônes aux sujets
    for sujet in sujets_importants + sujets_secondaires:
        sujet['icone'] = generer_icone_categorie(sujet['titre'])
    
    # Extraire les points clés
    points_cles = extraire_points_cles(contenu_md)
    print(f"   ✓ Points clés: {len(points_cles)}")
    
    return {
        'metadata': metadata,
        'titre': titre,
        'edition': edition,
        'introduction': introduction,
        'sujets_importants': sujets_importants,
        'sujets_secondaires': sujets_secondaires,
        'points_cles': points_cles,
        'date_generation': datetime.now().isoformat()
    }


def generer_data_json(fichiers_markdown: Dict[str, str]) -> Dict:
    """
    Génère la structure JSON complète pour le site web
    Returns: Dict avec toutes les données de veille structurées
    """
    print("\n🔨 Génération de la structure JSON...")
    
    data = {
        'version': '2.0',
        'date_generation': datetime.now().isoformat(),
        'veilles': {}
    }
    
    # Traiter chaque fichier
    for nom_fichier, contenu_md in fichiers_markdown.items():
        # Déterminer le type de veille (ia ou news)
        if 'IA' in nom_fichier or 'ia' in nom_fichier:
            cle = 'ia'
        elif 'News' in nom_fichier or 'news' in nom_fichier:
            cle = 'news'
        else:
            cle = nom_fichier.replace('.md', '').lower()
        
        data['veilles'][cle] = traiter_fichier_markdown(nom_fichier, contenu_md)
    
    print(f"\n✅ Structure JSON générée avec succès")
    print(f"   - Veilles traitées: {', '.join(data['veilles'].keys())}")
    
    return data


def sauvegarder_json(data: Dict, chemin: str = 'docs/data.json'):
    """
    Sauvegarde les données en JSON
    """
    print(f"\n💾 Sauvegarde dans {chemin}...")
    
    # Créer le dossier docs si nécessaire
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    
    # Sauvegarder avec indentation pour lisibilité
    with open(chemin, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    taille = os.path.getsize(chemin)
    print(f"   ✓ Fichier sauvegardé: {taille} octets ({taille/1024:.1f} KB)")


def main():
    """Point d'entrée principal"""
    print("=" * 70)
    print("🚀 Agent Générateur JSON - VeilleNLI")
    print("=" * 70)
    print(f"⏰ Exécution: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
    
    try:
        # 1. Télécharger les fichiers Markdown
        fichiers_markdown = telecharger_fichiers_markdown()
        
        if not fichiers_markdown:
            print("\n❌ Aucun fichier à traiter. Arrêt.")
            return 1
        
        # 2. Générer la structure JSON
        data_json = generer_data_json(fichiers_markdown)
        
        # 3. Sauvegarder le fichier JSON
        sauvegarder_json(data_json, 'docs/data.json')
        
        print("\n" + "=" * 70)
        print("✅ Agent Générateur JSON terminé avec succès!")
        print("=" * 70)
        print(f"📊 Statistiques:")
        for cle, veille in data_json['veilles'].items():
            print(f"   - {cle.upper()}: {len(veille['sujets_importants'])} sujets principaux, "
                  f"{len(veille['sujets_secondaires'])} secondaires")
        print(f"\n🌐 Fichier disponible: docs/data.json")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
