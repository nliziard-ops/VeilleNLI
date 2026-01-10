# 🔍 VeilleNLI

**Système automatisé de veille hebdomadaire intelligente**

Un système de veille automatisée basé sur Claude AI qui génère chaque semaine des synthèses d'actualités personnalisées sur l'IA et l'actualité générale, puis produit un site web au style comics pour les consulter.

---

## 📋 Vue d'ensemble

VeilleNLI est un système orchestré par GitHub Actions qui exécute automatiquement trois agents spécialisés :

1. **Agent Veille IA** : Synthétise les actualités IA/LLM de la semaine
2. **Agent Veille Actualités** : Synthétise l'actualité générale hebdomadaire
3. **Agent Générateur Web V2** : Crée un site web interactif à double onglets pour visualiser les synthèses

### 🎯 Objectifs

- Automatiser la collecte et l'analyse d'actualités
- Croiser minimum 3 sources fiables par sujet
- Fournir des analyses neutres avec différents points de vue
- Présenter l'information de manière engageante et moderne
- Hiérarchiser les sujets par importance (6 sujets majeurs + sujets secondaires)

---

## 🏗️ Architecture

```
VeilleNLI/
├── .github/
│   └── workflows/
│       ├── agents-collecteurs.yml    # Exécution des agents de veille
│       └── agent-generateur.yml      # Génération du site web
├── agents/
│   ├── agent_veille_ia.py           # Agent de veille IA/LLM
│   ├── agent_veille_news.py         # Agent de veille actualités
│   └── agent_generateur_web.py      # Générateur de site web V2
├── config/
│   └── styles_preferences.json      # Préférences de style visuel
├── docs/
│   └── index.html                   # Site web généré (GitHub Pages)
└── requirements.txt
```

---

## 🤖 Les Agents

### 1. Agent Veille IA (`agent_veille_ia.py`)

**Mission** : Synthétiser l'actualité IA et LLM de la semaine écoulée.

**Fonctionnement** :
- Utilise Claude Sonnet 4 avec l'outil `web_search`
- Recherche sur 9 catégories : nouveaux modèles, open source, recherche scientifique, régulation, industrie, cybersécurité, applications, hardware, actualités locales (Nantes/Ouest)
- Croise minimum 3 sources par sujet
- Identifie 10-15 sujets majeurs
- Met en avant les divergences d'analyse entre sources
- Génère un fichier Markdown structuré

**Profil du lecteur** :
- Cadre supérieur ingénieur basé à Nantes
- Intéressé par : LLM, IA générative, open source, cloud, économie du secteur, recherche, régulation européenne, cybersécurité, applications entreprises

**Sortie** : `VeilleIA.md` uploadé sur Google Drive

---

### 2. Agent Veille Actualités (`agent_veille_news.py`)

**Mission** : Synthétiser l'actualité générale hebdomadaire.

**Fonctionnement** :
- Utilise Claude Sonnet 4 avec l'outil `web_search`
- Couvre 5-6 catégories prioritaires : politique française, économie & entreprises, international & Europe, écologie & transition, Nantes & région Ouest
- Maximum 2 sujets par catégorie
- S'appuie sur des médias sérieux (Les Échos, Le Monde, Ouest-France, Financial Times, etc.)
- Présente les différences d'interprétation entre médias
- Reste strictement neutre et analytique

