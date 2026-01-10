import anthropic
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
import json
from datetime import datetime
import re
from html.parser import HTMLParser

# Configuration
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')
GOOGLE_CREDENTIALS = json.loads(os.environ.get('GOOGLE_DRIVE_CREDENTIALS'))
FOLDER_ID = os.environ.get('GOOGLE_DRIVE_FOLDER_ID')

def charger_preferences():
    """Charge les préférences de style depuis le fichier config"""
    try:
        with open('config/styles_preferences.json', 'r') as f:
            return json.load(f)
    except:
        return {
            "semaine_actuelle": 1,
            "cycle": ["layout", "couleurs", "typographie", "visualisation", "animations"],
            "preferences": {
                "j_aime": [],
                "rejete": [],
                "pas_note": []
            }
        }

def sauvegarder_preferences(preferences):
    """Sauvegarde les préférences mises à jour"""
    os.makedirs('config', exist_ok=True)
    with open('config/styles_preferences.json', 'w') as f:
        json.dump(preferences, f, indent=2)

def telecharger_fichiers_markdown():
    """Télécharge tous les fichiers .md du dossier Drive"""
    credentials = service_account.Credentials.from_service_account_info(
        GOOGLE_CREDENTIALS,
        scopes=['https://www.googleapis.com/auth/drive.readonly']
    )
    
    service = build('drive', 'v3', credentials=credentials)
    
    query = f"'{FOLDER_ID}' in parents and (name='VeilleIA.md' or name='VeilleNews.md')"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])
    
    fichiers_markdown = {}
    for file in files:
        content = service.files().get_media(fileId=file['id']).execute()
        fichiers_markdown[file['name']] = content.decode('utf-8')
        print(f"   ✓ {file['name']} téléchargé ({len(content)} octets)")
    
    return fichiers_markdown

def parser_markdown_sections(contenu_md):
    """
    Parse le Markdown et extrait les sections principales
    Retourne : (sujets_importants, sujets_secondaires, synthese_finale)
    """
    lignes = contenu_md.split('\n')
    sections = []
    section_actuelle = None
    synthese_finale = ""
    
    # Sections à exclure du découpage
    exclusions = ['introduction', 'table des matières', 'synthèse finale', 'fin de l\'édition']
    
    for ligne in lignes:
        # Détecter les titres de niveau 2 (##)
        if ligne.strip().startswith('## '):
            titre = ligne.strip()[3:].strip()
            titre_lower = titre.lower()
            
            # Vérifier si c'est la synthèse finale
            if 'synthèse finale' in titre_lower:
                section_actuelle = {'titre': titre, 'contenu': '', 'est_synthese': True}
            # Exclure certaines sections
            elif any(excl in titre_lower for excl in exclusions):
                section_actuelle = None
            else:
                # Sauvegarder la section précédente
                if section_actuelle and not section_actuelle.get('est_synthese'):
                    sections.append(section_actuelle)
                # Créer nouvelle section
                section_actuelle = {'titre': titre, 'contenu': ''}
        
        # Ajouter le contenu à la section actuelle
        elif section_actuelle:
            if section_actuelle.get('est_synthese'):
                synthese_finale += ligne + '\n'
            else:
                section_actuelle['contenu'] += ligne + '\n'
    
    # Ajouter la dernière section
    if section_actuelle and not section_actuelle.get('est_synthese'):
        sections.append(section_actuelle)
    
    # Séparer en sujets importants (6 premiers) et secondaires (reste)
    sujets_importants = sections[:6]
    sujets_secondaires = sections[6:]
    
    return sujets_importants, sujets_secondaires, synthese_finale

def tronquer_texte(texte, nb_mots=40):
    """
    Tronque un texte à nb_mots et ajoute '...' si nécessaire
    Retourne : (texte_court, texte_complet, est_tronque)
    """
    # Nettoyer le texte
    texte = texte.strip()
    
    # Extraire juste le premier paragraphe (section "Résumé")
    # Chercher la première ligne non vide après "### Résumé"
    lignes = texte.split('\n')
    resume = ""
    capture = False
    
    for ligne in lignes:
        ligne_clean = ligne.strip()
        if '### résumé' in ligne_clean.lower() or '**résumé**' in ligne_clean.lower():
            capture = True
            continue
        if capture and ligne_clean and not ligne_clean.startswith('#') and not ligne_clean.startswith('**'):
            resume = ligne_clean
            break
    
    if not resume:
        # Fallback : prendre le premier paragraphe non vide
        for ligne in lignes:
            if ligne.strip() and not ligne.strip().startswith('#'):
                resume = ligne.strip()
                break
    
    # Découper en mots
    mots = resume.split()
    
    if len(mots) <= nb_mots:
        return resume, resume, False
    
    texte_court = ' '.join(mots[:nb_mots]) + '...'
    return texte_court, resume, True

