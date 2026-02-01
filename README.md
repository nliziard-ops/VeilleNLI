# VeilleNLI

Système de veille automatisée sur l'Intelligence Artificielle et les actualités générales, propulsé par **ChatGPT-4 Turbo** (OpenAI).

## 🌐 Site web

**https://nliziard-ops.github.io/VeilleNLI/**

---

## 📋 Description

VeilleNLI génère quotidiennement deux veilles hebdomadaires via un **pipeline 4-agents** :

- **Veille IA & LLM** : Actualités IA depuis sources institutionnelles (Anthropic, OpenAI, Mistral, DeepSeek, etc.)
- **Veille Actualités** : Presse nationale/internationale/locale (35% int, 35% nat, 30% local Bretagne)

### Architecture 4-agents (ChatGPT-4 Turbo)

Le système utilise **2 pipelines parallèles** de 2 agents chacun :

**Pipeline IA :**
1. **Agent Recherche IA** (GPT-4 Turbo + web_search) : Collecte factuelle depuis sites institutionnels → `recherche_ia_brute.json`
2. **Agent Synthèse IA** (GPT-4 Turbo) : Sélectionne 6 sujets (3 tendances + 3 tech) + analyse approfondie → `VeilleIA.md`

**Pipeline News :**
1. **Agent Recherche News** (GPT-4 Turbo + web_search) : Collecte factuelle depuis presse → `recherche_news_brute.json`
2. **Agent Synthèse News** (GPT-4 Turbo) : Sélectionne 6 sujets (2 int + 2 nat + 2 local) + analyse approfondie → `VeilleNews.md`

Puis : Validation → Sync GitHub → Génération data.json → Commit → GitHub Pages

---

## ✨ Fonctionnalités

### Recherche Web Factuelle (Agents 1 & 2)

- ✅ **ChatGPT-4 Turbo** avec capacité `web_search` native
- ✅ **Sources IA institutionnelles** : Anthropic, OpenAI, Mistral, DeepSeek, The Hacker News, DeepLearning.AI, Google AI, NVIDIA AI
- ✅ **Presse internationale** : Le Grand Continent, El País, BBC, Reuters
- ✅ **Presse nationale** : Le Figaro, Le Monde, Le Monde Diplomatique
- ✅ **Presse locale Bretagne** : Ouest-France, Le Télégramme
- ✅ **Collecte pure sans interprétation** : Titre, résumé court, synthèse complète, source, URL

### Synthèse Analytique (Agents 3 & 4)

**Veille IA - 6 sujets sélectionnés :**
- **3 premiers** : Tendances qui font parler (buzz, controverses, ruptures)
- **3 suivants** : Sujets technologiques (avancées, modèles, hardware)

**Veille News - 6 sujets répartition obligatoire :**
- **2 internationaux** (géopolitique, économie mondiale)
- **2 nationaux** (France : politique, économie, société)
- **2 locaux** (Bretagne/Pays de Loire : politique locale, sports maritimes, mer)

**Pour chaque sujet :**
- Résumé court (3-4 lignes)
- Synthèse approfondie (15-25 lignes) : contexte, faits, impacts, analyse
- Divergences entre sources
- Toutes les sources citées avec URLs

**Autres sujets (liste compacte) :**
- Titre
- Résumé court (2-3 lignes)
- Synthèse (5-8 lignes)
- Source unique avec URL

### Frontend Web

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

1. **Workflow complet (4-agents)** :  
   https://github.com/nliziard-ops/VeilleNLI/actions/workflows/veille-openai-complete.yml  
   → Cliquer "Run workflow"

2. **Le workflow exécute automatiquement** :
   - Recherches web parallèles (IA + News)
   - Synthèses analytiques
   - Upload Google Drive
   - Sync Markdown vers GitHub
   - Génération data.json
   - Commit sur GitHub
   - Le site se met à jour automatiquement

**Durée totale** : ~5-8 minutes

---

## 📊 Coûts

**Architecture 4-agents ChatGPT-4 Turbo**

| Agent | Modèle | Tokens | Coût/jour |
|-------|--------|--------|------------|
| Recherche IA | GPT-4 Turbo | ~5K | ~0.06€ |
| Synthèse IA | GPT-4 Turbo | ~10K | ~0.12€ |
| Recherche News | GPT-4 Turbo | ~5K | ~0.06€ |
| Synthèse News | GPT-4 Turbo | ~10K | ~0.12€ |
| **TOTAL** | - | ~30K | **~0.36€** |

**Par mois** : ~10.80€  
**Budget jusqu'à fin mars (60 jours)** : ~21.60€

### Optimisations appliquées

- ✅ GPT-4 Turbo au lieu de GPT-4 (3x moins cher)
- ✅ web_search natif (pas de Tavily API)
- ✅ Token limits : 8K recherche, 12K synthèse
- ✅ Exécution parallèle (recherches IA + News simultanées)
- ✅ Température optimisée : 0.1 (recherche), 0.7 (synthèse)

### Comparaison architectures

