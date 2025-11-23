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

def generer_site_web(fichiers_markdown, preferences):
    """Génère le site web via Claude API"""
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    
    semaine = preferences['semaine_actuelle']
    cycle = preferences['cycle']
    test_actuel = cycle[(semaine - 1) % len(cycle)]
    
    j_aime = ', '.join(preferences['preferences']['j_aime']) if preferences['preferences']['j_aime'] else 'Aucun pour le moment'
    rejete = ', '.join(preferences['preferences']['rejete']) if preferences['preferences']['rejete'] else 'Aucun'
    
    contexte_prefs = f"""
PRÉFÉRENCES UTILISATEUR :
- Styles aimés (à intégrer) : {j_aime}
- Styles rejetés (NE JAMAIS utiliser) : {rejete}
- Test de cette semaine : {test_actuel.upper()}
- Semaine numéro {semaine}
"""
    
    contenu_fichiers = ""
    for nom, contenu in fichiers_markdown.items():
        contenu_fichiers += f"\n\n=== FICHIER : {nom} ===\n{contenu}\n"
    
    prompt = """# MISSION : Générateur de Site Web de Veille - Style Comics

## CONTEXTE
Tu dois créer un site web d'une seule page HTML avec navigation latérale pour visualiser des synthèses de veille hebdomadaires.

""" + contexte_prefs + """

## FICHIERS MARKDOWN FOURNIS
""" + contenu_fichiers + """

## STRUCTURE VISUELLE OBLIGATOIRE

### Layout global
- Menu latéral gauche très fin (30-40px)
- Zone principale avec grille de 6 cases (2 colonnes x 3 lignes)
- Section "Points clés" en bas

### MENU LATÉRAL (30-40px de large)
- Fixe à gauche de l'écran
- 2 boutons verticaux : "Veille IA" et "Veille Actualités"
- Fond sombre ou coloré
- Icônes + texte vertical OU juste icônes
- Clic change la veille affichée

### GRILLE DE CASES TYPE BD/COMICS
- 6 cases par veille (2 colonnes x 3 lignes)
- Chaque case contient :
  * Icône/Emoji en haut (adaptée au sujet)
  * Titre du sujet (court, 1-2 lignes max)
  * Bouton "Lire +" ou "Détails" en bas
- Cases de taille variable mais lisibles
- Style BD : bordures nettes, ombres portées légères, aspect "case de comics"
- Espacement entre les cases

### SECTION "POINTS CLÉS" EN BAS
- Après les 6 cases
- Titre "POINTS CLÉS À RETENIR"
- 3-5 points importants en bullet points
- Design sobre mais visible
- Extrait de la synthèse finale du markdown

### HAUTEUR TOTALE : environ 2 ÉCRANS
- Grille compacte mais lisible
- Tout visible avec 1-2 scrolls maximum
- Responsive

### MODAL/OVERLAY AU CLIC
- Clic sur "Lire +" ouvre un modal par-dessus
- Modal affiche le contenu complet du sujet
- Markdown parsé et bien formaté
- Bouton [X] ou [Fermer] en haut à droite
- Fond semi-transparent derrière
- Clic en dehors ferme le modal

## TEST DE CETTE SEMAINE : """ + test_actuel.upper() + """

Tu dois appliquer une variante créative de """ + test_actuel + """ :

- Layout : disposition asymétrique des cases, grille décalée, overlap léger
- Couleurs : palette comics (primaires, pop, vintage, noir et blanc)
- Typographie : polices comics, handwriting, bold pour titres
- Visualisation : style bulles BD, phylactères, effets tramés
- Animations : effet flip de case, zoom hover, shake subtil

## CONTRAINTES TECHNIQUES

- Fichier HTML autonome avec CSS inline et JavaScript vanilla
- Pas de bibliothèques externes sauf CDN pour polices si besoin
- Compatible Chrome, Firefox, Safari, Edge récents
- Responsive : desktop prioritaire

### Parsing du Markdown
- Parse le markdown côté client (JavaScript)
- Identifie les sections principales (## Titre)
- Crée 1 case par section majeure
- Limite à 6 cases les plus importantes
- Affiche tout le contenu dans le modal

## EXTRACTION DES DONNÉES

Pour chaque fichier markdown :
1. Identifier les 6 sections les plus importantes (titres ##)
2. Extraire le titre de chaque section
3. Choisir une icône/emoji pertinente selon le sujet
4. Extraire les 3-5 points clés de la "Synthèse finale"

## CONSIGNES DE STYLE

- Design moderne et impactant
- Inspiration comics américain (Marvel, DC, BD franco-belge)
- Couleurs vives et contrastées (sauf si test couleurs sombres)
- Typographie lisible et punchy
- Expérience fun et engageante

## RESPECTER LES PRÉFÉRENCES
- Intégrer : """ + j_aime + """
- NE JAMAIS utiliser : """ + rejete + """

## OUTPUT

Génère UNIQUEMENT le code HTML complet, de <!DOCTYPE html> à </html>

- Pas de commentaires avant/après
- Pas de balises markdown
- Code production-ready
- Tout fonctionne dès l'ouverture du fichier

GÉNÈRE LE SITE MAINTENANT.
"""
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8000,
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )
    
    html_content = message.content[0].text
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
    
    print("\n📂 Chargement des préférences...")
    preferences = charger_preferences()
    cycle = preferences['cycle']
    semaine = preferences['semaine_actuelle']
    test_actuel = cycle[(semaine - 1) % len(cycle)]
    print(f"   Semaine n°{semaine}")
    print(f"   Test de la semaine : {test_actuel.upper()}")
    
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
    
    print("\n🎨 Génération du site web...")
    print("   ⚠️  Cette opération peut prendre 1-2 minutes...")
    try:
        html = generer_site_web(fichiers, preferences)
        print(f"   ✓ Site généré ({len(html)} caractères)")
    except Exception as e:
        print(f"❌ ERREUR lors de la génération : {e}")
        return
    
    print("\n💾 Sauvegarde du site...")
    sauvegarder_site(html)
    
    print("\n📊 Mise à jour des préférences...")
    incrementer_semaine(preferences)
    
    print("\n" + "="*60)
    print("✅ Agent Générateur Web terminé avec succès!")
    print(f"🌐 Site disponible à : https://nliziard-ops.github.io/VeilleNLI/")
    print("="*60)

if __name__ == "__main__":
    main()
