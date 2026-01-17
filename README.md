# VeilleNLI

Système de veille automatisée sur l'Intelligence Artificielle et les actualités générales, propulsé par OpenAI GPT-4 Turbo.

## 🌐 Site web

**https://nliziard-ops.github.io/VeilleNLI/**

---

## 📋 Description

VeilleNLI génère quotidiennement deux veilles hebdomadaires :

- **Veille IA & LLM** : Actualités sur l'intelligence artificielle, modèles de langage, recherche, régulation
- **Veille Actualités** : Politique française, économie, international, écologie, Nantes & région Ouest

### Architecture OpenAI

Le système utilise un **workflow unique** qui exécute séquentiellement :

1. **Agent Veille IA** (GPT-4 Turbo) : Recherche web via Tavily, analyse, génération Markdown
2. **Agent Veille News** (GPT-4 Turbo) : Recherche web, analyse, génération Markdown
3. **Générateur JSON** : Parse les Markdown et génère `data.json`
4. **Commit automatique** : Push des fichiers sur GitHub

---

## ✨ Fonctionnalités

### Génération de contenu

- ✅ **6 sujets principaux** traités en profondeur :
  - Résumé (3-5 lignes)
  - Points de vue croisés (3+ sources)
  - Analyse & implications
  - Signaux faibles (veille IA uniquement)
  - Sources complètes

- ✅ **Autres sujets** en format condensé :
  - Thème
  - Résumé court (2-3 lignes)
  - Source unique

### Frontend web

- ✅ Design sobre et élégant (Crimson Text + IBM Plex Sans)
- ✅ Navigation IA / Actualités
- ✅ Cards avec bouton **"Lire +"** pour dérouler le détail
- ✅ Section **"Autres sujets"** en bas de page
- ✅ Responsive design
- ✅ Parser Markdown avancé
- ✅ Chargement dynamique depuis `data.json`

---

## 🚀 Utilisation

### Consulter les veilles

👉 **https://nliziard-ops.github.io/VeilleNLI/**

### Relancer manuellement

1. **Workflow complet (IA + News)** :  
   https://github.com/nliziard-ops/VeilleNLI/actions/workflows/veille-quotidienne.yml  
   → Cliquer "Run workflow"

2. **Le workflow exécute automatiquement** :
   - Collecte des données (IA puis News)
   - Upload sur Google Drive
   - Génération data.json
   - Commit sur GitHub
   - Le site se met à jour automatiquement

---

## 📊 Coûts

**Migration complète vers OpenAI** (GPT-4 Turbo)

| Composant | Coût/jour |
|-----------|-----------|
| Agent Veille IA | $0.09 |
| Agent Veille News | $0.09 |
| **TOTAL** | **$0.18** (~0.16€) |

