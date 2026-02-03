# 🤖 VeilleNLI

Système de veille automatisée quotidienne sur l'IA et l'actualité, propulsé par **OpenAI GPT-5.2**.

🌐 **Site** : https://nliziard-ops.github.io/VeilleNLI/

---

## 📋 Description

VeilleNLI génère **quotidiennement à 6h00 (Paris)** deux bulletins de veille :

- **🤖 Veille IA** : Actualités IA/LLM depuis sources institutionnelles
- **📰 Veille Actualités** : Presse internationale, nationale, locale (Bretagne)

### Architecture

**4 agents OpenAI en pipeline :**

```
Recherche IA v3 (GPT-5.2) → Synthèse IA v3 (GPT-5.2 Pro)
Recherche News v3 (GPT-5.2) → Synthèse News v3 (GPT-5.2 Pro)
           ↓
  Validation → Sync GitHub → data.json → Site Web
```

**Exécution :** GitHub Actions (quotidien, 6h00 Paris)  
**Durée :** ~4-6 minutes  
**Coût :** ~0.40€/jour (~12€/mois)

---

## 🚀 Utilisation

### Consulter les veilles

👉 https://nliziard-ops.github.io/VeilleNLI/

### Lancer manuellement

1. [Actions](https://github.com/nliziard-ops/VeilleNLI/actions/workflows/veille-openai-v3.yml)
2. **"Run workflow"**

---

## 📁 Structure

```
VeilleNLI/
├── .github/workflows/
│   ├── veille-openai-v3.yml          # Pipeline principal
│   └── cleanup-repo.yml              # Maintenance
│
├── agents/
│   ├── agent_recherche_ia_v3.py      # Collecte IA
│   ├── agent_synthese_ia_v3.py       # Analyse IA
│   ├── agent_recherche_news_v3.py    # Collecte News
│   ├── agent_synthese_news_v3.py     # Analyse News
│   ├── agent_validateur_markdown.py  # Validation
│   └── agent_generateur_json.py      # data.json
│
├── docs/                             # Site GitHub Pages
│   ├── index.html
│   ├── data.json
│   └── markdown/
│       ├── VeilleIA.md
│       └── VeilleNews.md
│
├── scripts/
│   ├── cleanup_repository.py         # Nettoyage
│   └── list_openai_models.py         # Utilitaire
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🛠️ Technologies

- **Backend** : Python 3.11+
- **LLM** : OpenAI GPT-5.2 / GPT-5.2 Pro
- **Storage** : Google Drive API
- **Frontend** : React 18
- **Hosting** : GitHub Pages
- **CI/CD** : GitHub Actions

---

## 🔐 Secrets GitHub

```
OPENAI_API_KEY              # API OpenAI
GOOGLE_DRIVE_CREDENTIALS    # Service account JSON
GOOGLE_DRIVE_FOLDER_ID      # ID dossier stockage
```

---

## 🧪 Tests Locaux

```bash
# Installation
pip install -r requirements.txt

# Variables d'environnement
export OPENAI_API_KEY="sk-..."
export GOOGLE_DRIVE_CREDENTIALS='{"type":"service_account",...}'
export GOOGLE_DRIVE_FOLDER_ID="1xxx"

# Test agents
python agents/agent_recherche_ia_v3.py
python agents/agent_synthese_ia_v3.py

# Validation JSON
cat docs/data.json | python -m json.tool

# Serveur local
cd docs && python -m http.server 8000
```

---

## 📊 Monitoring

**Workflow** : [Actions](https://github.com/nliziard-ops/VeilleNLI/actions/workflows/veille-openai-v3.yml)  
**Schedule** : Quotidien 6h00 Europe/Paris  
**Durée** : 4-6 minutes  
**Coût** : ~0.40€/jour

---

## 💰 Coûts

| Agent | Modèle | Tokens | Coût/jour |
|-------|--------|--------|-----------|
| Recherche IA | GPT-5.2 | 10k | ~0.05€ |
| Synthèse IA | GPT-5.2 Pro | 8k | ~0.15€ |
| Recherche News | GPT-5.2 | 10k | ~0.05€ |
| Synthèse News | GPT-5.2 Pro | 8k | ~0.15€ |
| **Total** | - | **36k** | **~0.40€** |

**Par mois** : ~12€  
**Budget disponible** : 40€/mois

---

## 🔧 Maintenance

### Nettoyage du repository

```bash
# Simulation
python scripts/cleanup_repository.py

# Exécution
python scripts/cleanup_repository.py --execute --yes
```

Ou via [workflow](https://github.com/nliziard-ops/VeilleNLI/actions/workflows/cleanup-repo.yml)

---

## 📝 Licence

Tous droits réservés - Nicolas Liziard ([@nliziard-ops](https://github.com/nliziard-ops))

---

*VeilleNLI - Architecture v3 - Février 2026*
