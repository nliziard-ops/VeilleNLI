# 🤖 VeilleNLI - Veille Automatisée IA & Actualités

Système de veille quotidienne automatisé propulsé par **OpenAI GPT-5.2** et **GPT-4o-mini**.

🌐 **Site web** : https://nliziard-ops.github.io/VeilleNLI/

---

## 📋 Description

VeilleNLI génère **quotidiennement à 6h** deux veilles complètes :

- **🤖 Veille IA & LLM** : Actualités IA depuis sources institutionnelles
- **📰 Veille Actualités** : Presse internationale, nationale et locale (Bretagne)

### Architecture v3 : 4 agents séparés (Collecte | Synthèse)

**Pipeline IA :**
1. **Agent Recherche IA v3** (GPT-5.2, 10k tokens) : Collecte brute → `recherche_ia_brute.json`
2. **Agent Synthèse IA v3** (GPT-5.2 Pro, 8k tokens) : Sélection 6 sujets (3 buzz + 3 tech) + analyse → `VeilleIA.md`

**Pipeline News :**
1. **Agent Recherche News v3** (GPT-5.2, 10k tokens) : Collecte brute → `recherche_news_brute.json`
2. **Agent Synthèse News v3** (GPT-5.2 Pro, 8k tokens) : Sélection 6 sujets (2 int + 2 nat + 2 local) + analyse → `VeilleNews.md`

Puis : **Validation → Sync GitHub → data.json → GitHub Pages**

---

## 🚀 Utilisation

### Consulter les veilles

👉 **https://nliziard-ops.github.io/VeilleNLI/**

### Exécution manuelle

