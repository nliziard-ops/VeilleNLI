# Architecture et Mémoire du Projet VeilleNLI

**Date de consolidation** : 3 février 2026  
**Version** : 3.0 - Deep Research OpenAI GPT-5.2  
**Statut** : Production stable

---

## 📌 Vue d'ensemble du projet

### Mission
VeilleNLI est un système de veille automatisée qui génère quotidiennement deux rapports d'intelligence économique :

1. **Veille IA & LLM** : Actualités sur l'Intelligence Artificielle, les modèles de langage, la recherche, les startups, la régulation
2. **Veille Actualités** : Actualités générales (internationale 35%, nationale 35%, locale Bretagne 30%) avec focus sports maritimes

Le système s'exécute automatiquement **tous les jours à 6h00 (Paris)** et publie les résultats sur **GitHub Pages** : https://nliziard-ops.github.io/VeilleNLI/

### Utilisateur cible
Cadre supérieur, ingénieur, basé à Nantes/Bretagne. Centres d'intérêt :
- **IA/LLM** : Modèles, recherche, open source, régulation, startups (focus Mistral AI, Poolside, DeepSeek)
- **Local** : Nantes, Bretagne, Belle-Île-en-Mer, écosystème IA régional
- **Sports maritimes** : Voile, course au large, surf, kitesurf, wingfoil
- **Actualités** : Politique, économie, international, écologie

---

## 🏗️ Architecture technique actuelle

### Workflow principal : `deep-research-daily.yml`

Le système utilise un **pipeline en 6 étapes** avec OpenAI GPT-5.2 et GPT-4o-mini :

```
┌───────────────────────────────────────────────────────────┐
│           DEEP RESEARCH QUOTIDIEN (6h00 Paris)           │
└───────────────────────────────────────────────────────────┘

┌──────────────────────┐  ┌──────────────────────┐
│ 1. Deep Research IA  │  │ 2. Deep Research News│
│    GPT-5.2           │  │    GPT-5.2           │
│    web_search        │  │    web_search        │
│                      │  │                      │
│ Recherche live web   │  │ Recherche live web   │
│ 15-20 articles IA    │  │ 15-20 articles news  │
│                      │  │                      │
│ → research_ia.md     │  │ → research_news.md   │
└──────────┬───────────┘  └──────────┬───────────┘
           │                         │
           └────────┬────────────────┘
                    ↓
         ┌──────────────────────┐
         │ 3. Formatter         │
         │    GPT-4o-mini       │
         │                      │
         │ Fusionne + formate   │
         │ Top 6 sujets + reste │
         │                      │
         │ → VeilleIA.md       │
         │ → VeilleNews.md     │
         │ Upload Google Drive  │
         └──────────┬───────────┘
                    ↓
         ┌──────────────────────┐
         │ 4. Sync GitHub       │
         │    Python script     │
         │                      │
         │ Download Drive       │
         │ → docs/markdown/*.md │
         │ Commit GitHub        │
         └──────────┬───────────┘
                    ↓
         ┌──────────────────────┐
         │ 5. Génère JSON       │
         │    Python parsing    │
         │                      │
         │ Parse Markdown       │
         │ → docs/data.json     │
         │ Commit GitHub        │
         └──────────┬───────────┘
                    ↓
         ┌──────────────────────┐
         │ 6. Résumé final      │
         │    Statistiques      │
         └──────────────────────┘
                    ↓
         ┌──────────────────────┐
         │   GitHub Pages       │
         │   Site web public    │
         └──────────────────────┘
```

### Modèles OpenAI utilisés

| Agent | Modèle | Usage | Coût estimé |
|-------|--------|-------|-------------|
| Deep Research IA | GPT-5.2 | Recherche web + analyse | ~0.10€ |
| Deep Research News | GPT-5.2 | Recherche web + analyse | ~0.10€ |
| Formatter | GPT-4o-mini | Mise en forme élégante | ~0.04€ |
| Générateur JSON | Python pur | Parsing Markdown | 0.00€ |
| **TOTAL** | - | - | **~0.24€/jour** |

**Budget mensuel** : ~7.20€/mois (sur budget 40€/mois → **marge confortable**)

---

## 🤖 Description des agents

### 1. Deep Research IA (`deep_research_ia.py`)

**Mission** : Recherche web live sur l'actualité IA/LLM

**Modèle** : GPT-5.2 avec `web_search` natif OpenAI

