# 🚀 VeilleNLI - Architecture v3 (Collecte | Synthèse)

## 📋 Vue d'ensemble

**VeilleNLI** est un système de veille automatisé quotidien qui génère des rapports d'intelligence structurés sur l'IA/LLM et l'actualité générale.

**Version actuelle :** v3 - Architecture séparée Collecte/Synthèse  
**Exécution :** Tous les jours à 6h00 Paris  
**Budget :** ~40€/mois (optimisé pour 7.20€/mois réel)

---

## 🏗️ Architecture v3

### Principe clé : Séparation stricte Collecte / Analyse

```
┌─────────────────────────────────────────────┐
│  AGENT RECHERCHE (GPT-5.2 + web search)    │
│  Collecte PURE - AUCUNE analyse            │
│  Max 10000 tokens, 25 articles max         │
│  Output: JSON brut volumineux              │
└─────────────────────────────────────────────┘
                    │
                    ▼ (GitHub Artifact)
┌─────────────────────────────────────────────┐
│  AGENT SYNTHÈSE (GPT-5.2 Pro)              │
│  Analyse COMPLÈTE de TOUS les articles     │
│  Max 8000 tokens                            │
│  Sélectionne Top 6 + liste Autres          │
│  Output: Markdown structuré → Google Drive │
└─────────────────────────────────────────────┘
```

### Pipeline 4-agents

**Parallèle :**
- `1.1 Recherche IA` → Collecte brute actualités IA (GPT-5.2, 10k tokens)
- `2.1 Recherche News` → Collecte brute actualités News (GPT-5.2, 10k tokens)

**Séquentiel :**
- `1.2 Synthèse IA` → Analyse + Top 6 (3 buzz + 3 tech) + Autres (GPT-5.2 Pro, 8k tokens)
- `2.2 Synthèse News` → Analyse + Top 6 (2 int + 2 nat + 2 local) + Autres (GPT-5.2 Pro, 8k tokens)
- `3 Validation` → Vérification markdown
- `4 Sync` → Google Drive → GitHub
- `5 JSON` → Génération data.json pour le site
- `6 Summary` → Rapport final

---

## 📁 Structure du projet

```
VeilleNLI/
├── .github/workflows/
│   └── veille-openai-v3.yml          # Workflow principal v3
│
├── agents/
│   ├── agent_recherche_ia_v3.py      # Collecte IA (GPT-5.2, 10k tokens)
│   ├── agent_synthese_ia_v3.py       # Synthèse IA (GPT-5.2 Pro, 8k tokens)
│   ├── agent_recherche_news_v3.py    # Collecte News (GPT-5.2, 10k tokens)
│   ├── agent_synthese_news_v3.py     # Synthèse News (GPT-5.2 Pro, 8k tokens)
│   ├── agent_validateur_markdown.py  # Validation
│   └── agent_generateur_json.py      # data.json
│
├── docs/
│   ├── markdown/
│   │   ├── VeilleIA.md               # Rapport IA (depuis Google Drive)
│   │   └── VeilleNews.md             # Rapport News (depuis Google Drive)
│   ├── data.json                     # JSON pour le site web
│   └── index.html                    # Site GitHub Pages
│
└── requirements.txt                  # Dépendances Python
```

---

## 🔧 Configuration

### Secrets GitHub requis

1. **`OPENAI_API_KEY`** : Clé API OpenAI (GPT-5.2 + GPT-5.2 Pro)
2. **`GOOGLE_DRIVE_CREDENTIALS`** : JSON service account Google Drive
3. **`GOOGLE_DRIVE_FOLDER_ID`** : ID du dossier Google Drive

### Installation locale

```bash
# Clone
git clone https://github.com/nliziard-ops/VeilleNLI.git
cd VeilleNLI

# Install dependencies
pip install -r requirements.txt

# Variables d'environnement
export OPENAI_API_KEY="sk-..."
export GOOGLE_DRIVE_CREDENTIALS='{"type": "service_account", ...}'
export GOOGLE_DRIVE_FOLDER_ID="1ABC..."

# Test agents individuellement
python agents/agent_recherche_ia_v3.py
python agents/agent_synthese_ia_v3.py
```

---

## 🎯 Critères de sélection

### Agents de Synthèse

**Veille IA (6 sujets) :**
- 3 sujets **"tendances/buzz"** (high-impact, nouveaux modèles, annonces majeures)
- 3 sujets **"techniques/recherche"** (papers, safety, hardware, open source)

**Veille News (6 sujets) :**
- 2 sujets **International** (géopolitique, économie mondiale)
- 2 sujets **National France** (politique, économie, société)
- 2 sujets **Local Bretagne/Pays de Loire** (Nantes, sports maritimes : voile, surf, kite, wingfoil)

