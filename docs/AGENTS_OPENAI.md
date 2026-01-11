# 🤖 Agents Veille IA - Architecture 2-agents OpenAI

## 📋 Vue d'ensemble

Système de veille automatisé optimisé pour minimiser les coûts OpenAI en utilisant une architecture à 2 agents :

- **Agent 1 (Collecteur)** : GPT-4o-mini - Recherche, filtrage, classification
- **Agent 2 (Synthétiseur)** : GPT-4o - Synthèse Markdown de haute qualité

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AGENT 1 - COLLECTEUR                     │
│                    (GPT-4o-mini - économique)               │
├─────────────────────────────────────────────────────────────┤
│ 1. Recherches Tavily (12-15 requêtes ciblées)              │
│    ├─ AI LLM news                                           │
│    ├─ OpenAI GPT updates                                    │
│    ├─ AI regulation Europe                                  │
│    └─ ... autres thèmes                                     │
│                                                              │
│ 2. Filtrage & Classification (GPT-4o-mini)                  │
│    ├─ Suppression doublons                                  │
│    ├─ Filtrage pertinence IA/LLM                            │
│    ├─ Classification thématique                             │
│    └─ Scoring de pertinence (1-10)                          │
│                                                              │
│ 3. Output : articles_filtres_ia.json                        │
│    ├─ 12-18 articles les plus pertinents                    │
│    ├─ Métadonnées structurées                               │
│    └─ Statistiques de filtrage                              │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   AGENT 2 - SYNTHÉTISEUR                    │
│                   (GPT-4o - qualité maximale)               │
├─────────────────────────────────────────────────────────────┤
│ 1. Lecture JSON pré-filtré                                  │
│    └─ Articles déjà triés et classifiés                     │
│                                                              │
│ 2. Génération Synthèse Markdown (GPT-4o)                    │
│    ├─ Analyse approfondie                                   │
│    ├─ Points de vue croisés                                 │
│    ├─ Signaux faibles                                       │
│    └─ Synthèse finale                                       │
│                                                              │
│ 3. Upload Google Drive                                      │
│    └─ VeilleIA.md (prêt pour le site web)                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 💰 Optimisation des coûts

### Comparaison de l'architecture

| Architecture | Coût estimé/jour | Détails |
|--------------|------------------|---------|
| **1 agent GPT-4o** (approche naïve) | ~0.25€ | GPT-4o fait tout (recherche + synthèse) |
| **2 agents optimisés** (actuel) | ~0.09€ | GPT-4o-mini filtre, GPT-4o synthétise |
| **Économie** | **64%** | 7.80€ vs 2.70€ par mois |

### Détail des coûts (estimation)

**Agent 1 - Collecteur (GPT-4o-mini)** : ~0.02€/jour
- Tavily : 12 recherches × 8 résultats = 96 articles bruts (gratuit, limite 1000/mois)
- GPT-4o-mini : ~2000 tokens input + 1500 tokens output
- Coût : $0.15/1M input, $0.60/1M output → ~$0.001/exécution

**Agent 2 - Synthèse (GPT-4o)** : ~0.07€/jour
- GPT-4o : ~1500 tokens input + 6000 tokens output
- Coût : $2.50/1M input, $10/1M output → ~$0.064/exécution

**Total : ~0.09€/jour = 2.70€/mois**

Budget : 25€ jusqu'à fin mars = **9 mois d'autonomie** ✅

---

## 🚀 Utilisation

### 1️⃣ Test local

```bash
# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
export OPENAI_API_KEY="sk-..."
export TAVILY_API_KEY="tvly-..."
export GOOGLE_DRIVE_CREDENTIALS='{"type":"service_account",...}'
export GOOGLE_DRIVE_FOLDER_ID="1abc..."

# Tester Agent 1 seul
python agents/agent_collecteur_ia.py

# Tester Agent 2 seul (après Agent 1)
python agents/agent_synthese_ia.py

# Tester les 2 agents en séquence
python test_agents_ia.py
```

### 2️⃣ Automatisation GitHub Actions

Le workflow `.github/workflows/veille-ia-openai.yml` lance automatiquement :
- **Quotidien** : 6h00 Paris (lundi-dimanche)
- **Manuel** : via l'onglet "Actions" sur GitHub

---

## 📁 Structure des fichiers

