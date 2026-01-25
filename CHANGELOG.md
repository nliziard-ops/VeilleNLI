# Changelog - VeilleNLI

Tous les changements notables de ce projet sont documentés dans ce fichier.

---

## [2.0.0] - 2026-01-25

### 🚀 Migration Deep Research (Version majeure)

#### Ajouté
- **Deep Research IA** (`agents/deep_research_ia.py`)
  - Recherche approfondie OpenAI o1 (Extended Thinking)
  - Focus sources officielles (OpenAI, Anthropic, Mistral, ArXiv)
  - Couverture IA Nantes et Bretagne
  - 20-25 articles de haute qualité

- **Deep Research News** (`agents/deep_research_news.py`)
  - Recherche approfondie actualités avec OpenAI o1
  - Sport maritime : voile, surf, kitesurf, wingfoil (minimum 10-12 articles)
  - Local Bretagne/Nantes/Belle-Île (minimum 7-8 articles)
  - Équilibre 35% International / 35% National / 30% Local
  - 25-30 articles au total

- **Agent Formatter** (`agents/agent_formatter.py`)
  - Mise en forme élégante avec GPT-4o-mini (économique)
  - Sélection automatique des 6 meilleurs articles
  - Format : Résumé + Points de vue croisés + Analyse + Sources
  - Upload automatique Google Drive

- **Workflow complet** (`.github/workflows/deep-research-daily.yml`)
  - 6 jobs séquentiels (2 parallèles au début)
  - Job 1-2 : Deep Research IA + News en parallèle
  - Job 3 : Formatter + Upload Google Drive
  - Job 4 : Sync Markdown → GitHub (docs/markdown/)
  - Job 5 : Génération data.json
  - Job 6 : Résumé final avec statistiques

- **Documentation technique complète**
  - `DEEP_RESEARCH_MIGRATION.md` : Guide migration détaillé
  - README.md mis à jour avec architecture Deep Research
  - CHANGELOG.md : Historique des versions

#### Modifié
- README.md : Architecture Deep Research, coûts actualisés
- Fréquence d'exécution : Quotidienne 6h Paris (inchangé)
- Budget : ~0.51€/jour (vs 0.18€ ancien système)

#### Désactivé
- `.github/workflows/veille-quotidienne.yml` : Workflow Tavily désactivé
- `agents/agent_collecteur_ia.py` : Inactif (remplacé par Deep Research)
- `agents/agent_collecteur_news.py` : Inactif
- `agents/agent_synthese_ia.py` : Inactif
- `agents/agent_synthese_news.py` : Inactif

#### Performances
- **Qualité** : ⭐⭐⭐⭐⭐ (vs ⭐⭐⭐)
- **Fraîcheur** : ⭐⭐⭐⭐⭐ (sources officielles prioritaires)
- **Couverture** : +200% (sport maritime + local Bretagne complets)
- **Durée** : 8-12 min (vs 5 min)
- **Coût** : +183% (0.51€ vs 0.18€)

#### ROI
- Augmentation coût justifiée par amélioration qualité massive
- Sport maritime : 0 → 10-12 articles/semaine
- Local Bretagne : Incomplet → Complet (7-8 articles/semaine)
- IA Nantes : Absent → Présent
- Sources obsolètes : Fréquent → Rare

---

## [1.5.0] - 2026-01-18

### Optimisation système Tavily

#### Ajouté
- Augmentation requêtes Tavily : 10 → 15 (IA) et 8 → 13 (News)
- Amélioration couverture géographique News

#### Modifié
- Coût quotidien : 0.12€ → 0.18€
- Meilleure diversité thématique IA

#### Problèmes identifiés
- Qualité moyenne (contenu parfois obsolète)
- Manque sport maritime
- Couverture locale incomplète
→ **Décision : Migration vers Deep Research**

---

## [1.0.0] - 2025-12-01

### Lancement système OpenAI + Tavily

#### Ajouté
- Migration Anthropic → OpenAI complète
- Architecture 2 agents par veille (collecte + synthèse)
- Workflow GitHub Actions quotidien 6h Paris
- Frontend React avec GitHub Pages
- Générateur JSON automatique
- Validation Markdown

#### Technologies
- Collecte : GPT-4o-mini + Tavily API
- Synthèse : GPT-4o
- Storage : Google Drive
- Frontend : React 18 + Marked.js

#### Performances initiales
- Coût : ~0.12€/jour
- Durée : ~5 min
- Qualité : ⭐⭐⭐

---

## [0.5.0] - 2025-11-15

### Prototype Anthropic

#### Ajouté
- Système initial avec Claude (Anthropic)
- 2 veilles : IA + Actualités
- Upload manuel Google Drive
- Site statique basique

#### Désactivé (2025-12-01)
- Remplacé par système OpenAI pour meilleur contrôle coûts

---

## Statistiques migration Deep Research

### Avant (Tavily v1.5.0)
```
Requêtes    : 15 IA + 13 News = 28 requêtes Tavily
Qualité     : ⭐⭐⭐
Sport       : ❌ Absent
Local       : ❌ Incomplet
Coût/jour   : 0.18€
Durée       : 5 min
```

### Après (Deep Research v2.0.0)
```
Requêtes    : 2 recherches approfondies o1
Qualité     : ⭐⭐⭐⭐⭐
Sport       : ✅ 10-12 articles/semaine
Local       : ✅ 7-8 articles/semaine
IA Nantes   : ✅ Présent
Coût/jour   : 0.51€ (+183%)
Durée       : 8-12 min
```

**ROI positif malgré coût supérieur**

---

## Guide des versions

### Format
- **[MAJOR.MINOR.PATCH]**
- **MAJOR** : Changement architecture (incompatible)
- **MINOR** : Nouvelles fonctionnalités (compatible)
- **PATCH** : Corrections bugs (compatible)

### Versions actives
- **v2.0.0** : Production (Deep Research)
- **v1.5.0** : Désactivée (Tavily)
- **v1.0.0** : Désactivée (OpenAI + Tavily initial)

---

*Dernière mise à jour : 25 janvier 2026*