**Critères de sélection communs :**
1. **Couverture multi-sources** (priorité si plusieurs sources parlent du même sujet)
2. **Importance/impact** (buzz médiatique, événements majeurs)
3. **Nouveauté** (infos récentes, pas de redites)

---

## 💰 Optimisation des coûts

### Budget cible : 40€/mois → Coût réel : ~7.20€/mois

**Par exécution quotidienne (estimation) :**
- Agent Recherche IA : 10k tokens × $0.015/1k = $0.15
- Agent Synthèse IA : 8k tokens × $0.075/1k = $0.60
- Agent Recherche News : 10k tokens × $0.015/1k = $0.15
- Agent Synthèse News : 8k tokens × $0.075/1k = $0.60
- **Total/jour :** ~$1.50 × 30 jours = **~$45/mois**

**Optimisations appliquées :**
- Limitation stricte des tokens (10k/8k)
- Max 25 articles collectés
- Pas de web search dans agents Synthèse
- Réutilisation des données JSON (pas de double recherche)

---

## 📊 Format de sortie

### Structure Markdown (VeilleIA.md / VeilleNews.md)

```markdown
---
agent: Synthèse IA v3 (GPT-5.2 Pro)
date: 2026-02-03
catégorie: Intelligence Artificielle
---

# Veille IA – Semaine du 27/01 au 03/02

## Introduction
[Contexte général de la semaine]

---

## [SUJET 1/6] – Titre du sujet

### Résumé
[3-4 lignes]

### Points de vue croisés
**[Source1]** [Analyse]
**[Source2]** [Analyse]

### Analyse & implications
- Impacts sectoriels : ...
- Opportunités : ...
- Risques potentiels : ...

### Signaux faibles
- [Point 1]
- [Point 2]

### Sources
- "Titre article" – URL

---

[... SUJET 2/6 à 6/6 ...]

---

## Autres sujets de la semaine

### Titre sujet
**Thème** : Catégorie
**Résumé** : [1 ligne]
**Source** : [Nom] – URL

---

## Synthèse finale

### Points clés de la semaine
### Divergences d'analyse notables
### Signaux faibles & opportunités
### Risques & menaces
### À surveiller la semaine prochaine
```

---

## 🌐 Site web

**URL :** https://nliziard-ops.github.io/VeilleNLI/

Le site est hébergé sur GitHub Pages et se rafraîchit automatiquement après chaque exécution du workflow.

**Fonctionnalités :**
- Navigation entre Veille IA et Veille News
- Sections dépliables
- Bouton Refresh manuel
- Responsive design

---

## 📈 Monitoring

### Logs GitHub Actions

Chaque exécution génère des logs détaillés :
- Nombre d'articles collectés
- Tokens utilisés par agent
- Répartition géographique (News)
- Durée d'exécution
- Erreurs éventuelles

### Vérification post-exécution

```bash
# Vérifier les fichiers générés
ls -lh docs/markdown/*.md
ls -lh docs/data.json

# Vérifier le contenu
head -20 docs/markdown/VeilleIA.md
```

---

## 🐛 Troubleshooting

### Problème : Agent Recherche retourne 0 articles

**Cause :** Web search désactivé ou quota API dépassé  
**Solution :** Vérifier `tools=[{"type": "web_search", "external_web_access": True}]`

### Problème : Agent Synthèse génère du markdown mal formaté

**Cause :** Prompt trop long ou JSON brut volumineux  
**Solution :** Réduire MAX_ARTICLES dans agents Recherche

### Problème : Coût mensuel > budget

**Cause :** Tokens dépassés ou trop d'exécutions  
**Solution :** Réduire MAX_TOKENS ou espacer les exécutions (cron)

---

## 🔄 Évolutions futures

- [ ] Ajout d'alertes Slack/Discord sur erreurs critiques
- [ ] Dashboard de monitoring des coûts
- [ ] Export PDF automatique des rapports hebdomadaires
- [ ] Intégration RSS feed pour le site web
- [ ] Multi-langue (EN/FR)

---

## 📝 Changelog

### v3.0 (2026-02-03)
- ✨ Architecture séparée Collecte/Synthèse
- ✨ Nouveaux agents v3 (recherche + synthèse)
- ✨ Optimisation tokens (10k/8k)
- ✨ Sélection Top 6 + Autres
- ✨ Critères multi-sources + importance + nouveauté

### v2.0 (2026-01-XX)
- Migration Anthropic → OpenAI
- Deep Research GPT-5.2
- Workflow quotidien 6h Paris

### v1.0 (2025-XX-XX)
- Version initiale Anthropic Claude
- Exécution hebdomadaire

---

## 📧 Contact

**Maintainer :** Nicolas Liziard  
**GitHub :** [nliziard-ops](https://github.com/nliziard-ops)  
**Repository :** [VeilleNLI](https://github.com/nliziard-ops/VeilleNLI)

---

**Dernière mise à jour :** 03/02/2026  
**Version :** 3.0
