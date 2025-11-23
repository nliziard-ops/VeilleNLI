import anthropic
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
import json
from datetime import datetime

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
        # Valeurs par défaut si le fichier n'existe pas
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
    
    # Lister les fichiers .md
    query = f"'{FOLDER_ID}' in parents and (name='VeilleIA.md' or name='VeilleNews.md')"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])
    
    fichiers_markdown = {}
    for file in files:
        # Télécharger le contenu
        content = service.files().get_media(fileId=file['id']).execute()
        fichiers_markdown[file['name']] = content.decode('utf-8')
        print(f"   ✓ {file['name']} téléchargé ({len(content)} octets)")
    
    return fichiers_markdown

def generer_site_web(fichiers_markdown, preferences):
    """Génère le site web via Claude API"""
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    
    # Déterminer le test de la semaine
    semaine = preferences['semaine_actuelle']
    cycle = preferences['cycle']
    test_actuel = cycle[(semaine - 1) % len(cycle)]
    
    # Construire le contexte des préférences
    j_aime = ', '.join(preferences['preferences']['j_aime']) if preferences['preferences']['j_aime'] else 'Aucun pour l\'instant'
    rejete = ', '.join(preferences['preferences']['rejete']) if preferences['preferences']['rejete'] else 'Aucun'
    
    contexte_prefs = f"""
PRÉFÉRENCES UTILISATEUR :
- Styles aimés (à intégrer) : {j_aime}
- Styles rejetés (NE JAMAIS utiliser) : {rejete}
- Test de cette semaine : {test_actuel.upper()}
- Semaine n°{semaine}
"""
    
    # Préparer le contenu des fichiers pour le prompt
    contenu_fichiers = ""
    for nom, contenu in fichiers_markdown.items():
        contenu_fichiers += f"\n\n=== FICHIER : {nom} ===\n{contenu}\n"
    
    prompt = """# **MISSION : Générateur de Site Web de Veille**

## **CONTEXTE**
Tu dois créer un site web d'une seule page HTML avec des onglets pour visualiser des synthèses de veille hebdomadaires.

""" + contexte_prefs + """

## **FICHIERS MARKDOWN FOURNIS**
""" + contenu_fichiers + """

## **CONTRAINTES CRITIQUES**

### 1. MISE EN FORME TRÈS ABOUTIE
- Design **professionnel et moderne** de qualité production
- **Esthétique soignée** dès la première version
- Chaque variante doit être **visuellement impressionnante**

### 2. TEST DE CETTE SEMAINE : """ + test_actuel.upper() + """
Tu dois créer une **NOUVELLE variante créative** de cet aspect :

- **Layout** : grille, colonnes, masonry, flexbox, disposition asymétrique...
- **Couleurs** : palettes sombres/claires, tons chauds/froids, contrastes, gradients...
- **Typographie** : polices (Google Fonts), tailles, poids, hiérarchie, espacement...
- **Visualisation** : cartes, badges, icônes, timeline, indicateurs visuels...
- **Animations** : transitions, hover effects, accordéons, parallax, fade-in...

### 3. RESPECTER LES PRÉFÉRENCES
- **Intégrer** les éléments des styles "j'aime"
- **NE JAMAIS utiliser** les styles "rejetés"

## **STRUCTURE REQUISE**

### En haut de page (discret)
Un petit bandeau en haut indiquant le style testé cette semaine.

### Système d'onglets
- **2 onglets** : "Veille IA" et "Veille Actualités"
- Navigation fluide entre les onglets
- Onglet actif visuellement distinct

### Double niveau d'affichage

**Vue synthétique (par défaut)** :
- Affichage rapide à scanner (10-15 min de lecture)
- Présentation condensée des sections principales
- Chaque section cliquable pour voir le détail

**Vue détaillée (au clic)** :
- Affichage complet du contenu d'une section
- Mise en forme enrichie et esthétique
- Retour facile à la vue synthétique

## **SPÉCIFICATIONS TECHNIQUES**

- **Fichier HTML autonome** avec CSS inline et JavaScript vanilla
- **Responsive** : fonctionne sur desktop, tablette, mobile
- **Performance** : chargement rapide, animations fluides
- **Accessibilité** : contraste suffisant, navigation clavier possible
- **Compatibilité** : Chrome, Firefox, Safari, Edge modernes

## **PARSING DU MARKDOWN**

- Utilise JavaScript pour parser le markdown côté client
- Affiche correctement les titres, listes, liens, citations
- Préserve la structure hiérarchique du contenu
- Liens cliquables et fonctionnels

## **CONSIGNES DE CRÉATIVITÉ**

- Sois **audacieux** dans le design
- Teste des approches **modernes et innovantes**
- Utilise des **effets visuels subtils mais impactants**
- Crée une expérience utilisateur **mémorable**
- Le design doit faire dire "Wow, c'est beau !"

## **OUTPUT**

Génère **UNIQUEMENT** le code HTML complet, prêt à être sauvegardé dans un fichier .html

- Pas de commentaires explicatifs avant ou après le code
- Pas de balises markdown
- Juste le code HTML pur, de <!DOCTYPE html> à </html>
- Code production-ready, testé mentalement

**GÉNÈRE LE SITE MAINTENANT.**
"""
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8000,
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )
    
    # Extraire le HTML de la réponse
    html_content = message.content[0].text
    
    # Nettoyer si des balises markdown persistent
    html_content = html_content.replace('```html', '').replace('```', '').strip()
    
    return html_content

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
    print("🚀 Démarrage Agent Générateur Web...")
    print(f"⏰ Date d'exécution : {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    # Charger les préférences
    print("\n📂 Chargement des préférences...")
    preferences = charger_preferences()
    cycle = preferences['cycle']
    semaine = preferences['semaine_actuelle']
    test_actuel = cycle[(semaine - 1) % len(cycle)]
    print(f"   Semaine n°{semaine}")
    print(f"   Test de la semaine : {test_actuel.upper()}")
    
    # Télécharger les fichiers markdown
    print("\n📥 Téléchargement des fichiers markdown depuis Google Drive...")
    try:
        fichiers = telecharger_fichiers_markdown()
        if not fichiers:
            print("❌ ERREUR : Aucun fichier markdown trouvé dans Google Drive")
            print("   Vérifiez que VeilleIA.md et VeilleNews.md existent dans le dossier")
            return
        print(f"   ✓ {len(fichiers)} fichier(s) trouvé(s)")
    except Exception as e:
        print(f"❌ ERREUR lors du téléchargement : {e}")
        return
    
    # Générer le site
    print("\n🎨 Génération du site web...")
    print("   ⚠️  Cette opération peut prendre 1-2 minutes...")
    try:
        html = generer_site_web(fichiers, preferences)
        print(f"   ✓ Site généré ({len(html)} caractères)")
    except Exception as e:
        print(f"❌ ERREUR lors de la génération : {e}")
        return
    
    # Sauvegarder
    print("\n💾 Sauvegarde du site...")
    sauvegarder_site(html)
    
    # Incrémenter le compteur
    print("\n📊 Mise à jour des préférences...")
    incrementer_semaine(preferences)
    
    print("\n" + "="*60)
    print("✅ Agent Générateur Web terminé avec succès!")
    print(f"🌐 Site disponible à : https://nliziard-ops.github.io/VeilleNLI/")
    print("="*60)

if __name__ == "__main__":
    main()
