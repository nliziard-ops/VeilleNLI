# VeilleNLI

Système de veille automatisée sur l'Intelligence Artificielle et les actualités générales, propulsé par **OpenAI Deep Research (o1)**.

## 🌐 Site web

**https://nliziard-ops.github.io/VeilleNLI/**

---

## 📋 Description

VeilleNLI génère quotidiennement deux veilles hebdomadaires via **Deep Research** :

- **Veille IA & LLM** : Actualités IA, modèles de langage, recherche, régulation, startups (focus Nantes/Bretagne)
- **Veille Actualités** : Politique, économie, international, sport maritime (voile, surf, kitesurf, wingfoil), local (Bretagne, Nantes, Belle-Île)

### Architecture Deep Research (OpenAI o1)

Le système utilise un **workflow unique** avec **6 jobs séquentiels** :

1. **Deep Research IA** (OpenAI o1) : Recherche approfondie IA/LLM → `research_ia.md`
2. **Deep Research News** (OpenAI o1) : Recherche approfondie actualités → `research_news.md`
3. **Formatter** (GPT-4o-mini) : Mise en forme élégante → Upload Google Drive
4. **Sync Markdown** : Télécharge depuis Google Drive → `docs/markdown/`
5. **Générateur JSON** : Parse Markdown → `data.json`
6. **Commit GitHub** : Push sur main → GitHub Pages

---

## ✨ Fonctionnalités

### Deep Research

- ✅ **Recherche approfondie** avec OpenAI Extended Thinking (o1)
- ✅ **Sources officielles prioritaires** : OpenAI Blog, Anthropic Blog, Mistral AI, ArXiv
- ✅ **Couverture géographique** : USA, Europe, Asie, France, Nantes, Bretagne
- ✅ **Sport maritime** : Voile, course au large, surf, planche à voile, kitesurf, wingfoil
- ✅ **Local Bretagne** : Actualités Bretagne, Pays de la Loire, Nantes, Belle-Île-en-Mer

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

1. **Workflow complet (Deep Research)** :  
   https://github.com/nliziard-ops/VeilleNLI/actions/workflows/deep-research-daily.yml  
   → Cliquer "Run workflow"

2. **Le workflow exécute automatiquement** :
   - Recherches Deep approfondies (IA + News en parallèle)
   - Mise en forme et upload Google Drive
   - Sync Markdown vers GitHub
   - Génération data.json
   - Commit sur GitHub
   - Le site se met à jour automatiquement

**Durée totale** : ~8-12 minutes

---

## 📊 Coûts

**Architecture Deep Research (OpenAI o1 + GPT-4o-mini)**

| Composant | Modèle | Coût/jour |
|-----------|--------|-----------|
| Deep Research IA | o1-2024-12-17 | ~0.25€ |
| Deep Research News | o1-2024-12-17 | ~0.25€ |
| Formatter IA | GPT-4o-mini | ~0.005€ |
| Formatter News | GPT-4o-mini | ~0.005€ |
| **TOTAL** | - | **~0.51€** |

**Par mois** : ~15.30€  
**Budget jusqu'à fin mars (65 jours)** : ~33€

### Optimisations appliquées

- ✅ Deep Research : 2 recherches approfondies au lieu de 28 requêtes Tavily
- ✅ Formatter économique : GPT-4o-mini au lieu de GPT-4
- ✅ Exécution parallèle des recherches (gain de temps)
- ✅ Timeout adapté : 15 minutes par recherche
- ✅ Artifacts inter-jobs pour réduire les coûts de stockage

### Amélioration vs ancien système (Tavily)

| Critère | Ancien (Tavily) | Nouveau (Deep Research) |
|---------|-----------------|-------------------------|
| **Qualité** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Fraîcheur** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Couverture** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Sport maritime** | ❌ | ✅ |
| **Local Bretagne** | ❌ | ✅ |
| **IA Nantes** | ❌ | ✅ |
| **Coût/jour** | ~0.18€ | ~0.51€ |

---

## 🏗️ Architecture technique

