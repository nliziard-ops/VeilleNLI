# Documentation Technique VeilleNLI

**Date de mise à jour** : 3 février 2026  
**Statut** : Production stable  
**Architecture** : OpenAI GPT-5.2 + GPT-4o-mini

---

## 📋 Vue d'ensemble

VeilleNLI est un système de veille automatisée qui génère quotidiennement deux rapports d'actualité :

- **Veille IA & LLM** : Actualités sur l'Intelligence Artificielle et les modèles de langage
- **Veille Actualités** : Actualités générales (internationale, nationale, locale Bretagne)

Le système s'exécute **tous les jours à 6h00 (Paris)** via GitHub Actions et publie automatiquement les résultats sur **GitHub Pages**.

### Site web
https://nliziard-ops.github.io/VeilleNLI/

---

## 🏗️ Architecture actuelle (Février 2026)

### Workflow principal : `deep-research-daily.yml`

Le workflow s'exécute en **6 jobs séquentiels** :

```
┌─────────────────────────────────────────────────────────────┐
│                WORKFLOW DEEP RESEARCH QUOTIDIEN             │
│           Schedule: Tous les jours à 6h00 Paris            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────┐
│  JOB 1: Research IA │ → GPT-5.2 avec web_search
│  deep_research_ia.py│    Génère: research_ia.md
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│ JOB 2: Research News│ → GPT-5.2 avec web_search
│deep_research_news.py│    Génère: research_news.md
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│ JOB 3: Formatter    │ → GPT-4o-mini (économique)
│ agent_formatter.py  │    Fusionne + met en forme
│                     │    Upload: VeilleIA.md + VeilleNews.md
│                     │    Destination: Google Drive
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│ JOB 4: Sync GitHub  │ → Python script inline
│   Download Drive    │    Télécharge depuis Google Drive
│   Commit Markdown   │    Commit: docs/markdown/*.md
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│ JOB 5: Génère JSON  │ → agent_generateur_json.py
│   Parse Markdown    │    Parse les .md depuis Drive
│   data.json         │    Génère: docs/data.json
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│ JOB 6: Résumé final │ → Affiche statistiques
│   Workflow Summary  │    Confirme succès pipeline
└─────────────────────┘
```

---

## 🤖 Agents OpenAI utilisés

### 1. Deep Research IA (`deep_research_ia.py`)

**Modèle** : GPT-5.2 avec web_search  
**Entrée** : Prompt de recherche thématique IA  
**Sortie** : `research_ia.md` (15-20 articles trouvés)

**Fonctionnalités** :
- Recherche web **live** avec l'outil natif OpenAI `web_search`
- Extraction des citations **réelles** depuis les annotations de réponse
- Focus géographique : USA (50%), Europe (30%), Asie (15%), Nantes/Bretagne (5%)
- Thèmes couverts : Nouveaux modèles LLM, Agents autonomes, Multimodal AI, Reasoning models, Open source, Recherche scientifique, Régulation, Safety, Investissements, Hardware IA, Startups françaises, IA Nantes/Bretagne

**Configuration** :
```python
model="gpt-5.2"
max_output_tokens=4000
reasoning={"effort": "medium"}
tools=[{"type": "web_search"}]
```

**Budget estimé** : ~0.10€ par exécution

**Méthode d'appel** :
```python
response = client.responses.create(
    model="gpt-5.2",
    input=prompt,
    max_output_tokens=4000,
    reasoning={"effort": "medium"},
    tools=[{"type": "web_search"}]
)
```

---

### 2. Deep Research News (`deep_research_news.py`)

**Modèle** : GPT-5.2 avec web_search  
**Entrée** : Prompt de recherche actualités générales  
**Sortie** : `research_news.md` (15-20 articles trouvés)

**Fonctionnalités** :
- Recherche web **live** avec l'outil natif OpenAI `web_search`
- Extraction des citations **réelles** depuis les annotations
- Focus géographique : International (35%), National France (35%), Local Bretagne/Pays de Loire (30%)
- Thèmes couverts : Politique, Économie, Société, International, Environnement, Technologie, Culture, **Sports maritimes** (voile, surf, kitesurf, wingfoil)

**Configuration** : Identique à Deep Research IA

**Budget estimé** : ~0.10€ par exécution

---

### 3. Agent Formatter (`agent_formatter.py`)