def extraire_points_cles(synthese_finale):
    """Extrait les points clés de la synthèse finale"""
    points = []
    lignes = synthese_finale.split('\n')
    
    # Chercher les sections pertinentes
    capture = False
    for ligne in lignes:
        ligne_clean = ligne.strip()
        
        # Détecter les sections de points clés
        if any(keyword in ligne_clean.lower() for keyword in ['points clés', 'événements majeurs', 'signaux faibles']):
            capture = True
            continue
        
        # Arrêter à la prochaine section
        if ligne_clean.startswith('###') and capture:
            capture = False
        
        # Capturer les points (lignes commençant par - ou numéros)
        if capture and (ligne_clean.startswith('-') or ligne_clean.startswith('•') or 
                       (ligne_clean and ligne_clean[0].isdigit() and '. ' in ligne_clean)):
            point = ligne_clean.lstrip('-•0123456789. ').strip()
            if point:
                points.append(point)
    
    return points[:5]  # Maximum 5 points

class HTMLValidator(HTMLParser):
    """Validateur HTML simple"""
    def __init__(self):
        super().__init__()
        self.tags = []
        self.errors = []
    
    def handle_starttag(self, tag, attrs):
        if tag not in ['img', 'br', 'hr', 'input', 'meta', 'link']:
            self.tags.append(tag)
    
    def handle_endtag(self, tag):
        if self.tags and self.tags[-1] == tag:
            self.tags.pop()
        elif tag not in ['img', 'br', 'hr', 'input', 'meta', 'link']:
            self.errors.append(f"Tag fermant sans ouverture : {tag}")
    
    def is_valid(self):
        return len(self.errors) == 0 and len(self.tags) == 0

def verifier_html_genere(html_content, sujets_ia, sujets_news):
    """
    Vérifie la validité et l'intégrité du HTML généré
    Retourne : (bool_valide, dict_details)
    """
    checks = {}
    
    # 1. Validité HTML de base
    validator = HTMLValidator()
    try:
        validator.feed(html_content)
        checks['html_valide'] = validator.is_valid()
        if not checks['html_valide']:
            checks['html_erreurs'] = validator.errors + [f"Tags non fermés: {validator.tags}"]
    except Exception as e:
        checks['html_valide'] = False
        checks['html_erreurs'] = [str(e)]
    
    # 2. Présence de tous les sujets IA
    sujets_ia_manquants = []
    for sujet in sujets_ia:
        titre = sujet['titre']
        if titre not in html_content:
            sujets_ia_manquants.append(titre)
    checks['tous_sujets_ia'] = len(sujets_ia_manquants) == 0
    if sujets_ia_manquants:
        checks['sujets_ia_manquants'] = sujets_ia_manquants
    
    # 3. Présence de tous les sujets News
    sujets_news_manquants = []
    for sujet in sujets_news:
        titre = sujet['titre']
        if titre not in html_content:
            sujets_news_manquants.append(titre)
    checks['tous_sujets_news'] = len(sujets_news_manquants) == 0
    if sujets_news_manquants:
        checks['sujets_news_manquants'] = sujets_news_manquants
    
    # 4. Présence des éléments essentiels
    elements_requis = {
        'menu_lateral': '<nav' in html_content or 'sidebar' in html_content.lower(),
        'section_ia': 'veille-ia' in html_content.lower() or 'veille ia' in html_content.lower(),
        'section_news': 'actualités' in html_content.lower() or 'actualites' in html_content.lower(),
        'points_cles': 'points clés' in html_content.lower() or 'points cles' in html_content.lower(),
        'javascript': '<script' in html_content,
        'modal_system': 'modal' in html_content.lower()
    }
    checks['elements_essentiels'] = elements_requis
    checks['tous_elements_presents'] = all(elements_requis.values())
    
    # 5. Vérification des liens/sources
    checks['liens_presents'] = 'http://' in html_content or 'https://' in html_content
    
    # Résultat global
    checks_critiques = [
        checks['html_valide'],
        checks['tous_sujets_ia'],
        checks['tous_sujets_news'],
        checks['tous_elements_presents']
    ]
    
    est_valide = all(checks_critiques)
    
    return est_valide, checks