| Critère | Ancien (Tavily) | Nouveau (ChatGPT-4 Turbo) |
|---------|-----------------|---------------------------|
| **Qualité** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Fraîcheur** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Sources** | Tavily API | Sites directs |
| **Analyse** | Superficielle | Approfondie |
| **Divergences** | ❌ | ✅ |
| **Coût/jour** | ~0.18€ | ~0.36€ |

---

## 🏭 Architecture technique

```
┌──────────────────────────────────────────────────────────────┐
│     Workflow Veille OpenAI Complète (6h Paris)              │
│                                                              │
│  ┌─────────────────────┐    ┌─────────────────────┐        │
│  │ 1.1 Recherche IA      │    │ 2.1 Recherche News  │        │
│  │ GPT-4 Turbo          │    │ GPT-4 Turbo         │        │
│  │ web_search           │    │ web_search          │        │
│  │                       │    │                     │        │
│  │ Sources inst. IA     │    │ Presse int/nat/loc  │        │
│  │                       │    │                     │        │
│  │ → recherche_ia.json   │    │ → recherche_news.json│        │
│  └───────────┬──────────┘    └──────────┬──────────┘        │
│             │                        │                   │
│             ↓                        ↓                   │
│  ┌───────────┴──────────┐    ┌──────────┴──────────┐        │
│  │ 1.2 Synthèse IA       │    │ 2.2 Synthèse News   │        │
│  │ GPT-4 Turbo          │    │ GPT-4 Turbo         │        │
│  │                       │    │                     │        │
│  │ Sélection 6 sujets :  │    │ Sélection 6 sujets :│        │
│  │ - 3 tendances        │    │ - 2 internationaux  │        │
│  │ - 3 tech             │    │ - 2 nationaux       │        │
│  │                       │    │ - 2 locaux          │        │
│  │ Analyse approfondie  │    │ Analyse approfondie │        │
│  │ Divergences sources  │    │ Divergences sources │        │
│  │                       │    │                     │        │
│  │ → VeilleIA.md        │    │ → VeilleNews.md     │        │
│  │ Upload Google Drive  │    │ Upload Google Drive │        │
│  └───────────┬──────────┘    └──────────┬──────────┘        │
│             └────────┬───────────────────────┘                   │
│                        ↓                                   │
│            ┌────────────────────────────┐                  │
│            │ 3. Validation Markdown     │                  │
│            │                            │                  │
│            │ Vérifie VeilleIA.md       │                  │
│            │ Vérifie VeilleNews.md     │                  │
│            └────────────┬───────────────┘                  │
│                         ↓                                   │
│            ┌────────────────────────────┐                  │
│            │ 4. Sync Markdown → GitHub │                  │
│            │                            │                  │
│            │ Download Google Drive      │                  │
│            │ → docs/markdown/*.md      │                  │
│            │ Commit GitHub              │                  │
│            └────────────┬───────────────┘                  │
│                         ↓                                   │
│            ┌────────────────────────────┐                  │
│            │ 5. Génération data.json   │                  │
│            │                            │                  │
│            │ Parse Markdown             │                  │
│            │ → docs/data.json          │                  │
│            │ Commit GitHub              │                  │
│            └────────────┬───────────────┘                  │
│                         ↓                                   │
│            ┌────────────────────────────┐                  │
│            │ 6. Résumé final           │                  │
│            │                            │                  │
│            │ Statistiques               │                  │
│            │ Pipeline OK                │                  │
│            └────────────────────────────┘                  │
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
│   ├── agent_recherche_ia.py       # [ACTIF] Recherche IA (GPT-4 Turbo + web_search)
│   ├── agent_recherche_news.py     # [ACTIF] Recherche News (GPT-4 Turbo + web_search)
│   ├── agent_synthese_ia_v2.py     # [ACTIF] Synthèse IA (GPT-4 Turbo)
│   ├── agent_synthese_news_v2.py   # [ACTIF] Synthèse News (GPT-4 Turbo)
│   ├── agent_validateur_markdown.py # Validation Markdown
│   ├── agent_generateur_json.py    # Générateur data.json
│   │
│   ├── agent_collecteur_ia.py      # [INACTIF] Ancien système Tavily
│   ├── agent_collecteur_news.py    # [INACTIF] Ancien système Tavily
│   ├── agent_synthese_ia.py        # [INACTIF] Ancienne synthèse
│   ├── agent_synthese_news.py      # [INACTIF] Ancienne synthèse
│   ├── deep_research_ia.py         # [INACTIF] Ancien Deep Research
│   └── deep_research_news.py       # [INACTIF] Ancien Deep Research
│
├── .github/workflows/
│   ├── veille-openai-complete.yml  # [ACTIF] Workflow 4-agents
│   ├── deep-research-daily.yml     # [INACTIF] Ancien workflow Deep Research
│   └── veille-quotidienne.yml      # [INACTIF] Ancien workflow Tavily
│
├── docs/
│   ├── index.html                  # Frontend React
│   ├── data.json                   # Données structurées
│   └── markdown/
│       ├── VeilleIA.md             # Markdown IA
│       └── VeilleNews.md           # Markdown News
│
├── README.md                       # Ce fichier
├── ARCHITECTURE_4_AGENTS.md        # Documentation architecture 4-agents
└── requirements.txt                # Dépendances Python
```