**Modèle** : GPT-4o-mini-2024-07-18 (économique)  
**Entrée** : `research_ia.md` + `research_news.md`  
**Sortie** : `VeilleIA.md` + `VeilleNews.md` (formatés)

**Rôle** : Transforme les recherches brutes en synthèses élégantes avec :
- Sélection des **6 articles les plus pertinents** (score 8-10)
- Structure markdown professionnelle avec métadonnées YAML
- Section "Autres sujets" pour les articles restants (format compact)
- Synthèse finale avec points clés, divergences, signaux faibles
- Upload automatique sur **Google Drive**

**Configuration** :
```python
model="gpt-4o-mini-2024-07-18"
temperature=0.7
max_tokens=8000
```

**Budget estimé** : ~0.04€ par exécution (2 documents)

**Tarification GPT-4o-mini** :
- Input : $0.15 / 1M tokens
- Output : $0.60 / 1M tokens

---

### 4. Agent Générateur JSON (`agent_generateur_json.py`)

**Type** : Script Python pur (pas de LLM)  
**Entrée** : `VeilleIA.md` + `VeilleNews.md` (depuis Google Drive)  
**Sortie** : `docs/data.json`

**Fonctionnalités** :
- Parsing avancé du Markdown (front matter, sections, sous-sections)
- Extraction des métadonnées (agent, date, catégorie)
- Structuration JSON pour le frontend React
- Détection intelligente de la section "Autres sujets" (stop parsing)
- Génération d'icônes adaptées par catégorie

**Structure JSON générée** :
```json
{
  "version": "2.0",
  "date_generation": "2026-02-03T06:30:00",
  "veilles": {
    "ia": {
      "metadata": {...},
      "titre": "Veille IA & LLM – Semaine...",
      "edition": "Édition Reasoning",
      "introduction": "...",
      "sujets_importants": [
        {
          "titre": "...",
          "resume": "...",
          "resume_court": "...",
          "resume_complet": "...",
          "points_de_vue": [...],
          "fiabilite": [...],
          "sources": [...],
          "contenu_complet": "...",
          "icone": "🤖"
        }
      ],
      "sujets_secondaires": [...],
      "points_cles": [...]
    },
    "news": {...}
  }
}
```