def generer_site_web_avec_verification(fichiers_markdown, preferences, max_tentatives=3):
    """
    Génère le site web avec système de vérification et régénération
    """
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    
    # Parser les fichiers Markdown
    print("   📊 Parsing des fichiers Markdown...")
    data_veilles = {}
    
    for nom_fichier, contenu_md in fichiers_markdown.items():
        sujets_imp, sujets_sec, synthese = parser_markdown_sections(contenu_md)
        points_cles = extraire_points_cles(synthese)
        
        # Préparer les sujets avec résumés tronqués
        for sujet in sujets_imp:
            court, complet, tronque = tronquer_texte(sujet['contenu'], 40)
            sujet['resume_court'] = court
            sujet['resume_complet'] = complet
            sujet['est_tronque'] = tronque
        
        data_veilles[nom_fichier] = {
            'sujets_importants': sujets_imp,
            'sujets_secondaires': sujets_sec,
            'points_cles': points_cles,
            'contenu_brut': contenu_md
        }
    
    print(f"      ✓ VeilleIA.md : {len(data_veilles.get('VeilleIA.md', {}).get('sujets_importants', []))} sujets importants, {len(data_veilles.get('VeilleIA.md', {}).get('sujets_secondaires', []))} secondaires")
    print(f"      ✓ VeilleNews.md : {len(data_veilles.get('VeilleNews.md', {}).get('sujets_importants', []))} sujets importants, {len(data_veilles.get('VeilleNews.md', {}).get('sujets_secondaires', []))} secondaires")
    
    # Boucle de génération avec vérification
    for tentative in range(1, max_tentatives + 1):
        print(f"\n   🎨 Génération du site (tentative {tentative}/{max_tentatives})...")
        
        try:
            # Construire le prompt
            prompt = construire_prompt_generation(data_veilles, preferences)
            
            # Appeler Claude
            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=16000,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            html_content = message.content[0].text
            html_content = html_content.replace('```html', '').replace('```', '').strip()
            
            print(f"      ✓ HTML généré ({len(html_content)} caractères)")
            
            # Vérification
            print(f"   🔍 Vérification de l'intégrité (tentative {tentative}/{max_tentatives})...")
            est_valide, details_checks = verifier_html_genere(
                html_content,
                data_veilles.get('VeilleIA.md', {}).get('sujets_importants', []) + 
                data_veilles.get('VeilleIA.md', {}).get('sujets_secondaires', []),
                data_veilles.get('VeilleNews.md', {}).get('sujets_importants', []) + 
                data_veilles.get('VeilleNews.md', {}).get('sujets_secondaires', [])
            )
            
            if est_valide:
                print("      ✅ Vérification réussie !")
                print(f"         - HTML valide: {details_checks['html_valide']}")
                print(f"         - Tous sujets IA présents: {details_checks['tous_sujets_ia']}")
                print(f"         - Tous sujets News présents: {details_checks['tous_sujets_news']}")
                print(f"         - Éléments essentiels: {details_checks['tous_elements_presents']}")
                return html_content, True, details_checks
            else:
                print(f"      ⚠️  Vérification échouée (tentative {tentative}/{max_tentatives})")
                print(f"         - HTML valide: {details_checks['html_valide']}")
                print(f"         - Tous sujets IA présents: {details_checks['tous_sujets_ia']}")
                print(f"         - Tous sujets News présents: {details_checks['tous_sujets_news']}")
                print(f"         - Éléments essentiels: {details_checks['tous_elements_presents']}")
                
                if tentative < max_tentatives:
                    print(f"      🔄 Régénération en cours...")
                else:
                    print(f"      ❌ Échec après {max_tentatives} tentatives. Le site sera quand même sauvegardé.")
                    return html_content, False, details_checks
        
        except Exception as e:
            print(f"      ❌ ERREUR lors de la génération : {e}")
            if tentative < max_tentatives:
                print(f"      🔄 Nouvelle tentative...")
            else:
                raise
    
    return None, False, {}