```
┌──────────────────────────────────────────────────────────────┐
│          Workflow Deep Research (6h Paris)                   │
│                                                              │
│  ┌─────────────────────┐    ┌─────────────────────┐        │
│  │ 1. Deep Research IA │    │ 2. Deep Research    │        │
│  │    (o1, parallèle)  │    │    News (o1)        │        │
│  │                     │    │    (parallèle)      │        │
│  │ → research_ia.md    │    │ → research_news.md  │        │
│  └──────────┬──────────┘    └──────────┬──────────┘        │
│             └────────────┬──────────────┘                   │
│                          ↓                                   │
│             ┌────────────────────────────┐                  │
│             │ 3. Formatter               │                  │
│             │    (GPT-4o-mini)           │                  │
│             │                            │                  │
│             │ Lit les 2 research         │                  │
│             │ Structure élégante         │                  │
│             │                            │                  │
│             │ → VeilleIA.md              │                  │
│             │ → VeilleNews.md            │                  │
│             │ Upload Google Drive        │                  │
│             └────────────┬───────────────┘                  │
│                          ↓                                   │
│             ┌────────────────────────────┐                  │
│             │ 4. Sync Markdown           │                  │
│             │                            │                  │
│             │ Download Google Drive      │                  │
│             │ → docs/markdown/*.md       │                  │
│             │ Commit GitHub              │                  │
│             └────────────┬───────────────┘                  │
│                          ↓                                   │
│             ┌────────────────────────────┐                  │
│             │ 5. Générateur JSON         │                  │
│             │                            │                  │
│             │ Parse Markdown             │                  │
│             │ → docs/data.json           │                  │
│             │ Commit GitHub              │                  │
│             └────────────┬───────────────┘                  │
│                          ↓                                   │
│             ┌────────────────────────────┐                  │
│             │ 6. Résumé final            │                  │
│             │                            │                  │
│             │ Statistiques               │                  │
│             │ Pipeline OK                │                  │
│             └────────────────────────────┘                  │
└──────────────────────────────────────────────────────────────┘
                          ↓
         ┌────────────────────────────┐
         │   Frontend React           │
         │   GitHub Pages             │
         │   Fetch data.json          │
         └────────────────────────────┘
```

---

## 📁 Structure du projet

```
VeilleNLI/
├── agents/
│   ├── deep_research_ia.py         # Deep Research IA (o1)
│   ├── deep_research_news.py       # Deep Research News (o1)
│   ├── agent_formatter.py          # Formatter (GPT-4o-mini)
│   ├── agent_generateur_json.py    # Générateur data.json
│   │
│   ├── agent_collecteur_ia.py      # [INACTIF] Ancien système Tavily
│   ├── agent_collecteur_news.py    # [INACTIF] Ancien système
│   ├── agent_synthese_ia.py        # [INACTIF] Ancien système
│   └── agent_synthese_news.py      # [INACTIF] Ancien système
│
├── .github/workflows/
│   ├── deep-research-daily.yml     # [ACTIF] Workflow Deep Research
│   └── veille-quotidienne.yml      # [DÉSACTIVÉ] Ancien workflow Tavily
│
├── docs/
│   ├── index.html                  # Frontend React
│   ├── data.json                   # Données structurées
│   └── markdown/
│       ├── VeilleIA.md             # Markdown IA
│       └── VeilleNews.md           # Markdown News
│
├── README.md                       # Ce fichier
├── DEEP_RESEARCH_MIGRATION.md      # Documentation migration Deep Research
└── requirements.txt                # Dépendances Python
```

---

## 🛠️ Technologies

- **Backend** : Python 3.11+
- **LLM Deep Research** : OpenAI o1 (`o1-2024-12-17`)
- **LLM Formatter** : OpenAI GPT-4o-mini (`gpt-4o-mini-2024-07-18`)
- **Storage** : Google Drive API
- **Frontend** : React 18, Babel, Marked.js
- **Hosting** : GitHub Pages
- **CI/CD** : GitHub Actions

---

## 🔐 Secrets GitHub requis