**Budget** : Gratuit (pas d'appel API)

---

## 💰 Budget et Optimisations

### Coûts quotidiens

| Composant | Modèle | Coût estimé |
|-----------|--------|-------------|
| Deep Research IA | GPT-5.2 | ~0.10€ |
| Deep Research News | GPT-5.2 | ~0.10€ |
| Formatter (2 docs) | GPT-4o-mini | ~0.04€ |
| Générateur JSON | Python pur | 0.00€ |
| **TOTAL** | - | **~0.24€/jour** |

### Coûts mensuels

- **Par mois (30 jours)** : ~7.20€
- **Budget 40€/mois** : Largement suffisant avec **32.80€ de marge**

### Optimisations appliquées

1. **GPT-4o-mini pour la mise en forme** : 10x moins cher que GPT-4 Turbo
2. **Web search natif OpenAI** : Pas de coût Tavily API externe
3. **Générateur JSON en Python pur** : Pas d'appel LLM pour le parsing
4. **Token limits adaptés** :
   - Deep Research : 4000 tokens output (suffisant pour 15-20 articles)
   - Formatter : 8000 tokens output (format détaillé)
5. **Reasoning effort "medium"** : Équilibre qualité/coût/latence

---

## 🔐 Configuration Secrets GitHub

Le système nécessite **3 secrets** configurés dans Settings → Secrets and variables → Actions :

### `OPENAI_API_KEY`
- **Type** : Clé API OpenAI
- **Format** : `sk-proj-...`
- **Usage** : Agents Deep Research + Formatter
- **Permissions requises** : Accès modèles GPT-5.2 et GPT-4o-mini

### `GOOGLE_DRIVE_CREDENTIALS`
- **Type** : Service Account JSON
- **Format** : JSON complet du compte de service Google Cloud
- **Usage** : Upload/Download des fichiers Markdown
- **Permissions requises** : 
  - `https://www.googleapis.com/auth/drive` (lecture/écriture)
  - Accès au dossier spécifié par `GOOGLE_DRIVE_FOLDER_ID`

### `GOOGLE_DRIVE_FOLDER_ID`
- **Type** : ID de dossier Google Drive
- **Format** : `1abc...xyz` (extrait de l'URL du dossier)
- **Usage** : Stockage des fichiers Markdown finaux

---

## 🔄 Flux de données

```
┌─────────────────────────────────────────────────────────────┐
│                    FLUX DE DONNÉES                          │
└─────────────────────────────────────────────────────────────┘

1. RECHERCHE WEB
   ├─ deep_research_ia.py → research_ia.md (artifact)
   └─ deep_research_news.py → research_news.md (artifact)

2. MISE EN FORME
   ├─ agent_formatter.py
   │   ├─ Input: research_ia.md + research_news.md
   │   ├─ Processing: GPT-4o-mini
   │   └─ Output: VeilleIA.md + VeilleNews.md → Google Drive

3. SYNCHRONISATION
   ├─ Sync GitHub (Python inline)
   │   ├─ Download: VeilleIA.md + VeilleNews.md ← Google Drive
   │   └─ Commit: docs/markdown/*.md → GitHub repo

4. GÉNÉRATION JSON
   ├─ agent_generateur_json.py
   │   ├─ Input: VeilleIA.md + VeilleNews.md ← Google Drive
   │   ├─ Processing: Python parsing
   │   └─ Output: docs/data.json → GitHub repo

5. PUBLICATION
   └─ GitHub Pages
       ├─ Source: docs/data.json
       └─ Site: https://nliziard-ops.github.io/VeilleNLI/
```

---

## 📂 Structure du repository

```
VeilleNLI/
├── .github/
│   └── workflows/
│       ├── deep-research-daily.yml    # [ACTIF] Workflow quotidien
│       ├── list-models.yml            # [UTIL] Test modèles OpenAI
│       ├── update-data.yml            # [VIDE] Placeholder
│       ├── veille-openai-complete.yml # [INACTIF] Ancien workflow
│       └── veille-quotidienne.yml     # [INACTIF] Ancien workflow
│
├── agents/
│   ├── deep_research_ia.py            # [ACTIF] Agent recherche IA
│   ├── deep_research_news.py          # [ACTIF] Agent recherche News
│   ├── agent_formatter.py             # [ACTIF] Agent mise en forme
│   ├── agent_generateur_json.py       # [ACTIF] Générateur JSON
│   │
│   └── [AGENTS INACTIFS - Anciens systèmes]
│       ├── agent_recherche_ia.py
│       ├── agent_recherche_news.py
│       ├── agent_synthese_ia_v2.py
│       ├── agent_synthese_news_v2.py
│       ├── agent_collecteur_ia.py
│       ├── agent_collecteur_news.py
│       ├── agent_synthese_ia.py
│       ├── agent_synthese_news.py
│       └── agent_validateur_markdown.py
│
├── docs/
│   ├── index.html                     # Frontend React
│   ├── data.json                      # Données structurées (généré)
│   └── markdown/
│       ├── VeilleIA.md                # Markdown IA (synced)
│       └── VeilleNews.md              # Markdown News (synced)
│
├── README.md                          # Documentation utilisateur
├── DOCUMENTATION_TECHNIQUE.md         # Ce fichier
├── ARCHITECTURE_MEMOIRE.md            # État du système (ce fichier)
└── requirements.txt                   # Dépendances Python
```

---

## 🛠️ Technologies

### Backend
- **Python** : 3.11+
- **OpenAI SDK** : `openai` (dernière version)
- **Google Drive API** : `google-api-python-client`, `google-auth`

### LLM
- **GPT-5.2** : Recherche web avec extended thinking
- **GPT-4o-mini** : Mise en forme économique

### Frontend
- **React 18** : UI dynamique
- **Babel Standalone** : Transpilation JSX côté client
- **Marked.js** : Parsing Markdown
- **Fetch API** : Chargement `data.json`

### Hosting
- **GitHub Actions** : CI/CD (exécution quotidienne)
- **GitHub Pages** : Hosting statique
- **Google Drive** : Stockage intermédiaire Markdown

---

## ⚙️ Configuration du workflow

### Schedule
```yaml
on:
  schedule:
    - cron: '0 5 * * *'  # 6h00 Paris (5h00 UTC en hiver)
  workflow_dispatch:      # Déclenchement manuel
```

### Timeouts
- Deep Research : 15 minutes (recherche longue)
- Formatter : 10 minutes
- Sync & JSON : 5 minutes

### Retry logic
- **Git operations** : 3 tentatives avec `--rebase -X ours`
- **Sleep** : 2-5 secondes entre tentatives

---

## 🧪 Tests locaux

### 1. Test Deep Research IA
```bash
export OPENAI_API_KEY="sk-proj-..."
python agents/deep_research_ia.py

# Vérifier la sortie
cat research_ia.md
```

### 2. Test Deep Research News
```bash
python agents/deep_research_news.py
cat research_news.md
```

### 3. Test Formatter
```bash
export GOOGLE_DRIVE_CREDENTIALS='{"type":"service_account",...}'
export GOOGLE_DRIVE_FOLDER_ID="1abc...xyz"
python agents/agent_formatter.py

# Vérifier upload Google Drive
```

### 4. Test Générateur JSON
```bash
python agents/agent_generateur_json.py

# Vérifier la sortie
cat docs/data.json | python -m json.tool
```

### 5. Test Frontend local
```bash
cd docs
python -m http.server 8000
# Ouvrir http://localhost:8000
```

---

## 🐛 Dépannage

### Workflow échoue

**Symptôme** : Job échoue dans GitHub Actions

**Actions** :
1. Consulter les logs du job en échec
2. Vérifier les secrets GitHub (Settings → Secrets)
3. Vérifier les quotas OpenAI (https://platform.openai.com/usage)
4. Vérifier l'accès Google Drive du service account

### Site n'affiche pas les données

**Symptôme** : Page blanche ou erreur dans la console

**Actions** :
1. Ouvrir la console navigateur (F12)
2. Vérifier que `data.json` est accessible : https://nliziard-ops.github.io/VeilleNLI/data.json
3. Valider le JSON : https://jsonlint.com/
4. Vérifier les CORS (GitHub Pages devrait autoriser)

### Parsing JSON échoue

**Symptôme** : `agent_generateur_json.py` ne détecte pas les sections

**Actions** :
1. Vérifier le format Markdown sur Google Drive
2. Tester le regex de détection "Autres sujets" :
   ```python
   import re
   pattern = re.compile(r'^##\s+Autres\s+(sujet|sujets|actualité|actualités)', re.IGNORECASE)
   pattern.match("## Autres sujets de la semaine")  # Doit retourner un match
   ```
3. Ajouter des logs dans le parser pour debug

### Coûts OpenAI élevés

**Symptôme** : Coût quotidien > 0.30€

**Actions** :
1. Consulter https://platform.openai.com/usage
2. Vérifier les tokens utilisés dans les logs GitHub Actions
3. Réduire `max_output_tokens` si nécessaire
4. Vérifier qu'il n'y a pas d'exécutions multiples non prévues

---

## 📊 Monitoring

### Métriques clés à surveiller

| Métrique | Valeur attendue | Alerte si |
|----------|-----------------|----------|
| Coût quotidien | ~0.24€ | > 0.35€ |
| Temps total workflow | 5-8 min | > 15 min |
| Taille `data.json` | 20-50 KB | < 10 KB ou > 100 KB |
| Sujets IA principaux | 6 | < 6 |
| Sujets News principaux | 6 | < 6 |
| Succès workflow | 100% | < 95% |

### Logs à consulter

1. **GitHub Actions** : https://github.com/nliziard-ops/VeilleNLI/actions
   - Workflow "Deep Research Quotidien"
   - Consulter chaque job pour voir les logs détaillés

2. **OpenAI Usage** : https://platform.openai.com/usage
   - Coûts quotidiens par modèle
   - Tokens consommés

3. **Google Drive** : Vérifier manuellement
   - Présence de `VeilleIA.md` et `VeilleNews.md`
   - Date de dernière modification

---

## 🚀 Amélirations futures possibles

### Court terme
- [ ] Ajouter des tests unitaires (pytest)
- [ ] Créer un script de validation pre-commit
- [ ] Ajouter un dashboard de monitoring (GitHub Pages)

### Moyen terme
- [ ] Migrer vers GPT-5.3 si disponible (meilleure qualité)
- [ ] Ajouter un système de cache pour réduire les coûts
- [ ] Implémenter des notifications (email/Slack) en cas d'échec

### Long terme
- [ ] Développer une API REST pour accès programmatique
- [ ] Créer une app mobile (React Native)
- [ ] Ajouter des fonctionnalités de personnalisation utilisateur

---

**Dernière mise à jour** : 3 février 2026  
**Mainteneur** : Nicolas Liziard (@nliziard-ops)