def construire_prompt_generation(data_veilles, preferences):
    """Construit le prompt pour Claude avec toutes les données parsées"""
    
    # Préparer les données IA
    ia_data = data_veilles.get('VeilleIA.md', {})
    ia_importants = ia_data.get('sujets_importants', [])
    ia_secondaires = ia_data.get('sujets_secondaires', [])
    ia_points_cles = ia_data.get('points_cles', [])
    
    # Préparer les données News
    news_data = data_veilles.get('VeilleNews.md', {})
    news_importants = news_data.get('sujets_importants', [])
    news_secondaires = news_data.get('sujets_secondaires', [])
    news_points_cles = news_data.get('points_cles', [])
    
    prompt = f"""# MISSION : Générateur de Site Web de Veille - Version 2 Onglets

## CONTEXTE
Tu dois créer un site web d'une seule page HTML avec 2 ONGLETS pour visualiser les veilles IA et Actualités.

## STRUCTURE OBLIGATOIRE

### Layout global
- **1 PAGE HTML UNIQUE**
- Menu latéral gauche (30-40px) avec 2 boutons : "Veille IA" / "Actualités"
- **2 SECTIONS** masquables via JavaScript (une visible à la fois)
- Style Comics/BD moderne et élégant

### MENU LATÉRAL (30-40px)
- Fixe à gauche
- 2 boutons verticaux avec icônes
- Clic sur bouton → masque section active et affiche la nouvelle
- Fond coloré style comics

### CHAQUE SECTION (IA et Actualités) CONTIENT :

#### 1. GRILLE DE 6 CARTES COMICS (Sujets Importants)
- Disposition : 2 colonnes x 3 lignes OU 3 colonnes x 2 lignes
- Chaque carte :
  * Icône/Emoji en haut
  * **Titre du sujet** (1-2 lignes max)
  * **Résumé tronqué à 40 mots** avec "..." à la fin si tronqué
  * Clic sur résumé → expand pour afficher le résumé complet (dans la carte)
  * Bouton "Lire +" → ouvre modal avec TOUT le détail du sujet
- Style BD : bordures nettes, ombres, couleurs vives

#### 2. LISTE DES SUJETS SECONDAIRES (en bas)
- Titre : "Autres sujets de la semaine"
- Liste compacte :
  * **Titre du sujet en gras**
  * Description = résumé complet (pas tronqué)
  * Clic sur titre → ouvre modal avec détail complet

#### 3. SECTION POINTS CLÉS
- Titre : "POINTS CLÉS À RETENIR"
- 3-5 bullet points extraits de la synthèse
- Design sobre mais visible

### MODALS (CRITIQUES - DOIVENT FONCTIONNER)
**CHAQUE SUJET** doit avoir son propre modal avec :
- Overlay semi-transparent derrière
- Contenu complet du sujet :
  1. **Titre du sujet**
  2. **Résumé complet**
  3. **Points de vue croisés** (si présents)
  4. **Fiabilité & signaux faibles** (si présents)
  5. **Sources** avec liens cliquables
- Bouton [X] en haut à droite
- Clic en dehors → ferme le modal
- **JAVASCRIPT OBLIGATOIRE** : fonctions openModal(id) et closeModal()

## DONNÉES FOURNIES

### VEILLE IA

**Sujets importants (6 cartes) :**
{json.dumps([{
    'titre': s['titre'],
    'resume_court': s['resume_court'],
    'resume_complet': s['resume_complet'],
    'contenu_complet': s['contenu']
} for s in ia_importants], ensure_ascii=False, indent=2)}

**Sujets secondaires (liste) :**
{json.dumps([{
    'titre': s['titre'],
    'resume': s['contenu'].split('###')[0].strip()[:200] + '...',
    'contenu_complet': s['contenu']
} for s in ia_secondaires], ensure_ascii=False, indent=2)}

**Points clés :**
{json.dumps(ia_points_cles, ensure_ascii=False, indent=2)}

### VEILLE ACTUALITÉS

**Sujets importants (6 cartes) :**
{json.dumps([{
    'titre': s['titre'],
    'resume_court': s['resume_court'],
    'resume_complet': s['resume_complet'],
    'contenu_complet': s['contenu']
} for s in news_importants], ensure_ascii=False, indent=2)}

**Sujets secondaires (liste) :**
{json.dumps([{
    'titre': s['titre'],
    'resume': s['contenu'].split('###')[0].strip()[:200] + '...',
    'contenu_complet': s['contenu']
} for s in news_secondaires], ensure_ascii=False, indent=2)}

**Points clés :**
{json.dumps(news_points_cles, ensure_ascii=False, indent=2)}

## CONTRAINTES TECHNIQUES

- HTML5 sémantique
- CSS inline OU balise <style> dans <head>
- JavaScript vanilla dans <script> avant </body>
- Pas de bibliothèques externes (sauf Google Fonts si besoin)
- Compatible tous navigateurs récents
- Responsive (desktop prioritaire)

## JAVASCRIPT REQUIS

```javascript
// Navigation entre onglets
function showTab(tabName) {{
    // Masquer toutes les sections
    document.querySelectorAll('.veille-section').forEach(s => s.style.display = 'none');
    // Afficher la section demandée
    document.getElementById('veille-' + tabName).style.display = 'block';
    // Gérer les boutons actifs
    document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
    document.querySelector('.nav-btn[data-tab="' + tabName + '"]').classList.add('active');
}}

// Expand/collapse résumés dans les cartes
function toggleResume(cardId) {{
    const card = document.getElementById(cardId);
    const court = card.querySelector('.resume-court');
    const complet = card.querySelector('.resume-complet');
    // Toggle visibility
}}

// Gestion des modals
function openModal(modalId) {{
    document.getElementById('modal-' + modalId).style.display = 'flex';
}}

function closeModal(modalId) {{
    document.getElementById('modal-' + modalId).style.display = 'none';
}}

// Fermer modal si clic en dehors
window.onclick = function(event) {{
    if (event.target.classList.contains('modal')) {{
        event.target.style.display = 'none';
    }}
}}
```

## STYLE COMICS/BD

- Couleurs vives et contrastées
- Bordures épaisses noires autour des cartes
- Ombres portées (box-shadow)
- Polices lisibles et impactantes
- Icônes/emojis grandes et visibles
- Boutons stylisés façon comics

## CHECKLIST DE VALIDATION

Ton HTML DOIT contenir :
- ✅ Menu latéral avec 2 boutons fonctionnels
- ✅ 2 sections (veille-ia et veille-actualites)
- ✅ 6 cartes par section avec résumés tronqués
- ✅ Listes des sujets secondaires
- ✅ Sections points clés
- ✅ 1 modal par sujet (IA + News)
- ✅ JavaScript pour navigation et modals
- ✅ Tous les titres de sujets présents
- ✅ Tous les liens sources présents

## OUTPUT

Génère UNIQUEMENT le code HTML complet de <!DOCTYPE html> à </html>

- Pas de commentaires avant/après
- Pas de balises markdown
- Code production-ready
- Tout fonctionne immédiatement

GÉNÈRE LE SITE MAINTENANT.
"""
    
    return prompt

