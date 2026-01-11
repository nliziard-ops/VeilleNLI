# VeilleNLI

Système de veille automatisée sur l'Intelligence Artificielle et les actualités générales, propulsé par OpenAI GPT-4o.

## 🌐 Site web

**https://nliziard-ops.github.io/VeilleNLI/**

---

## 📋 Description

VeilleNLI génère quotidiennement deux veilles hebdomadaires :

- **Veille IA & LLM** : Actualités sur l'intelligence artificielle, modèles de langage, recherche, régulation
- **Veille Actualités** : Politique française, économie, international, écologie, Nantes & région Ouest

### Architecture 2-agents

Chaque veille utilise 2 agents OpenAI :

1. **Agent Collecteur (GPT-4o-mini)** : Recherche web via Tavily, filtrage, classification
2. **Agent Synthèse (GPT-4o)** : Génération Markdown avec structure 6 sujets détaillés + autres sujets

---

## ✨ Fonctionnalités

### Agents de synthèse

- ✅ **6 sujets principaux** traités en profondeur :
  - Résumé (5 lignes)
  - Points de vue croisés (3 sources)
  - Analyse & implications
  - Signaux faibles (IA seulement)
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

---

## 🚀 Utilisation

### Consulter les veilles

👉 **https://nliziard-ops.github.io/VeilleNLI/**

### Relancer les agents manuellement

1. **Veille IA** :  
   https://github.com/nliziard-ops/VeilleNLI/actions/workflows/veille-ia-openai.yml  
   → Cliquer "Run workflow"

2. **Veille News** :  
   https://github.com/nliziard-ops/VeilleNLI/actions/workflows/veille-news-openai.yml  
   → Cliquer "Run workflow"

3. **Mettre à jour le site** :
   - Télécharger `VeilleIA.md` et `VeilleNews.md` depuis Google Drive
   - Les uploader dans `docs/markdown/` sur GitHub
   - Le site se met à jour automatiquement

---

## 📊 Coûts

| Veille | Coût/jour |
|--------|-----------|
| Veille IA | $0.066 |
| Veille News | $0.046 |
| **TOTAL** | **$0.112** (~0.10€) |

**Par mois** : ~3€  
**Autonomie avec 25€** : 8 mois

---

## 🏗️ Architecture technique

```
┌──────────────────────────┐
│   Agent 1 (GPT-4o-mini)  │
│   Tavily → Filtrage      │
└────────────┬─────────────┘
             │ JSON
             ↓
┌──────────────────────────┐
│   Agent 2 (GPT-4o)       │
│   Top 6 + Autres         │
│   → Markdown             │
└────────────┬─────────────┘
             │
             ↓
      Google Drive
             │
             ↓ (copie manuelle)
             │
      docs/markdown/
             │
             ↓
┌──────────────────────────┐
│   Frontend React         │
│   GitHub Pages           │
└──────────────────────────┘
```

---

## 📁 Structure du projet

```
VeilleNLI/
├── agents/
│   ├── agent_collecteur_ia.py      # Collecte IA (GPT-4o-mini)
│   ├── agent_synthese_ia.py        # Synthèse IA (GPT-4o)
│   ├── agent_collecteur_news.py    # Collecte News (GPT-4o-mini)
│   └── agent_synthese_news.py      # Synthèse News (GPT-4o)
│
├── .github/workflows/
│   ├── veille-ia-openai.yml        # Workflow quotidien IA
│   └── veille-news-openai.yml      # Workflow quotidien News
│
├── docs/
│   ├── index.html                  # Frontend React
│   ├── markdown/
│   │   ├── VeilleIA.md             # Markdown IA
│   │   └── VeilleNews.md           # Markdown News
│   └── SYSTEM_COMPLETE.md          # Documentation complète
│
└── README.md                        # Ce fichier
```

---

## 🛠️ Technologies

- **Backend** : Python 3.11+
- **LLM** : OpenAI GPT-4o + GPT-4o-mini
- **Web Search** : Tavily API
- **Storage** : Google Drive API
- **Frontend** : React 18, Babel, Marked.js
- **Hosting** : GitHub Pages
- **CI/CD** : GitHub Actions

---

## 📖 Documentation

- **[SYSTEM_COMPLETE.md](docs/SYSTEM_COMPLETE.md)** : Documentation technique complète
- **[PHASE3_COMPLETE.md](docs/PHASE3_COMPLETE.md)** : Phase 3 (Agents News)
- **[AGENTS_OPENAI.md](docs/AGENTS_OPENAI.md)** : Architecture agents OpenAI

---

## 🔐 Secrets GitHub requis

```
OPENAI_API_KEY              # Clé API OpenAI
TAVILY_API_KEY              # Clé API Tavily
GOOGLE_DRIVE_CREDENTIALS    # JSON service account Google Drive
GOOGLE_DRIVE_FOLDER_ID      # ID du dossier Google Drive
```

---

## 🎯 Profil du lecteur

Cadre supérieur, ingénieur, basé à Nantes. Centres d'intérêt :

- **IA/LLM** : Modèles de langage, recherche, open source, régulation, cybersécurité
- **Actualités** : Politique française, économie, international, écologie, Nantes & Ouest, Bretagne

---

## 📅 Exécution

- **Fréquence** : Quotidienne à 6h (Paris)
- **Format** : Hebdomadaire (cumul de la semaine)
- **Mise à jour** : Manuelle (copie Markdown → GitHub)

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

*Dernière mise à jour : 11 janvier 2026*
