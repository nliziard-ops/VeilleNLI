# 🏗️ ARCHITECTURE v3

Documentation technique du système VeilleNLI.

---

## 📊 Vue d'ensemble

### Pipeline de traitement

```
┌─────────────────────────────────────────────────────────────┐
│                     GITHUB ACTIONS                          │
│                   Quotidien 6h00 Paris                      │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┴───────────────────┐
        ▼                                       ▼
┌────────────────┐                     ┌────────────────┐
│ RECHERCHE IA   │                     │ RECHERCHE NEWS │
│ GPT-5.2        │                     │ GPT-5.2        │
│ Web Search     │                     │ Web Search     │
│ → 25 articles  │                     │ → 25 articles  │
└────────┬───────┘                     └────────┬───────┘
         │                                      │
         │ recherche_ia_brute.json              │ recherche_news_brute.json
         │                                      │
         ▼                                      ▼
┌────────────────┐                     ┌────────────────┐
│ SYNTHÈSE IA    │                     │ SYNTHÈSE NEWS  │
│ GPT-5.2 Pro    │                     │ GPT-5.2 Pro    │
│ Top 6 + Autres │                     │ Top 6 + Autres │
│ → VeilleIA.md  │                     │ → VeilleNews.md│
└────────┬───────┘                     └────────┬───────┘
         │                                      │
         └──────────┬───────────────────────────┘
                    ▼
           ┌─────────────────┐
           │ VALIDATION      │
           │ Markdown check  │
           └────────┬────────┘
                    ▼
           ┌─────────────────┐
           │ SYNC GITHUB     │
           │ Drive → GitHub  │
           └────────┬────────┘
                    ▼
           ┌─────────────────┐
           │ GÉNÉRATION JSON │
           │ → data.json     │
           └────────┬────────┘
                    ▼
           ┌─────────────────┐
           │ GITHUB PAGES    │
           │ Site React      │
           └─────────────────┘
```

---

## 🤖 Agents

### 1. Recherche IA v3
**Fichier** : `agents/agent_recherche_ia_v3.py`  
**Modèle** : GPT-5.2 + web search  
**Input** : Prompt de collecte  
**Output** : `recherche_ia_brute.json` (25 articles)  
**Tokens** : ~10k

**Rôle** : Collecte brute d'articles IA/LLM sans analyse

### 2. Synthèse IA v3
**Fichier** : `agents/agent_synthese_ia_v3.py`  
**Modèle** : GPT-5.2 Pro  
**Input** : `recherche_ia_brute.json`  
**Output** : `VeilleIA.md` (Google Drive)  
**Tokens** : ~8k

**Rôle** : Sélection Top 6 (3 buzz + 3 tech) + analyse complète

### 3. Recherche News v3
**Fichier** : `agents/agent_recherche_news_v3.py`  
**Modèle** : GPT-5.2 + web search  
**Input** : Prompt de collecte  
**Output** : `recherche_news_brute.json` (25 articles)  
**Tokens** : ~21k

**Rôle** : Collecte brute actualités générales (int + nat + local)

### 4. Synthèse News v3
**Fichier** : `agents/agent_synthese_news_v3.py`  
**Modèle** : GPT-5.2 Pro  
**Input** : `recherche_news_brute.json`  
**Output** : `VeilleNews.md` (Google Drive)  
**Tokens** : ~8k

**Rôle** : Sélection Top 6 (2 int + 2 nat + 2 local) + analyse

### 5. Validateur Markdown
**Fichier** : `agents/agent_validateur_markdown.py`  
**Input** : Google Drive  
**Output** : Validation structure

**Rôle** : Vérifie la structure des fichiers markdown

### 6. Générateur JSON
**Fichier** : `agents/agent_generateur_json.py`  
**Input** : `VeilleIA.md` + `VeilleNews.md`  
**Output** : `docs/data.json`

**Rôle** : Parse markdown et génère JSON pour le site