1. Aller sur [Actions](https://github.com/nliziard-ops/VeilleNLI/actions/workflows/veille-openai-v3.yml)
2. Cliquer sur **"Run workflow"**

**Durée** : ~4-6 minutes

---

## 💰 Coûts (Optimisés)

| Composant | Modèle | Coût/jour | Coût/mois |
|-----------|--------|-----------|-----------|
| Recherche IA | GPT-5.2 (10k tokens) | ~0.05€ | ~1.50€ |
| Synthèse IA | GPT-5.2 Pro (8k tokens) | ~0.15€ | ~4.50€ |
| Recherche News | GPT-5.2 (10k tokens) | ~0.05€ | ~1.50€ |
| Synthèse News | GPT-5.2 Pro (8k tokens) | ~0.15€ | ~4.50€ |
| **TOTAL** | - | **~0.40€** | **~12€** |

**Budget actuel** : 40€/mois (reste ~28€ de marge)

### Optimisations appliquées

- ✅ GPT-5.2 avec recherche web native (pas de Tavily)
- ✅ Agents séparés (collecte pure vs synthèse)
- ✅ Token limits stricts (10k recherche, 8k synthèse)
- ✅ Température optimisée (0.1 collecte, 0.7 synthèse)
- ✅ Exécutions parallèles (IA + News simultanées)

---

## 🏗️ Architecture Technique

```
┌─────────────────────────────────────────────────────┐
│  Workflow v3 (quotidien 6h Paris)                   │
├─────────────────────────────────────────────────────┤
│                                                     │
│  1.1 Recherche IA v3  ║  2.1 Recherche News v3     │
│      (GPT-5.2)        ║      (GPT-5.2)             │
│      10k tokens       ║      10k tokens            │
│      ↓                ║      ↓                     │
│  recherche_ia.json    ║  recherche_news.json       │
│      ↓                ║      ↓                     │
│  1.2 Synthèse IA v3   ║  2.2 Synthèse News v3      │
│      (GPT-5.2 Pro)    ║      (GPT-5.2 Pro)         │
│      8k tokens        ║      8k tokens             │
│      ↓                ║      ↓                     │
│  VeilleIA.md          ║  VeilleNews.md             │
│  (Google Drive)       ║  (Google Drive)            │
│                                                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  3. Validation Markdown                             │
│  4. Sync → GitHub (docs/markdown/)                  │
│  5. Génération data.json                            │
│  6. Résumé final                                    │
│                                                     │
└─────────────────────────────────────────────────────┘
                    ↓
         ┌────────────────────┐
         │  Frontend React    │
         │  GitHub Pages      │
         └────────────────────┘
```

---

## 📁 Structure du Projet

```
VeilleNLI/
├── .github/workflows/
│   ├── veille-openai-v3.yml       # [ACTIF] Pipeline quotidien 4-agents
│   └── cleanup-repo.yml           # Workflow de nettoyage (manuel)
│
├── agents/
│   ├── agent_recherche_ia_v3.py       # [ACTIF] Collecte IA
│   ├── agent_synthese_ia_v3.py        # [ACTIF] Synthèse IA
│   ├── agent_recherche_news_v3.py     # [ACTIF] Collecte News
│   ├── agent_synthese_news_v3.py      # [ACTIF] Synthèse News
│   ├── agent_validateur_markdown.py   # Validation Markdown
│   └── agent_generateur_json.py       # Génération data.json
│
├── scripts/
│   ├── list_openai_models.py          # Lister modèles OpenAI
│   └── cleanup_repository.py          # Script de nettoyage
│
├── docs/                              # GitHub Pages
│   ├── index.html                     # Frontend React
│   ├── data.json                      # Données structurées
│   └── markdown/
│       ├── VeilleIA.md
│       └── VeilleNews.md
│
├── README.md                          # Ce fichier
└── requirements.txt                   # Dépendances Python
```

---

## 🛠️ Technologies

- **Backend** : Python 3.11+
- **LLM** : OpenAI GPT-5.2 / GPT-5.2 Pro
- **Storage** : Google Drive API
- **Frontend** : React 18, Babel, Marked.js
- **Hosting** : GitHub Pages
- **CI/CD** : GitHub Actions

---

## 🔐 Secrets GitHub

```bash
OPENAI_API_KEY              # Clé API OpenAI (GPT-5.2)
GOOGLE_DRIVE_CREDENTIALS    # Service account Google Drive (JSON)
GOOGLE_DRIVE_FOLDER_ID      # ID du dossier de stockage
```

---

## 🧹 Nettoyage du Repository

Le repository a été **nettoyé** pour ne conserver que les fichiers essentiels du workflow v3.

### Méthode 1 : Workflow GitHub Actions (Recommandé)

1. Aller sur [Actions](https://github.com/nliziard-ops/VeilleNLI/actions/workflows/cleanup-repo.yml)
2. Cliquer sur **"Run workflow"**
3. Confirmer l'exécution

**Le workflow va** :
- Supprimer tous les workflows obsolètes
- Supprimer toutes les documentations de migration
- Supprimer tous les agents v1 et v2
- Supprimer les dossiers `archive/` et `config/`
- Commit et push automatique

### Méthode 2 : Script Python local

```bash
# Simulation (affiche ce qui serait supprimé)
python scripts/cleanup_repository.py

# Exécution réelle
python scripts/cleanup_repository.py --execute
```

### Fichiers conservés après nettoyage

**Workflows** :
- ✅ `veille-openai-v3.yml` (actif)
- ✅ `cleanup-repo.yml` (nettoyage)

**Agents** :
- ✅ `agent_recherche_ia_v3.py`
- ✅ `agent_synthese_ia_v3.py`
- ✅ `agent_recherche_news_v3.py`
- ✅ `agent_synthese_news_v3.py`
- ✅ `agent_validateur_markdown.py`
- ✅ `agent_generateur_json.py`

**Autres** :
- ✅ `docs/` (site web complet)
- ✅ `scripts/list_openai_models.py`
- ✅ `README.md`
- ✅ `requirements.txt`

---

## 🧪 Tests Locaux

```bash
# 1. Installation
pip install -r requirements.txt

# 2. Variables d'environnement
export OPENAI_API_KEY="sk-..."
export GOOGLE_DRIVE_CREDENTIALS='{"type":"service_account",...}'
export GOOGLE_DRIVE_FOLDER_ID="1xxx"

# 3. Test Recherche IA
python agents/agent_recherche_ia_v3.py

# 4. Test Synthèse IA (nécessite recherche_ia_brute.json)
python agents/agent_synthese_ia_v3.py

# 5. Test Recherche News
python agents/agent_recherche_news_v3.py

# 6. Test Synthèse News
python agents/agent_synthese_news_v3.py

# 7. Validation JSON
cat docs/data.json | python -m json.tool

# 8. Servir le site localement
cd docs && python -m http.server 8000
# → http://localhost:8000
```

---

## 📊 Monitoring

### GitHub Actions

- **Workflow actif** : [Veille OpenAI v3](https://github.com/nliziard-ops/VeilleNLI/actions/workflows/veille-openai-v3.yml)
- **Dernière exécution** : Vérifier la page Actions
- **Schedule** : Quotidien à 6h00 (Europe/Paris)

### Métriques clés

| Métrique | Valeur cible |
|----------|--------------|
| Durée d'exécution | 4-6 minutes |
| Taille data.json | 30-60 KB |
| Sujets IA | 6 principaux + 15-20 autres |
| Sujets News | 6 principaux + 15-20 autres |
| Coût quotidien | ~0.40€ |
| Taux de succès | >95% |

---

## 🔧 Dépannage

### Workflow échoue

1. **Vérifier les secrets** : Settings → Secrets and variables → Actions
2. **Consulter les logs** : Actions → Dernier workflow → Chaque job a ses logs
3. **Quotas OpenAI** : Vérifier sur platform.openai.com

### Site n'affiche rien

1. **Ouvrir la console** : F12 dans le navigateur
2. **Vérifier data.json** : https://nliziard-ops.github.io/VeilleNLI/data.json
3. **Valider le JSON** : Copier-coller sur jsonlint.com

### Données manquantes

1. **Vérifier Google Drive** : Les fichiers `VeilleIA.md` et `VeilleNews.md` doivent exister
2. **Relancer le workflow** : Actions → Run workflow
3. **Consulter Job 5** : Logs du générateur JSON

---

## 🎯 Profil du Lecteur

- **Tech** : IA/LLM, recherche, startups, régulation
- **Actualités** : Politique, économie, international
- **Sports maritimes** : Voile, surf, kitesurf, wingfoil
- **Local** : Nantes, Bretagne, Belle-Île-en-Mer

---

## 📅 Historique

- **Février 2026** : Migration v3 - Architecture séparée (Collecte | Synthèse)
- **Janvier 2026** : Migration OpenAI GPT-5.2
- **Décembre 2025** : Architecture 4-agents OpenAI
- **Novembre 2025** : Migration Anthropic → OpenAI
- **Octobre 2025** : Création du projet (Anthropic Claude)

---

## 📝 Licence

Tous droits réservés - Nicolas Liziard (@nliziard-ops)

---

*Dernière mise à jour : Février 2026 - Architecture v3 (GPT-5.2)*
