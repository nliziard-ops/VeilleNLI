# 🤖 VeilleNLI

Système de veille automatisée quotidienne sur l'IA et l'actualité générale.

🌐 **Site** : https://nliziard-ops.github.io/VeilleNLI/

---

## 📋 Qu'est-ce que c'est ?

VeilleNLI génère **automatiquement tous les jours à 6h00** deux rapports de veille :

- **🤖 Veille IA** : Top 6 actualités IA/LLM (3 buzz + 3 tech)
- **📰 Veille Actualités** : Top 6 actualités générales (2 internationales + 2 nationales + 2 locales Bretagne)

---

## 🏗️ Architecture

**Pipeline 4 agents OpenAI GPT-5.2 :**

```
┌─────────────────────────┐     ┌─────────────────────────┐
│ Recherche IA v3         │────▶│ Synthèse IA v3          │
│ GPT-5.2 + web search    │     │ GPT-5.2 Pro             │
│ Collecte 25 articles    │     │ Sélection Top 6 + Autres│
└─────────────────────────┘     └─────────────────────────┘
                                              │
┌─────────────────────────┐     ┌─────────────────────────┐
│ Recherche News v3       │────▶│ Synthèse News v3        │
│ GPT-5.2 + web search    │     │ GPT-5.2 Pro             │
│ Collecte 25 articles    │     │ Sélection Top 6 + Autres│
└─────────────────────────┘     └─────────────────────────┘
              │                               │
              └───────────┬───────────────────┘
                          ▼
           ┌──────────────────────────┐
           │ Validation + Sync GitHub │
           │ data.json → GitHub Pages │
           └──────────────────────────┘
```

**Durée** : 4-6 minutes  
**Coût** : ~0.40€/jour (~12€/mois)  
**Exécution** : GitHub Actions

---

## 🚀 Utilisation

### Consulter les veilles

👉 https://nliziard-ops.github.io/VeilleNLI/

### Lancer manuellement

1. Aller sur [Actions](https://github.com/nliziard-ops/VeilleNLI/actions)
2. Sélectionner "🤖 Veille OpenAI v3"
3. Cliquer "Run workflow"

---

## 📁 Structure

```
VeilleNLI/
├── agents/                           # 6 agents Python
│   ├── agent_recherche_ia_v3.py      # Collecte IA (GPT-5.2)
│   ├── agent_synthese_ia_v3.py       # Analyse IA (GPT-5.2 Pro)
│   ├── agent_recherche_news_v3.py    # Collecte News (GPT-5.2)
│   ├── agent_synthese_news_v3.py     # Analyse News (GPT-5.2 Pro)
│   ├── agent_validateur_markdown.py  # Validation markdown
│   └── agent_generateur_json.py      # Génération data.json
│
├── .github/workflows/
│   └── veille-openai-v3.yml          # Pipeline automatisé
│
├── docs/                             # GitHub Pages
│   ├── index.html                    # Site React
│   ├── data.json                     # Données veille
│   └── markdown/                     # Markdowns source
│       ├── VeilleIA.md
│       └── VeilleNews.md
│
└── requirements.txt                  # Dépendances Python
```

---

## 🛠️ Stack Technique

- **Backend** : Python 3.11+
- **LLM** : OpenAI GPT-5.2 (recherche) + GPT-5.2 Pro (synthèse)
- **Web Search** : OpenAI Responses API avec `external_web_access`
- **Storage** : Google Drive (intermédiaire)
- **Frontend** : React 18 (single-page)
- **Hosting** : GitHub Pages
- **CI/CD** : GitHub Actions

---

## 🔐 Configuration

### Secrets GitHub requis

```
OPENAI_API_KEY              # Clé API OpenAI
GOOGLE_DRIVE_CREDENTIALS    # Service account JSON Google
GOOGLE_DRIVE_FOLDER_ID      # ID dossier stockage intermédiaire
```

### Installation locale

```bash
# Cloner
git clone https://github.com/nliziard-ops/VeilleNLI.git
cd VeilleNLI

# Installer dépendances
pip install -r requirements.txt

# Variables d'environnement
export OPENAI_API_KEY="sk-..."
export GOOGLE_DRIVE_CREDENTIALS='{"type":"service_account",...}'
export GOOGLE_DRIVE_FOLDER_ID="1xxx"

# Tester un agent
python agents/agent_recherche_ia_v3.py
```

---

## 💰 Coûts

| Agent | Modèle | Tokens moyens | Coût/jour |
|-------|--------|---------------|-----------|
| Recherche IA | GPT-5.2 | ~10k | 0.05€ |
| Synthèse IA | GPT-5.2 Pro | ~8k | 0.15€ |
| Recherche News | GPT-5.2 | ~21k | 0.10€ |
| Synthèse News | GPT-5.2 Pro | ~8k | 0.15€ |
| **TOTAL** | | **~47k** | **~0.45€** |

**Mensuel** : ~13.50€  
**Budget** : 40€/mois

---

## 📊 Monitoring

**Workflow** : [Actions](https://github.com/nliziard-ops/VeilleNLI/actions/workflows/veille-openai-v3.yml)  
**Planification** : Tous les jours à 6h00 (Europe/Paris)  
**Logs** : Disponibles dans GitHub Actions

---

## 🐛 Troubleshooting

### Recherche News retourne 0 articles

**Cause** : Blocage robot sur sources spécifiques  
**Solution** : Prompt utilise des requêtes web search génériques (pas d'accès direct aux sites)

### Synthèse News vide sur le site

**Cause** : Format markdown incompatible avec le parser  
**Solution** : Prompt strictement aligné sur format IA (séparateurs `---`)

### Erreur IndentationError

**Cause** : Modification manuelle du prompt avec mauvaise indentation  
**Solution** : Vérifier que `prompt = f"""` a 4 espaces d'indentation dans la fonction

---

## 📝 Documentation

- **README.md** (ce fichier) : Vue d'ensemble
- **ARCHITECTURE.md** : Détails techniques pipeline
- Code source : Documentation inline dans chaque agent

---

## 📄 Licence

Tous droits réservés - Nicolas Liziard ([@nliziard-ops](https://github.com/nliziard-ops))

---

*VeilleNLI v3 - Février 2026*