**Fonctionnalités clés** :
- Recherche web **live** (pas de données cached)
- Extraction automatique des **URLs réelles** depuis les annotations de réponse
- 15-20 recherches web ciblées sur les thèmes IA
- Focus géographique : USA 50%, Europe 30%, Asie 15%, Nantes/Bretagne 5%

**Thèmes couverts** :
1. Nouveaux modèles LLM (GPT, Claude, Gemini, Llama, Mistral, DeepSeek)
2. Agents autonomes et Agentic AI
3. Multimodal AI (vision, audio, vidéo)
4. Reasoning models (o1, o3, R1, chain-of-thought)
5. Open source (Hugging Face, communauté)
6. Recherche scientifique (ArXiv, conférences)
7. Régulation et gouvernance (AI Act Europe)
8. Safety, Alignment, risques
9. Investissements et industrie
10. Hardware IA (NVIDIA, AMD, TPU, Groq)
11. Startups françaises/européennes (Mistral, Poolside)
12. **IA Nantes et Bretagne** (écosystème local, startups, événements)

**Sources prioritaires** :
- Blogs officiels : OpenAI, Anthropic, Google AI, Meta AI
- Éditeurs : Mistral AI, Hugging Face, Stability AI
- Recherche : ArXiv, Papers with Code, NeurIPS, ICML
- Médias tech : TechCrunch, The Verge, Wired, VentureBeat

**Configuration** :
```python
model="gpt-5.2"
max_output_tokens=4000
reasoning={"effort": "medium"}
tools=[{"type": "web_search"}]
timeout=600  # 10 minutes
```

**Sortie** : `research_ia.md` avec section "Sources vérifiées" (URLs réelles extraites)

---

### 2. Deep Research News (`deep_research_news.py`)

**Mission** : Recherche web live sur l'actualité générale

**Modèle** : GPT-5.2 avec `web_search` natif

**Fonctionnalités** : Identiques à Deep Research IA

**Thèmes couverts** :
1. **International** (35%) : Géopolitique, économie mondiale, conflits, diplomatie
2. **National France** (35%) : Politique, économie, société, technologie
3. **Local Bretagne/Pays de Loire** (30%) :
   - Politique locale et régionale
   - Économie et entreprises bretonnes
   - Environnement et mer
   - **Sports maritimes** : Voile, course au large, surf, kitesurf, wingfoil
   - Culture et société

**Sources prioritaires** :
- **International** : Le Grand Continent, El País, BBC, Reuters, The Guardian
- **National** : Le Figaro, Le Monde, Le Monde Diplomatique, Mediapart
- **Local** : Ouest-France, Le Télégramme, Presse-Océan
- **Sport** : Voiles et Voiliers, Tip & Shaft, Wind Magazine

**Configuration** : Identique à Deep Research IA

**Sortie** : `research_news.md` avec section "Sources vérifiées"

---

### 3. Agent Formatter (`agent_formatter.py`)

**Mission** : Transformer les recherches brutes en synthèses élégantes

**Modèle** : GPT-4o-mini-2024-07-18 (économique)

**Entrée** :
- `research_ia.md` (15-20 articles bruts)
- `research_news.md` (15-20 articles bruts)

**Traitement** :
- Sélectionne les **6 articles les plus pertinents** (score 8-10)
- Génère une synthèse structurée avec :
  - Métadonnées YAML (agent, date, catégorie)
  - Introduction (4-5 lignes)
  - 6 sujets principaux détaillés (résumé, points de vue croisés, analyse, sources)
  - Section "Autres sujets" (format compact pour les articles restants)
  - Synthèse finale (points clés, divergences, signaux faibles)
- Style sobre et professionnel (ZÉRO emoji)

**Sortie** :
- `VeilleIA.md` → Upload Google Drive
- `VeilleNews.md` → Upload Google Drive

**Configuration** :
```python
model="gpt-4o-mini-2024-07-18"
temperature=0.7
max_tokens=8000
```

**Budget** : ~0.04€ (2 documents)

---

### 4. Agent Générateur JSON (`agent_generateur_json.py`)

**Mission** : Parser les Markdown et générer `data.json` pour le frontend

**Type** : Script Python pur (pas de LLM)

**Entrée** :
- `VeilleIA.md` (depuis Google Drive)
- `VeilleNews.md` (depuis Google Drive)