**Catégories locales spéciales** :
- Nantes et Pays de la Loire
- Bretagne (Belle-Île-en-Mer, L'Hôpital-Camfrout, Landerneau, Brest)

**Sortie** : `VeilleNews.md` uploadé sur Google Drive

---

### 3. Agent Générateur Web V2 (`agent_generateur_web.py`)

**Mission** : Créer un site web interactif au style comics/BD pour visualiser les veilles.

**🆕 Nouveautés V2** :

#### **Parsing Intelligent du Markdown**
- Extraction automatique des sections principales (##)
- Exclusion des sections meta (Introduction, Table des matières, Synthèse finale)
- Séparation automatique : **6 sujets importants** (premiers) + **sujets secondaires** (suivants)
- Extraction des points clés de la synthèse finale

#### **Résumés Tronqués**
- Résumés des sujets importants **tronqués à 40 mots** avec "..."
- Clic sur le résumé → expand pour afficher le texte complet
- Résumés des sujets secondaires affichés en entier

#### **Double Onglets**
- **1 page HTML unique** avec 2 sections masquables
- **Navigation JavaScript** fluide entre "Veille IA" et "Actualités"
- Menu latéral (30-40px) avec 2 boutons verticaux

#### **Système de Vérification Robuste**
- **3 tentatives maximum** de génération
- Vérifications automatiques :
  - Validité HTML (balises fermées, structure correcte)
  - Présence de tous les sujets (IA + Actualités)
  - Éléments essentiels (menu, sections, modals, JavaScript)
  - Liens et sources présents
- Régénération automatique en cas d'échec
- Logs détaillés des vérifications

**Design du site** :

#### **Sujets Importants (6 cartes comics par onglet)**
- Grille de 6 cartes style BD (2x3 ou 3x2)
- Chaque carte contient :
  - Icône/emoji pertinente
  - Titre du sujet (1-2 lignes)
  - Résumé tronqué à 40 mots (cliquable pour expand)
  - Bouton "Lire +" → ouvre modal avec détail complet
- Style BD : bordures nettes, ombres portées, couleurs vives

#### **Sujets Secondaires (liste compacte)**
- Titre : "Autres sujets de la semaine"
- Liste avec :
  - Titre en gras
  - Résumé complet
  - Clic sur titre → ouvre modal

#### **Section Points Clés**
- 3-5 points importants de la synthèse
- Design sobre mais visible

#### **Modals Fonctionnels**
- Overlay semi-transparent
- Contenu complet du sujet :
  1. Titre
  2. Résumé complet
  3. Points de vue croisés
  4. Fiabilité & signaux faibles
  5. Sources avec liens cliquables
- Bouton [X] fermeture
- Clic en dehors → ferme le modal

**Sortie** : `docs/index.html` pour GitHub Pages

---

## ⚙️ Workflows GitHub Actions

### Workflow "Agents Collecteurs" (`agents-collecteurs.yml`)

**Déclenchement** : Chaque samedi à 6h30 heure française (5h30 UTC)

**Séquence d'exécution** :
1. Agent Veille IA (job `run-agent-ia`)
2. Pause de 2 minutes (rate limit safety)
3. Agent Veille News (job `run-agent-news`)

**Configuration** :
- Python 3.11
- Ubuntu latest
- Dépendances : `anthropic`, `google-api-python-client`, `google-auth`

**Secrets requis** :
- `ANTHROPIC_API_KEY`
- `GOOGLE_DRIVE_CREDENTIALS`
- `GOOGLE_DRIVE_FOLDER_ID`

---

### Workflow "Agent Générateur Web" (`agent-generateur.yml`)

**Déclenchement** : Chaque samedi à 7h30 heure française (6h30 UTC)

**Séquence d'exécution** :
1. Téléchargement des fichiers Markdown depuis Google Drive
2. **Parsing intelligent** des fichiers Markdown
3. **Génération du site web HTML** (jusqu'à 3 tentatives)
4. **Vérification de l'intégrité** du HTML
5. Commit et push automatique du site vers `docs/index.html`
6. Mise à jour de `config/styles_preferences.json`

**Commit automatique** : 
```
🚀 Mise à jour automatique du site - YYYY-MM-DD
```

---

## 🔧 Configuration

### Prérequis

1. **API Anthropic** : Clé API Claude
2. **Google Drive API** : Credentials de service account
3. **GitHub Pages** : Activé sur le repository (branche `main`, dossier `/docs`)

### Secrets GitHub

Ajouter dans Settings > Secrets and variables > Actions :

```bash
ANTHROPIC_API_KEY=sk-ant-xxxxx
GOOGLE_DRIVE_CREDENTIALS={"type": "service_account", ...}
GOOGLE_DRIVE_FOLDER_ID=1aBcDeFgHiJkLmN
```

### Installation locale (optionnelle)

```bash
# Cloner le repository
git clone https://github.com/nliziard-ops/VeilleNLI.git
cd VeilleNLI

# Installer les dépendances
pip install -r requirements.txt

# Variables d'environnement
export ANTHROPIC_API_KEY="sk-ant-xxxxx"
export GOOGLE_DRIVE_CREDENTIALS='{"type": "service_account", ...}'
export GOOGLE_DRIVE_FOLDER_ID="1aBcDeFgHiJkLmN"

# Exécuter un agent
python agents/agent_veille_ia.py
python agents/agent_veille_news.py
python agents/agent_generateur_web.py
```

---

## 📊 Cycle de vie hebdomadaire

```mermaid
graph TD
    A[Samedi 6h30] --> B[Agent Veille IA]
    B --> C[Upload VeilleIA.md sur Drive]
    C --> D[Pause 2 min]
    D --> E[Agent Veille News]
    E --> F[Upload VeilleNews.md sur Drive]
    F --> G[Samedi 7h30]
    G --> H[Agent Générateur Web V2]
    H --> I[Parsing intelligent des MD]
    I --> J[Génération HTML - Tentative 1]
    J --> K{Vérification OK?}
    K -->|Non| L[Tentative 2]
    L --> M{Vérification OK?}
    M -->|Non| N[Tentative 3]
    N --> O{Vérification OK?}
    O -->|Oui ou Échec final| P[Commit & Push vers GitHub]
    K -->|Oui| P
    M -->|Oui| P
    P --> Q[GitHub Pages publie le site]
    Q --> R[Incrémente compteur de semaine]
```

---

## 🎨 Système de préférences visuelles

Le fichier `config/styles_preferences.json` gère l'évolution du design :

```json
{
  "semaine_actuelle": 10,
  "cycle": ["layout", "couleurs", "typographie", "visualisation", "animations"],
  "preferences": {
    "j_aime": [],
    "rejete": [],
    "pas_note": []
  }
}
```

**Cycle de tests** (rotation toutes les 5 semaines) :
1. **Layout** : disposition asymétrique, grille décalée, overlap
2. **Couleurs** : palettes comics (primaires, pop, vintage, noir et blanc)
3. **Typographie** : polices comics, handwriting, bold
4. **Visualisation** : bulles BD, phylactères, effets tramés
5. **Animations** : flip, zoom hover, shake subtil

⚠️ **Note V2** : Le système de préférences cycliques est actuellement désactivé. Focus sur la structure et la fonctionnalité.

---

## 📈 Statistiques

- **Fréquence** : Hebdomadaire (samedi)
- **Sujets par veille** : 10-15 (IA) / 8-10 (Actualités)
- **Hiérarchisation** : 6 sujets importants + sujets secondaires par onglet
- **Sources minimales par sujet** : 3
- **Temps de lecture** : 10-15 minutes par veille
- **Taille des synthèses** : ~8000 caractères (IA) / ~5000 caractères (Actualités)
- **Site web** : 1 page HTML, 2 onglets, 6 cartes + liste par onglet
- **Système de vérification** : 3 tentatives maximum

---

## 🌐 Accès au site

Le site est publié automatiquement via GitHub Pages :

**URL** : https://nliziard-ops.github.io/VeilleNLI/

---

## 📝 Format des synthèses Markdown

### Structure commune

```markdown
---
agent: [Veille IA | Veille Actualités]
date: YYYY-MM-DD
catégorie: [Intelligence Artificielle | Actualités Générales]
---

# Veille [Type] – Semaine du DD/MM/YYYY au DD/MM/YYYY
**Édition [Nom créatif]**

## Introduction
[3-4 lignes de contexte]

## Table des matières
[Liste des catégories]

## [CATÉGORIE] – [Titre]

### Résumé
[5 lignes max]

### Points de vue croisés
**Source 1** – [Analyse]
**Source 2** – [Divergences]
**Source 3** – [Compléments]

### Fiabilité & signaux faibles
[Points incertains]

### Sources
- [Source 1] – [URL]
- [Source 2] – [URL]
- [Source 3] – [URL]

---

## Synthèse finale

### Points clés de la semaine
[Liste]

### Divergences d'analyse notables
[Points de désaccord]

### À surveiller la semaine prochaine
[Sujets en développement]
```

---

## 🔒 Sécurité & Bonnes pratiques

- Credentials Google stockés en secret GitHub (jamais dans le code)
- API Key Anthropic en secret GitHub
- Pause de 2 minutes entre les agents pour respecter les rate limits
- Commit automatique avec user.email et user.name génériques
- Logs détaillés dans les workflows pour debug
- Système de vérification robuste (3 tentatives)

---

## 🚀 Déploiement

Le système est entièrement automatisé. Une fois les secrets configurés :

1. Les workflows s'exécutent automatiquement chaque samedi
2. Les fichiers Markdown sont créés et uploadés sur Google Drive
3. Le site web est généré avec vérifications (jusqu'à 3 tentatives)
4. Le site est publié sur GitHub Pages
5. Aucune intervention manuelle requise

**Exécution manuelle** : 
- Aller dans Actions > [Workflow] > Run workflow

---

## 📦 Dépendances

```
anthropic>=0.34.0
google-api-python-client>=2.100.0
google-auth>=2.23.0
```

---

## 🆕 Changelog V2

### Version 2.0 - Janvier 2026

**Nouvelles fonctionnalités** :
- ✅ Parsing intelligent du Markdown avec extraction automatique des sections
- ✅ Hiérarchisation des sujets (6 importants + secondaires)
- ✅ Résumés tronqués à 40 mots avec expand
- ✅ Double onglets (Veille IA / Actualités) avec navigation JavaScript
- ✅ Système de vérification robuste avec 3 tentatives de génération
- ✅ Validation HTML, présence des sujets, liens et éléments essentiels
- ✅ Modals fonctionnels pour afficher le détail des sujets
- ✅ Logs détaillés des vérifications

**Améliorations** :
- Structure HTML plus claire et sémantique
- Meilleure séparation des préoccupations (parsing, génération, vérification)
- Gestion d'erreurs améliorée avec retry automatique

---

## 🛠️ Évolutions futures possibles

- [ ] Réactivation du système de préférences visuelles cycliques
- [ ] Système de notation des styles (feedback utilisateur)
- [ ] Export PDF des synthèses
- [ ] Archivage automatique des anciennes semaines
- [ ] Dashboard avec statistiques d'évolution des sujets
- [ ] Intégration d'autres sources de veille (Twitter, Reddit, etc.)
- [ ] Notifications email lors de la publication
- [ ] Mode sombre/clair pour le site
- [ ] Recherche dans les archives
- [ ] Filtres par catégorie sur le site

---

## 📄 Licence

Projet personnel - Tous droits réservés

---

## 👤 Auteur

**Nicolas Liziard**  
Data Consultant chez CCR Consulting  
Nantes, France

---

## 🙏 Remerciements

- **Anthropic Claude** pour les capacités de recherche web et génération
- **GitHub Actions** pour l'orchestration automatisée
- **Google Drive API** pour le stockage des synthèses
- **GitHub Pages** pour l'hébergement du site

---

**Dernière mise à jour** : Janvier 2026  
**Version** : 2.0  
**Statut** : Production - Actif chaque samedi