```
agents/
├── agent_collecteur_ia.py    # Agent 1 - GPT-4o-mini
├── agent_synthese_ia.py       # Agent 2 - GPT-4o
├── agent_veille_ia.py         # [ANCIEN] Anthropic Claude (à supprimer)
└── agent_veille_news.py       # [ANCIEN] Anthropic Claude (à supprimer)

.github/workflows/
├── veille-ia-openai.yml       # Nouveau workflow 2-agents
└── agents-collecteurs.yml     # [ANCIEN] Workflow Anthropic

test_agents_ia.py              # Script de test local
requirements.txt               # Dépendances Python
```

---

## 🔧 Configuration requise

### Secrets GitHub

Les secrets suivants doivent être configurés dans **Settings → Secrets and variables → Actions** :

| Secret | Description | Exemple |
|--------|-------------|---------|
| `OPENAI_API_KEY` | Clé API OpenAI | `sk-proj-...` |
| `TAVILY_API_KEY` | Clé API Tavily Search | `tvly-...` |
| `GOOGLE_DRIVE_CREDENTIALS` | Service account JSON | `{"type":"service_account",...}` |
| `GOOGLE_DRIVE_FOLDER_ID` | ID du dossier Google Drive | `1abc123...` |

### Dépendances Python

```
openai>=1.54.0                    # OpenAI API
requests>=2.31.0                  # Tavily HTTP requests
google-api-python-client>=2.100.0 # Google Drive API
google-auth>=2.23.0               # Google authentication
```

---

## 📊 Format de sortie

### JSON intermédiaire (Agent 1 → Agent 2)

```json
{
  "date_collecte": "2026-01-11",
  "periode": {
    "debut": "2026-01-04",
    "fin": "2026-01-11"
  },
  "articles": [
    {
      "id": "a1b2c3d4e5f6",
      "titre": "OpenAI announces GPT-5 with reasoning capabilities",
      "source": "TechCrunch",
      "url": "https://...",
      "date_estimee": "2026-01-10",
      "theme": "Nouveaux modèles LLM",
      "snippet": "OpenAI unveiled GPT-5, featuring advanced reasoning...",
      "pertinence": 10,
      "tags": ["GPT-5", "OpenAI", "reasoning"]
    }
  ],
  "statistiques": {
    "articles_bruts": 87,
    "doublons_supprimes": 23,
    "articles_non_pertinents": 49,
    "articles_finaux": 15
  },
  "themes": {
    "Nouveaux modèles LLM": 3,
    "Régulation & gouvernance": 2,
    "Open source & écosystèmes": 4,
    "Recherche scientifique": 2
  }
}
```

### Markdown final (Agent 2 → Google Drive)

```markdown
---
agent: Veille IA (2 agents OpenAI)
date: 2026-01-11
catégorie: Intelligence Artificielle
---

# Veille IA & LLM – Semaine du 04/01/2026 au 11/01/2026
**Édition Gradient**

## Introduction
[Synthèse du climat de la semaine...]

## Nouveaux modèles LLM – OpenAI dévoile GPT-5

### Résumé
[Faits essentiels, enjeux, impacts...]

### Points de vue croisés

**TechCrunch**
[Angle éditorial...]

**The Verge**
[Divergences...]

### Sources
- OpenAI unveils GPT-5 – https://...
```

---

## 🐛 Dépannage

### Erreur : "TAVILY_API_KEY manquante"
1. Créer un compte sur https://tavily.com
2. Copier la clé API
3. Ajouter dans GitHub Secrets : `TAVILY_API_KEY`

### Erreur : "JSON non créé"
- Vérifier les logs de l'Agent 1
- Vérifier la clé OpenAI (`OPENAI_API_KEY`)
- Vérifier la clé Tavily (`TAVILY_API_KEY`)

### Erreur : "Google Drive upload failed"
- Vérifier `GOOGLE_DRIVE_CREDENTIALS` (JSON valide)
- Vérifier `GOOGLE_DRIVE_FOLDER_ID`
- Vérifier les permissions du service account sur le dossier

---

## 📈 Évolutions prévues

### Phase 3 : Agent Veille News (actualités générales)
- Dupliquer l'architecture 2-agents pour les actualités
- Fichiers : `agent_collecteur_news.py` + `agent_synthese_news.py`
- Output : `VeilleNews.md`

### Phase 4 : Frontend web
- Créer le site web qui lit `VeilleIA.md` et `VeilleNews.md` depuis Google Drive
- Architecture sécurisée (proxy GitHub Actions)

### Phase 5 : Nettoyage
- Supprimer les anciens agents Anthropic
- Supprimer `ANTHROPIC_API_KEY`
- Désactiver ancien workflow `agents-collecteurs.yml`

---

## 📝 Licence

Projet VeilleNLI - Nicolas Liziard (nliziard-ops)