---

## 🛠️ Technologies

- **Backend** : Python 3.11+
- **LLM** : OpenAI GPT-4 Turbo (`gpt-4-turbo-preview`)
- **Recherche Web** : Capacité `web_search` native ChatGPT
- **Storage** : Google Drive API
- **Frontend** : React 18, Babel, Marked.js
- **Hosting** : GitHub Pages
- **CI/CD** : GitHub Actions

---

## 🔐 Secrets GitHub requis

```
OPENAI_API_KEY              # Clé API OpenAI (GPT-4 Turbo)
GOOGLE_DRIVE_CREDENTIALS    # JSON service account Google Drive
GOOGLE_DRIVE_FOLDER_ID      # ID du dossier Google Drive
```

**Note** : `TAVILY_API_KEY` et `ANTHROPIC_API_KEY` ne sont plus utilisés

---

## 🎯 Profil du lecteur

Cadre supérieur, ingénieur, basé à Nantes. Centres d'intérêt :

- **IA/LLM** : Modèles de langage, recherche, open source, régulation, startups
- **Actualités** : Politique, économie, international, écologie
- **Sports maritimes** : Voile, course au large, surf, kitesurf, wingfoil
- **Local** : Nantes, Bretagne, Pays de Loire, Belle-Île-en-Mer

---

## 📅 Exécution

- **Fréquence** : Quotidienne à 6h00 (Paris)
- **Format** : Hebdomadaire (cumul de la semaine)
- **Mise à jour** : Automatique (workflow → GitHub → GitHub Pages)
- **Durée** : ~5-8 minutes par exécution

---

## 📊 Monitoring

### GitHub Actions

- **Workflow actif** : "Veille OpenAI Complète"
- **Logs** : Disponibles dans Actions → Dernier run
- **Jobs** : 6 jobs séquentiels (2 parallèles au début)

### Métriques clés

- ✅ Taille de `data.json` : ~20-50 KB
- ✅ Nombre de sujets IA : 6 principaux + 15-20 autres
- ✅ Nombre de sujets News : 6 principaux + 15-20 autres
- ✅ Coût quotidien : ~0.36€
- ✅ Temps d'exécution : 5-8 min

---

## 🔧 Maintenance

### Tests locaux

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Tester Recherche IA
export OPENAI_API_KEY="sk-..."
python agents/agent_recherche_ia.py

# 3. Tester Synthèse IA (nécessite recherche_ia_brute.json)
export GOOGLE_DRIVE_CREDENTIALS='{"type":"service_account",...}'
export GOOGLE_DRIVE_FOLDER_ID="1xxx"
python agents/agent_synthese_ia_v2.py

# 4. Tester Recherche News
python agents/agent_recherche_news.py

# 5. Tester Synthèse News
python agents/agent_synthese_news_v2.py

# 6. Tester le générateur JSON
python agents/agent_generateur_json.py

# 7. Vérifier data.json
cat docs/data.json | python -m json.tool

# 8. Servir le site localement
cd docs
python -m http.server 8000
# Ouvrir http://localhost:8000
```

### Dépannage

**Workflow échoue** :
- Vérifier les secrets GitHub (Settings → Secrets)
- Consulter les logs du workflow (chaque job a ses logs)
- Vérifier les quotas OpenAI
- Vérifier connectivité web_search

**Site n'affiche rien** :
- Ouvrir la console (F12)
- Vérifier que `data.json` est accessible
- Vérifier le format JSON (validateur en ligne)

**Données manquantes** :
- Vérifier les fichiers Markdown sur Google Drive
- Relancer le workflow manuellement
- Consulter les logs du générateur JSON (Job 5)

**Recherche web ne fonctionne pas** :
- Vérifier que GPT-4 Turbo a accès à web_search
- Consulter les logs des agents de recherche (Jobs 1.1 et 2.1)
- Vérifier les URLs des sources institutionnelles

---

## 📚 Documentation

- **ARCHITECTURE_4_AGENTS.md** : Documentation complète architecture 4-agents
- **DEEP_RESEARCH_MIGRATION.md** : Historique migration Deep Research
- **MIGRATION_COMPLETE.md** : Historique migration Anthropic → OpenAI

---

## 🎉 Migration 4-agents ChatGPT-4 Turbo terminée

**✅ Statut** : Production stable (février 2026)  
**✅ Architecture** : 4-agents GPT-4 Turbo (Recherche + Synthèse)  
**✅ Qualité** : Excellente (analyse approfondie avec divergences)  
**✅ Sources** : Institutionnelles (IA) + Presse référence (News)  
**✅ Budget** : ~0.36€/jour (~21.60€ jusqu'à fin mars)

---

## 🤝 Contribution

Projet personnel de Nicolas Liziard.

---

## 📄 Licence

Tous droits réservés.

---

## 📧 Contact

GitHub : [@nliziard-ops](https://github.com/nliziard-ops)

---

*Dernière mise à jour : 01 février 2026 - Migration Architecture 4-agents ChatGPT-4 Turbo*