**Par mois** : ~4.80€  
**Autonomie avec 25€** : ~5 mois (jusqu'à fin mars + bonus)

### Optimisations appliquées

- ✅ Modèle unique : GPT-4 Turbo (meilleur rapport qualité/prix)
- ✅ Limitation des tokens : 8000 (IA) / 5000 (News)
- ✅ Limitation des recherches : 8-10 par agent
- ✅ Exécution quotidienne unique
- ✅ Architecture sans agent intermédiaire

---

## 🏗️ Architecture technique

```
┌─────────────────────────────────────────────────────┐
│          Workflow Unique (6h Paris)                 │
│                                                     │
│  ┌──────────────────────────────────────────┐     │
│  │  1. Agent Veille IA (GPT-4 Turbo)        │     │
│  │     Tavily → Analyse → Markdown          │     │
│  └────────────────┬─────────────────────────┘     │
│                   ↓                                │
│  ┌──────────────────────────────────────────┐     │
│  │  2. Agent Veille News (GPT-4 Turbo)      │     │
│  │     Tavily → Analyse → Markdown          │     │
│  └────────────────┬─────────────────────────┘     │
│                   ↓                                │
│  ┌──────────────────────────────────────────┐     │
│  │  3. Upload Google Drive                  │     │
│  │     VeilleIA.md + VeilleNews.md          │     │
│  └────────────────┬─────────────────────────┘     │
│                   ↓                                │
│  ┌──────────────────────────────────────────┐     │
│  │  4. Générateur JSON                      │     │
│  │     Parse MD → data.json                 │     │
│  └────────────────┬─────────────────────────┘     │
│                   ↓                                │
│  ┌──────────────────────────────────────────┐     │
│  │  5. Commit GitHub                        │     │
│  │     docs/markdown/*.md + data.json       │     │
│  └──────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────┘
                     ↓
      ┌──────────────────────────────┐
      │   Frontend React             │
      │   GitHub Pages               │
      │   Fetch data.json            │
      └──────────────────────────────┘
```

---

## 📁 Structure du projet

```
VeilleNLI/
├── agents/
│   ├── agent_veille_ia.py          # Agent IA (GPT-4 Turbo)
│   ├── agent_veille_news.py        # Agent News (GPT-4 Turbo)
│   └── agent_generateur_json.py    # Générateur data.json
│
├── .github/workflows/
│   └── veille-quotidienne.yml      # Workflow unique automatique
│
├── docs/
│   ├── index.html                  # Frontend React
│   ├── data.json                   # Données structurées
│   └── markdown/
│       ├── VeilleIA.md             # Markdown IA
│       └── VeilleNews.md           # Markdown News
│
├── config/
│   └── prompts_openai.py           # Prompts système OpenAI
│
├── README.md                       # Ce fichier
└── MIGRATION_COMPLETE.md           # Historique migration
```

---

## 🛠️ Technologies

- **Backend** : Python 3.11+
- **LLM** : OpenAI GPT-4 Turbo (`gpt-4-turbo-2024-04-09`)
- **Web Search** : Tavily API (optimisé)
- **Storage** : Google Drive API
- **Frontend** : React 18, Babel, Marked.js
- **Hosting** : GitHub Pages
- **CI/CD** : GitHub Actions

---

## 🔐 Secrets GitHub requis

```
OPENAI_API_KEY              # Clé API OpenAI
TAVILY_API_KEY              # Clé API Tavily
GOOGLE_DRIVE_CREDENTIALS    # JSON service account Google Drive
GOOGLE_DRIVE_FOLDER_ID      # ID du dossier Google Drive
```

**Note** : `ANTHROPIC_API_KEY` a été supprimé (migration terminée)

---

## 🎯 Profil du lecteur

Cadre supérieur, ingénieur, basé à Nantes. Centres d'intérêt :

- **IA/LLM** : Modèles de langage, recherche, open source, régulation, cybersécurité
- **Actualités** : Politique française, économie, international, écologie, Nantes & Ouest, Bretagne

---

## 📅 Exécution

- **Fréquence** : Quotidienne à 6h00 (Paris)
- **Format** : Hebdomadaire (cumul de la semaine)
- **Mise à jour** : Automatique (workflow → GitHub → GitHub Pages)

---

## 📊 Monitoring

### GitHub Actions

- **Workflow** : "Veille Quotidienne (IA + News)"
- **Logs** : Disponibles dans Actions → Dernier run
- **Durée** : ~3-5 minutes

### Métriques clés

- ✅ Taille de `data.json` : ~20-50 KB
- ✅ Nombre de sujets IA : 6 principaux + 5-10 autres
- ✅ Nombre de sujets News : 6 principaux + 5-10 autres
- ✅ Coût quotidien : ~$0.18
- ✅ Temps d'exécution : 3-5 min

---

## 🔧 Maintenance

### Tests locaux

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Tester l'agent IA
export OPENAI_API_KEY="sk-..."
export TAVILY_API_KEY="tvly-..."
python agents/agent_veille_ia.py

# 3. Tester le générateur JSON
export GOOGLE_DRIVE_CREDENTIALS='{"type":"service_account",...}'
export GOOGLE_DRIVE_FOLDER_ID="1xxx"
python agents/agent_generateur_json.py

# 4. Vérifier data.json
cat docs/data.json | python -m json.tool

# 5. Servir le site localement
cd docs
python -m http.server 8000
# Ouvrir http://localhost:8000
```

### Dépannage

**Workflow échoue** :
- Vérifier les secrets GitHub (Settings → Secrets)
- Consulter les logs du workflow
- Vérifier les quotas Tavily/OpenAI

**Site n'affiche rien** :
- Ouvrir la console (F12)
- Vérifier que `data.json` est accessible
- Vérifier le format JSON (validateur en ligne)

**Données manquantes** :
- Vérifier les fichiers Markdown sur Google Drive
- Relancer le workflow manuellement
- Consulter les logs du générateur JSON

---

## 📖 Documentation

- **MIGRATION_COMPLETE.md** : Historique de la migration Anthropic → OpenAI
- **config/prompts_openai.py** : Prompts système des agents

---

## 🎉 Migration terminée

**✅ Statut** : Production stable (janvier 2026)  
**✅ Budget** : Optimisé (~0.16€/jour)  
**✅ Architecture** : Workflow unique simplifié  
**✅ Qualité** : Maintenue (GPT-4 Turbo)

---

## 🤝 Contribution

Projet personnel de Nicolas Liziard.

---

## 📄 Licence

Tous droits réservés.

---

## 📞 Contact

GitHub : [@nliziard-ops](https://github.com/nliziard-ops)

---

*Dernière mise à jour : 17 janvier 2026*