---

## 🔄 Workflow GitHub Actions

**Fichier** : `.github/workflows/veille-openai-v3.yml`

### Jobs parallèles

**Job 1.1** : Recherche IA → **Job 1.2** : Synthèse IA  
**Job 2.1** : Recherche News → **Job 2.2** : Synthèse News

### Jobs séquentiels

**Job 3** : Validation (attend 1.2 + 2.2)  
**Job 4** : Sync GitHub (attend 3)  
**Job 5** : Génération JSON (attend 4)  
**Job 6** : Résumé

### Artifacts

- `recherche-ia-brute` : JSON intermédiaire IA
- `recherche-news-brute` : JSON intermédiaire News

---

## 📦 Storage

### Google Drive (stockage intermédiaire)

```
VeilleNLI/
├── VeilleIA.md
└── VeilleNews.md
```

**Rôle** : Stockage temporaire avant sync GitHub

### GitHub Repository

```
docs/
├── markdown/
│   ├── VeilleIA.md
│   └── VeilleNews.md
└── data.json
```

**Rôle** : Source pour GitHub Pages

---

## 🌐 Frontend

**Fichier** : `docs/index.html`  
**Framework** : React 18 (single-page)  
**Hosting** : GitHub Pages

### Fonctionnalités

- Chargement `data.json`
- Affichage Top 6 par catégorie (cartes expandables)
- Section "Autres sujets"
- Responsive design

---

## 🔐 Secrets

**OPENAI_API_KEY** : Clé API OpenAI  
**GOOGLE_DRIVE_CREDENTIALS** : Service account JSON  
**GOOGLE_DRIVE_FOLDER_ID** : ID dossier stockage

---

## 💾 Format de données

### JSON intermédiaire (recherche_*_brute.json)

```json
{
  "articles": [
    {
      "id": "abc123...",
      "titre": "...",
      "url": "https://...",
      "source": "...",
      "date_publication": "YYYY-MM-DD",
      "contenu_brut": "...",
      "categorie_auto": "..."
    }
  ],
  "nb_articles": 25,
  "periode": {"debut": "...", "fin": "..."},
  "model_utilise": "gpt-5.2",
  "tokens_utilises": 10000
}
```

### Markdown (VeilleIA.md / VeilleNews.md)

```markdown
---
agent: Synthèse IA v3
date: YYYY-MM-DD
---

# Veille IA – Semaine du XX au XX

## Introduction
[2-3 paragraphes]

---

## [SUJET 1/6] – [Titre]

### Résumé
### Points de vue croisés
### Analyse & implications
### Signaux faibles
### Sources

---

## Autres sujets

### [Titre]
**Thème** : [Cat]
**Résumé** : [1 ligne]
**Source** : [Nom] – [URL]

---

## Synthèse finale

### Points clés
### Divergences
### Signaux faibles
### Risques
### À surveiller
```

### JSON final (data.json)

```json
{
  "ia": {
    "introduction": "...",
    "mainArticles": [...],
    "otherTopics": [...],
    "synthesis": {...}
  },
  "news": {
    "introduction": "...",
    "mainArticles": [...],
    "otherTopics": [...],
    "synthesis": {...}
  }
}
```

---

## 🐛 Points d'attention

### Recherche News
**Problème** : Blocage robots sur sites d'actualités  
**Solution** : Utiliser requêtes web search génériques (pas d'accès direct)

### Format Markdown
**Problème** : Parser sensible aux séparateurs  
**Solution** : Respecter strictement `---` entre sections

### Tokens
**Recherche News** : Consomme ~21k tokens (plus que IA)  
**Cause** : Sources généralistes moins structurées

---

## 📊 Performance

**Durée totale** : 4-6 minutes  
**Recherche** : ~2 min (parallèle)  
**Synthèse** : ~2 min (parallèle)  
**Validation + Sync + JSON** : ~1 min

---

*Architecture v3 - Février 2026*