```
OPENAI_API_KEY              # Clé API OpenAI (o1 + GPT-4o-mini)
GOOGLE_DRIVE_CREDENTIALS    # JSON service account Google Drive
GOOGLE_DRIVE_FOLDER_ID      # ID du dossier Google Drive
```

**Note** : `TAVILY_API_KEY` et `ANTHROPIC_API_KEY` ne sont plus utilisés

---

## 🎯 Profil du lecteur

Cadre supérieur, ingénieur, basé à Nantes. Centres d'intérêt :

- **IA/LLM** : Modèles de langage, recherche, open source, régulation, startups Nantes/Bretagne
- **Actualités** : Politique, économie, international, écologie, sport maritime (voile, surf, kitesurf)
- **Local** : Nantes, Bretagne, Pays de la Loire, Belle-Île-en-Mer

---

## 📅 Exécution

- **Fréquence** : Quotidienne à 6h00 (Paris)
- **Format** : Hebdomadaire (cumul de la semaine)
- **Mise à jour** : Automatique (workflow → GitHub → GitHub Pages)
- **Durée** : ~8-12 minutes par exécution

---

## 📊 Monitoring

### GitHub Actions

- **Workflow actif** : "Deep Research Quotidien"
- **Logs** : Disponibles dans Actions → Dernier run
- **Jobs** : 6 jobs séquentiels (2 parallèles au début)

### Métriques clés

- ✅ Taille de `data.json` : ~20-50 KB
- ✅ Nombre de sujets IA : 6 principaux + 15-20 autres
- ✅ Nombre de sujets News : 6 principaux + 15-20 autres
- ✅ Coût quotidien : ~0.51€
- ✅ Temps d'exécution : 8-12 min

---

## 🔧 Maintenance

### Tests locaux

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Tester Deep Research IA
export OPENAI_API_KEY="sk-..."
python agents/deep_research_ia.py

# 3. Tester Deep Research News
python agents/deep_research_news.py

# 4. Tester le Formatter (nécessite research*.md)
export GOOGLE_DRIVE_CREDENTIALS='{"type":"service_account",...}'
export GOOGLE_DRIVE_FOLDER_ID="1xxx"
python agents/agent_formatter.py

# 5. Tester le générateur JSON
python agents/agent_generateur_json.py

# 6. Vérifier data.json
cat docs/data.json | python -m json.tool

# 7. Servir le site localement
cd docs
python -m http.server 8000
# Ouvrir http://localhost:8000
```

### Dépannage

**Workflow échoue** :
- Vérifier les secrets GitHub (Settings → Secrets)
- Consulter les logs du workflow (chaque job a ses logs)
- Vérifier les quotas OpenAI
- Timeout Deep Research : augmenter à 20 min si nécessaire

**Site n'affiche rien** :
- Ouvrir la console (F12)
- Vérifier que `data.json` est accessible
- Vérifier le format JSON (validateur en ligne)

**Données manquantes** :
- Vérifier les fichiers Markdown sur Google Drive
- Relancer le workflow manuellement
- Consulter les logs du générateur JSON (Job 5)

**Deep Research timeout** :
- Les recherches o1 peuvent prendre 2-5 minutes
- Timeout actuel : 15 minutes (confortable)
- Si timeout fréquent : augmenter à 20 min dans le workflow

---

## 📖 Documentation

- **DEEP_RESEARCH_MIGRATION.md** : Documentation migration vers Deep Research
- **MIGRATION_COMPLETE.md** : Historique migration Anthropic → OpenAI

---

## 🎉 Migration Deep Research terminée

**✅ Statut** : Production stable (janvier 2026)  
**✅ Architecture** : Deep Research (o1) + Formatter (GPT-4o-mini)  
**✅ Qualité** : Excellente (recherche approfondie)  
**✅ Couverture** : Sport maritime + Local Bretagne + IA Nantes  
**✅ Budget** : ~0.51€/jour (~33€ jusqu'à fin mars)

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

*Dernière mise à jour : 25 janvier 2026 - Migration Deep Research*