**Fonctionnalités** :
- Parsing avancé du Markdown :
  - Extraction métadonnées YAML (front matter)
  - Détection du titre principal et édition
  - Extraction de l'introduction
  - Parsing des sections (## niveau 2)
  - **Détection intelligente de "Autres sujets"** (stop parsing à cette section)
  - Extraction des sous-sections (### niveau 3) : Résumé, Points de vue, Sources
  - Génération d'icônes adaptées par catégorie

**Pattern critique** :
```python
# Regex pour détecter "Autres sujets" / "Autres actualités" (TOUTES variantes)
autres_pattern = re.compile(r'^##\s+Autres\s+(sujet|sujets|actualité|actualités)', re.IGNORECASE)
```

**Sortie** : `docs/data.json` (structure JSON pour React)

**Structure JSON** :
```json
{
  "version": "2.0",
  "date_generation": "2026-02-03T06:30:00",
  "veilles": {
    "ia": {
      "metadata": {"agent": "...", "date": "...", "categorie": "..."},
      "titre": "Veille IA & LLM – Semaine...",
      "edition": "Édition Reasoning",
      "introduction": "...",
      "sujets_importants": [/* 6 sujets principaux */],
      "sujets_secondaires": [/* Autres sujets */],
      "points_cles": [/* Points clés synthèse finale */]
    },
    "news": {/* Même structure */}
  }
}
```

**Budget** : Gratuit (pas d'API LLM)

---

## 🔐 Configuration et secrets

### Secrets GitHub requis

Le workflow nécessite **3 secrets** configurés dans Settings → Secrets and variables → Actions :

#### 1. `OPENAI_API_KEY`
- **Format** : `sk-proj-...`
- **Usage** : Deep Research IA/News + Formatter
- **Permissions** : Accès GPT-5.2 et GPT-4o-mini

#### 2. `GOOGLE_DRIVE_CREDENTIALS`
- **Format** : JSON complet du service account Google Cloud
- **Usage** : Upload/Download Markdown
- **Permissions** :
  - `https://www.googleapis.com/auth/drive` (lecture/écriture)
  - Accès au dossier spécifié par `GOOGLE_DRIVE_FOLDER_ID`

**Exemple de structure** :
```json
{
  "type": "service_account",
  "project_id": "...",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "...",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "..."
}
```

#### 3. `GOOGLE_DRIVE_FOLDER_ID`
- **Format** : `1abc...xyz` (ID extrait de l'URL du dossier)
- **Usage** : Stockage intermédiaire des Markdown finaux
- **Exemple** : Si URL = `https://drive.google.com/drive/folders/1abc123xyz`, alors ID = `1abc123xyz`

---

## 📁 Structure du repository

### Fichiers actifs (utilisés quotidiennement)

```
VeilleNLI/
├── .github/workflows/
│   └── deep-research-daily.yml        # [ACTIF] Workflow quotidien 6h00
│
├── agents/
│   ├── deep_research_ia.py            # [ACTIF] Recherche IA GPT-5.2
│   ├── deep_research_news.py          # [ACTIF] Recherche News GPT-5.2
│   ├── agent_formatter.py             # [ACTIF] Mise en forme GPT-4o-mini
│   └── agent_generateur_json.py       # [ACTIF] Parser Python
│
├── docs/
│   ├── index.html                     # Frontend React
│   ├── data.json                      # Données structurées (généré)
│   └── markdown/
│       ├── VeilleIA.md                # Markdown IA (synced)
│       └── VeilleNews.md              # Markdown News (synced)
│
├── README.md                          # Documentation utilisateur
├── DOCUMENTATION_TECHNIQUE.md         # Documentation technique détaillée
├── ARCHITECTURE_MEMOIRE.md            # Ce fichier (état du système)
└── requirements.txt                   # Dépendances Python
```

### Fichiers inactifs (anciens systèmes, non utilisés)

```
├── .github/workflows/
│   ├── list-models.yml                # [UTIL] Test modèles OpenAI
│   ├── update-data.yml                # [VIDE] Placeholder
│   ├── veille-openai-complete.yml     # [INACTIF] Ancien workflow 4-agents
│   └── veille-quotidienne.yml         # [INACTIF] Ancien workflow Tavily
│
└── agents/
    ├── agent_recherche_ia.py          # [INACTIF] Ancien système GPT-4 Turbo
    ├── agent_recherche_news.py        # [INACTIF] Ancien système GPT-4 Turbo
    ├── agent_synthese_ia_v2.py        # [INACTIF] Ancienne synthèse
    ├── agent_synthese_news_v2.py      # [INACTIF] Ancienne synthèse
    ├── agent_collecteur_ia.py         # [INACTIF] Ancien système Tavily
    ├── agent_collecteur_news.py       # [INACTIF] Ancien système Tavily
    ├── agent_synthese_ia.py           # [INACTIF] Ancienne version
    ├── agent_synthese_news.py         # [INACTIF] Ancienne version
    └── agent_validateur_markdown.py   # [INACTIF] Validation non utilisée
```

---

## 📊 Historique des architectures

### Version 1.0 : Système Tavily (Septembre 2025)

**Stack** : ChatGPT-4 Turbo + Tavily API  
**Coût** : ~0.18€/jour  
**Problèmes** :
- Qualité des sources variable (agrégateurs secondaires)
- Contenu parfois superficiel
- Dépendance API externe (Tavily)

### Version 2.0 : Architecture 4-agents (Décembre 2025)

**Stack** : ChatGPT-4 Turbo (Recherche + Synthèse) sans Tavily  
**Coût** : ~0.36€/jour  
**Améliorations** :
- Recherche web native GPT-4 Turbo
- Sources institutionnelles directes
- Synthèse avec divergences entre sources
- 4 agents spécialisés (Recherche IA, Recherche News, Synthèse IA, Synthèse News)

**Limites** :
- GPT-4 Turbo moins performant que GPT-5.2 pour la recherche
- Coût légèrement élevé (4 appels LLM)

### Version 3.0 : Deep Research GPT-5.2 (Février 2026) ⭐ ACTUELLE

**Stack** : GPT-5.2 (Recherche) + GPT-4o-mini (Formatter)  
**Coût** : ~0.24€/jour (**33% moins cher que v2.0**)  
**Avantages** :
- **GPT-5.2 Extended Thinking** : Recherche web approfondie avec raisonnement étendu
- **Extraction automatique des URLs réelles** depuis les annotations
- **GPT-4o-mini pour la mise en forme** : 10x moins cher que GPT-4 Turbo
- **Architecture simplifiée** : 2 agents de recherche + 1 formatter (au lieu de 4 agents)
- **Qualité supérieure** : Analyse plus profonde, sources plus pertinentes

**Changements majeurs** :
- Migration de `client.chat.completions.create()` vers `client.responses.create()`
- Ajout du paramètre `reasoning={"effort": "medium"}`
- Extraction des citations depuis `response.output[].content[].annotations`
- Section "Sources vérifiées" automatiquement injectée dans le Markdown

---

## 🎯 Décisions techniques clés

### 1. Choix de GPT-5.2 pour la recherche

**Pourquoi GPT-5.2 ?**
- Extended Thinking : Raisonnement étendu pour analyses approfondies
- Web search natif performant (pas besoin Tavily API)
- Annotations avec URLs réelles (pas d'hallucinations d'URLs)
- Qualité supérieure aux versions précédentes

**Alternatives considérées** :
- ❌ GPT-4 Turbo : Moins performant, coût similaire
- ❌ Claude Sonnet 3.5 : Pas de web search natif, coût plus élevé
- ❌ Gemini 1.5 Pro : Moins mature, API moins stable

### 2. Choix de GPT-4o-mini pour la mise en forme

**Pourquoi GPT-4o-mini ?**
- **10x moins cher** que GPT-4 Turbo ($0.15/$0.60 vs $10/$30 par 1M tokens)
- Qualité suffisante pour la mise en forme (pas de recherche complexe)
- Rapide (latence faible)

**Tarification** :
- Input : $0.15 / 1M tokens
- Output : $0.60 / 1M tokens

### 3. Parsing Python pur pour le JSON

**Pourquoi pas de LLM ?**
- Parsing déterministe : Pas d'hallucinations possibles
- Gratuit : Pas de coût API
- Rapide : Exécution en quelques secondes
- Contrôle total : Debug facile avec regex et logs

**Risque** :
- Fragile si format Markdown change → Mais format stable depuis v2.0

### 4. Stockage intermédiaire sur Google Drive

**Pourquoi Google Drive ?**
- Visualisation facile des Markdown finaux
- Backup automatique (versionning Drive)
- Accès manuel possible pour vérification
- API stable et gratuite

**Alternative considérée** :
- ❌ Artifacts GitHub : Expiration après 1 jour, pas d'accès facile

---

## 🔍 Points d'attention et limites connues

### 1. Parsing Markdown fragile

**Problème** : Le générateur JSON repose sur des patterns regex pour détecter les sections

**Risque** : Si GPT-4o-mini change le format de sortie (ex: "## Autres thèmes" au lieu de "## Autres sujets"), le parsing peut échouer

**Mitigation** :
- Pattern regex robuste avec variantes : `r'^##\s+Autres\s+(sujet|sujets|actualité|actualités)'`
- Logs détaillés pour debug
- Tests réguliers du générateur JSON

### 2. Coûts OpenAI imprévisibles

**Problème** : Si GPT-5.2 génère plus de tokens que prévu (recherche très longue), coût peut augmenter

**Risque** : Dépasser le budget de 40€/mois

**Mitigation** :
- `max_output_tokens` limité à 4000 (Deep Research) et 8000 (Formatter)
- Monitoring quotidien : https://platform.openai.com/usage
- Alertes si coût > 0.35€/jour

### 3. Quotas OpenAI

**Problème** : Si quota OpenAI dépassé, workflow échoue

**Risque** : Pas de veille générée ce jour-là

**Mitigation** :
- Vérifier les quotas régulièrement
- Plan Tier 1+ recommandé (5000 RPM minimum)

### 4. Web search peut être lent

**Problème** : GPT-5.2 avec web search peut prendre 2-4 minutes par agent

**Risque** : Timeout du workflow (15 minutes par job)

**Mitigation** :
- Timeout généreux : 15 minutes pour Deep Research
- `reasoning.effort = "medium"` (pas "high" qui serait plus lent)

---

## 📈 Métriques de succès

### Qualité du contenu
- ✅ 6 sujets principaux détaillés (résumé + points de vue + sources)
- ✅ 15-20 autres sujets en format compact
- ✅ URLs réelles extraites (pas d'hallucinations)
- ✅ Sources primaires privilégiées (blogs officiels, ArXiv, presse référence)
- ✅ Divergences entre sources identifiées
- ✅ Signaux faibles détectés

### Performance technique
- ✅ Coût quotidien : ~0.24€ (sous budget 40€/mois)
- ✅ Temps d'exécution : 5-8 minutes (workflow complet)
- ✅ Taux de succès : >95% (workflows sans erreur)
- ✅ Taille `data.json` : 20-50 KB (optimal)

### Couverture géographique
- ✅ IA : USA 50%, Europe 30%, Asie 15%, Nantes/Bretagne 5%
- ✅ News : International 35%, National 35%, Local 30%

### Couverture thématique
- ✅ IA : 12 thèmes couverts (modèles, agents, multimodal, reasoning, etc.)
- ✅ News : Sports maritimes bien représentés (voile, surf, kitesurf)
- ✅ Local : Nantes, Bretagne, Belle-Île-en-Mer

---

## 🚀 Prochaines étapes

### Court terme (1-2 semaines)
- [ ] Ajouter des tests unitaires (pytest) pour le générateur JSON
- [ ] Créer un dashboard de monitoring (coûts, succès, temps)
- [ ] Documenter les patterns regex critiques

### Moyen terme (1-3 mois)
- [ ] Migrer vers GPT-5.3 si disponible (meilleure qualité)
- [ ] Implémenter un système de cache (réduire recherches doublons)
- [ ] Ajouter des notifications (email/Slack) en cas d'échec

### Long terme (6+ mois)
- [ ] Développer une API REST pour accès programmatique aux veilles
- [ ] Créer une app mobile (React Native)
- [ ] Ajouter des fonctionnalités de personnalisation utilisateur
- [ ] Implémenter un système de recommandations (ML)

---

## 📚 Ressources et documentation

### Documentation OpenAI
- GPT-5.2 Extended Thinking : https://platform.openai.com/docs/guides/extended-thinking
- GPT-4o-mini : https://platform.openai.com/docs/models/gpt-4o-mini
- Web search tool : https://platform.openai.com/docs/guides/web-search

### Documentation Google Drive API
- Service Accounts : https://cloud.google.com/iam/docs/service-accounts
- Python Quickstart : https://developers.google.com/drive/api/quickstart/python

### Documentation GitHub
- GitHub Actions : https://docs.github.com/en/actions
- GitHub Pages : https://docs.github.com/en/pages
- Secrets : https://docs.github.com/en/actions/security-guides/encrypted-secrets

---

**Dernière mise à jour** : 3 février 2026  
**Mainteneur** : Nicolas Liziard (@nliziard-ops)  
**Version** : 3.0 - Deep Research OpenAI GPT-5.2