def sauvegarder_site(html_content):
    """Sauvegarde le site dans docs/index.html pour GitHub Pages"""
    os.makedirs('docs', exist_ok=True)
    with open('docs/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("✅ Site web sauvegardé dans docs/index.html")

def incrementer_semaine(preferences):
    """Incrémente le compteur de semaine"""
    preferences['semaine_actuelle'] += 1
    sauvegarder_preferences(preferences)
    print(f"✅ Compteur de semaine incrémenté : semaine {preferences['semaine_actuelle']}")

def main():
    print("🚀 Démarrage Agent Générateur Web V2...")
    print(f"⏰ Date d'exécution : {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    print("\n📂 Chargement des préférences...")
    preferences = charger_preferences()
    print(f"   Semaine n°{preferences['semaine_actuelle']}")
    
    print("\n📥 Téléchargement des fichiers markdown depuis Google Drive...")
    try:
        fichiers = telecharger_fichiers_markdown()
        if not fichiers:
            print("❌ ERREUR : Aucun fichier markdown trouvé")
            return
        print(f"   ✓ {len(fichiers)} fichier(s) trouvé(s)")
    except Exception as e:
        print(f"❌ ERREUR lors du téléchargement : {e}")
        return
    
    print("\n🎨 Génération du site web avec vérification...")
    try:
        html, est_valide, details = generer_site_web_avec_verification(fichiers, preferences, max_tentatives=3)
        
        if html:
            print(f"\n   ✓ Site généré ({len(html)} caractères)")
            if est_valide:
                print("   ✅ Toutes les vérifications sont passées")
            else:
                print("   ⚠️  Le site a été généré mais certaines vérifications ont échoué")
                print(f"   📊 Détails: {json.dumps(details, indent=2, ensure_ascii=False)}")
        else:
            print("❌ ERREUR : Impossible de générer le site")
            return
            
    except Exception as e:
        print(f"❌ ERREUR lors de la génération : {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("\n💾 Sauvegarde du site...")
    sauvegarder_site(html)
    
    print("\n📊 Mise à jour des préférences...")
    incrementer_semaine(preferences)
    
    print("\n" + "="*60)
    print("✅ Agent Générateur Web V2 terminé avec succès!")
    print(f"🌐 Site disponible à : https://nliziard-ops.github.io/VeilleNLI/")
    print("="*60)

if __name__ == "__main__":
    main()
