# Architecture 4-agents ChatGPT-4 Turbo

**Date de création** : 01 février 2026  
**Auteur** : Nicolas Liziard  
**Statut** : Production active

---

## 🎯 Objectifs de l'architecture

### Problèmes résolus

1. **Séparation collecte/analyse** : Les anciens agents mélangeaient recherche et analyse
2. **Contrôle qualité sources** : Accès direct aux sites institutionnels vs API Tavily
3. **Analyse approfondie** : Synthèse détaillée avec divergences entre sources
4. **Structure claire** : 6 sujets prioritaires + autres en liste compacte
5. **Coût optimisé** : GPT-4 Turbo au lieu de GPT-4 standard

### Principes fondamentaux

- **Agent 1 & 2 (Recherche)** : Collecte PURE sans interprétation
- **Agent 3 & 4 (Synthèse)** : Analyse APPROFONDIE avec divergences
- **Parallélisation** : IA et News en même temps (gain de temps)
- **Sources vérifiables** : URLs complètes obligatoires
- **Budget maîtrisé** : Token limits strictes

---

## 🔍 Agent 1 - Recherche Web IA

### Rôle

Collecte factuelle d'informations depuis sites institutionnels IA, SANS analyse ni interprétation.

### Modèle

**GPT-4 Turbo** (`gpt-4-turbo-preview`)
- Température : 0.1 (très factuel)
- Max tokens : 8000
- Capacité : `web_search` native

### Sources institutionnelles

1. **Anthropic** : https://www.anthropic.com (Claude)
2. **OpenAI** : https://openai.com (GPT)
3. **Mistral AI** : https://mistral.ai (France)
4. **DeepSeek** : https://www.deepseek.com (Chine)
5. **The Hacker News** : https://thehackernews.com
6. **DeepLearning.AI** : https://www.deeplearning.ai
7. **Google AI** : https://ai.google (ajout institutionnel)
8. **NVIDIA AI** : https://www.nvidia.com/en-us/ai/ (ajout institutionnel)

### Format de sortie

Fichier JSON : `recherche_ia_brute.json`

```json
{
  "articles": [
    {
      "id": "abc123",
      "categorie": "Nouveaux modèles LLM",
      "titre": "Titre exact de l'article",
      "resume_court": "Résumé factuel en 2-3 lignes",
      "synthese_complete": "Contenu factuel complet : qui, quoi, quand, où, comment",
      "source": "OpenAI",
      "url": "https://openai.com/blog/article",
      "date_publication": "2026-02-01"
    }
  ],
  "periode": {
    "debut": "2026-01-25",
    "fin": "2026-02-01"
  },
  "sources_consultees": ["Anthropic", "OpenAI", "..."],
  "date_collecte": "2026-02-01",
  "model_utilise": "gpt-4-turbo-preview",
  "agent": "Recherche IA"
}
```

### Catégories

- Nouveaux modèles LLM
- Agents autonomes
- Multimodal (vision, audio, vidéo)
- Reasoning (o1, o3, R1)
- Open source
- Recherche scientifique
- Régulation & gouvernance
- Safety & Alignment
- Industrie & investissements
- Hardware (GPU, TPU)
- France & Europe
- Asie (Chine, Japon, etc.)

### Consignes strictes

✅ **À FAIRE** :
- Extraire UNIQUEMENT les faits vérifiables
- Citer les sources exactes
- Respecter les chiffres et dates
- Retranscrire fidèlement le contenu

❌ **À NE PAS FAIRE** :
- Interpréter les faits
- Porter un jugement
- Spéculer sur les impacts
- Ajouter des opinions personnelles

### Coût estimé

~5000 tokens (prompt + completion) × 0.01$/1K = **~0.06€**

---

## 🔍 Agent 2 - Recherche Web News

### Rôle

Collecte factuelle depuis presse nationale/internationale/locale, SANS analyse ni interprétation.

### Modèle

**GPT-4 Turbo** (`gpt-4-turbo-preview`)
- Température : 0.1 (très factuel)
- Max tokens : 8000
- Capacité : `web_search` native

### Sources presse

**INTERNATIONAL** :
1. **Le Grand Continent** : https://legrandcontinent.eu/fr/
2. **El País** : https://elpais.com/
3. **BBC News** : https://www.bbc.com/news
4. **Reuters** : https://www.reuters.com

**NATIONAL FRANCE** :
5. **Le Figaro** : https://www.lefigaro.fr/
6. **Le Monde** : https://www.lemonde.fr/
7. **Le Monde Diplomatique** : https://www.monde-diplomatique.fr/

**LOCAL BRETAGNE/PAYS DE LOIRE** :
8. **Ouest-France** : https://www.ouest-france.fr/
9. **Le Télégramme** : https://www.letelegramme.fr/

### Distribution géographique cible

- **35% International** : Géopolitique, économie mondiale, crises
- **35% National** : France (politique, économie, société)
- **30% Local** : Bretagne/Pays de Loire (politique locale, sports maritimes, mer)

### Format de sortie

Fichier JSON : `recherche_news_brute.json`

```json
{
  "articles": [
    {
      "id": "xyz789",
      "categorie": "Géopolitique",
      "zone_geo": "International",
      "titre": "Titre exact",
      "resume_court": "Résumé factuel 2-3 lignes",
      "synthese_complete": "Contenu factuel complet",
      "source": "Le Monde",
      "url": "https://lemonde.fr/article",
      "date_publication": "2026-02-01"
    }
  ],
  "periode": {...},
  "repartition": {
    "international": 8,
    "national": 7,
    "local": 6
  },
  "sources_consultees": ["Le Monde", "Ouest-France", "..."]
}
```

### Catégories

**INTERNATIONAL** :
- Géopolitique
- Économie mondiale
- Environnement

**FRANCE** :
- Politique nationale
- Économie France
- Société

**LOCAL BRETAGNE/PAYS DE LOIRE** :
- Politique locale
- Économie régionale
- Sports maritimes (voile, surf, kitesurf, wingfoil)
- Mer & littoral
- Culture Bretagne

### Focus local

- Nantes
- Brest
- Belle-Île-en-Mer
- Le Palais
- Sports maritimes (voile, surf, kitesurf, wingfoil, compétitions)

### Coût estimé

~5000 tokens × 0.01$/1K = **~0.06€**

---

## 🧠 Agent 3 - Synthèse IA

### Rôle

Analyser la recherche brute, sélectionner 6 sujets prioritaires, synthétiser en profondeur avec divergences entre sources.

### Modèle

**GPT-4 Turbo** (`gpt-4-turbo-preview`)
- Température : 0.7 (créativité modérée pour analyse)
- Max tokens : 12000
- Entrée : `recherche_ia_brute.json`

### Sélection des 6 sujets

**STRUCTURE OBLIGATOIRE** :
1. **Sujet 1** : TENDANCE QUI FAIT PARLER (buzz, controverse)
2. **Sujet 2** : TENDANCE QUI FAIT PARLER
3. **Sujet 3** : TENDANCE QUI FAIT PARLER
4. **Sujet 4** : SUJET TECHNOLOGIQUE (avancée, modèle, hardware)
5. **Sujet 5** : SUJET TECHNOLOGIQUE
6. **Sujet 6** : SUJET TECHNOLOGIQUE

### Structure par sujet

```markdown
## [SUJET X/6] – [Titre accrocheur]

### Résumé
[3-4 lignes : faits essentiels, enjeux]

### Synthèse approfondie
[15-25 lignes :
- Contexte : Événement déclencheur
- Faits clés : Qui, quoi, quand, chiffres
- Impacts : Industrie, utilisateurs, concurrents
- Analyse critique : Importance, ruptures potentielles]

### Divergences entre sources
[Si pertinent : Désaccords, angles différents, débats]

### Sources
- [Titre] – [Source] – [URL]
- [...]
```

### Autres sujets (liste compacte)

```markdown
### [Titre court]
**Résumé** : [2-3 lignes]
**Synthèse** : [5-8 lignes]
**Source** : [Média] – [URL]
```

### Format de sortie

Fichier Markdown : `VeilleIA.md` (uploadé sur Google Drive)

### Coût estimé

~10000 tokens × 0.012$/1K (moyenne input/output) = **~0.12€**

---

## 🧠 Agent 4 - Synthèse News

### Rôle

Analyser la recherche brute, sélectionner 6 sujets avec répartition géographique obligatoire, synthétiser en profondeur.

### Modèle

**GPT-4 Turbo** (`gpt-4-turbo-preview`)
- Température : 0.7
- Max tokens : 12000
- Entrée : `recherche_news_brute.json`

### Sélection des 6 sujets

**RÉPARTITION OBLIGATOIRE** :
1. **Sujet 1** : INTERNATIONAL (géopolitique, économie mondiale)
2. **Sujet 2** : INTERNATIONAL
3. **Sujet 3** : NATIONAL (France : politique, économie, société)
4. **Sujet 4** : NATIONAL
5. **Sujet 5** : LOCAL (Bretagne/Pays de Loire : politique, sports maritimes, mer)
6. **Sujet 6** : LOCAL

### Structure par sujet

Identique à Agent 3 (Résumé, Synthèse, Divergences, Sources)

### Format de sortie

Fichier Markdown : `VeilleNews.md` (uploadé sur Google Drive)

### Coût estimé

~10000 tokens × 0.012$/1K = **~0.12€**

---

## 🔄 Workflow GitHub Actions

### Pipeline complet

```yaml
name: Veille OpenAI Complète (4 agents)

schedule:
  - cron: '0 6 * * *'  # 6h00 Paris

jobs:
  # JOB 1.1 : Recherche IA (parallèle)
  step-1-1-recherche-ia:
    - Checkout
    - Setup Python
    - Install deps
    - Run agent_recherche_ia.py
    - Upload recherche_ia_brute.json (artifact)

  # JOB 2.1 : Recherche News (parallèle avec 1.1)
  step-2-1-recherche-news:
    - Checkout
    - Setup Python
    - Install deps
    - Run agent_recherche_news.py
    - Upload recherche_news_brute.json (artifact)

  # JOB 1.2 : Synthèse IA (attend 1.1)
  step-1-2-synthese-ia:
    needs: [step-1-1-recherche-ia]
    - Checkout
    - Setup Python
    - Download recherche_ia_brute.json
    - Run agent_synthese_ia_v2.py
    - Upload VeilleIA.md vers Google Drive

  # JOB 2.2 : Synthèse News (attend 2.1)
  step-2-2-synthese-news:
    needs: [step-2-1-recherche-news]
    - Checkout
    - Setup Python
    - Download recherche_news_brute.json
    - Run agent_synthese_news_v2.py
    - Upload VeilleNews.md vers Google Drive

  # JOB 3 : Validation (attend 1.2 ET 2.2)
  step-3-validation-markdown:
    needs: [step-1-2-synthese-ia, step-2-2-synthese-news]
    - Run agent_validateur_markdown.py

  # JOB 4 : Sync Markdown (attend 3)
  step-4-sync-markdown:
    needs: [step-3-validation-markdown]
    - Download depuis Google Drive
    - Commit vers docs/markdown/

  # JOB 5 : Génération data.json (attend 4)
  step-5-update-data-json:
    needs: [step-4-sync-markdown]
    - Run agent_generateur_json.py
    - Commit docs/data.json

  # JOB 6 : Résumé final (attend 5)
  step-6-summary:
    needs: [step-5-update-data-json]
    - Affiche statistiques
```

### Temps d'exécution

- **Job 1.1** : ~2 min (recherche IA)
- **Job 2.1** : ~2 min (recherche News) - **PARALLÈLE avec 1.1**
- **Job 1.2** : ~2 min (synthèse IA)
- **Job 2.2** : ~2 min (synthèse News) - **PARALLÈLE avec 1.2**
- **Job 3** : ~30s (validation)
- **Job 4** : ~30s (sync)
- **Job 5** : ~30s (data.json)
- **Job 6** : ~10s (résumé)

**Total** : ~5-8 minutes (grâce à la parallélisation)

---

## 💰 Budget et optimisations

### Coûts quotidiens

| Agent | Tokens | Coût |
|-------|--------|-------|
| Recherche IA | 5K | 0.06€ |
| Synthèse IA | 10K | 0.12€ |
| Recherche News | 5K | 0.06€ |
| Synthèse News | 10K | 0.12€ |
| **TOTAL** | **30K** | **0.36€** |

### Coûts mensuels

- **Par mois** : 0.36€ × 30 = **10.80€**
- **Jusqu'à fin mars (60j)** : 0.36€ × 60 = **21.60€**

### Optimisations techniques

1. **Modèle** : GPT-4 Turbo au lieu de GPT-4 standard (3x moins cher)
2. **Token limits** : Strictes (8K recherche, 12K synthèse)
3. **Température** : 0.1 pour recherche (moins créatif = moins de tokens)
4. **Parallélisation** : Recherches IA + News en même temps
5. **web_search natif** : Pas de coût Tavily API (0.18€ économisés)

---

## ✅ Avantages de l'architecture 4-agents

### Qualité

✅ **Séparation claire** : Collecte vs Analyse  
✅ **Sources directes** : Accès aux sites institutionnels  
✅ **Analyse approfondie** : 15-25 lignes par sujet  
✅ **Divergences** : Comparaison entre sources  
✅ **Citations complètes** : Toutes les sources avec URLs

### Structure

✅ **6 sujets prioritaires** : Traitement en profondeur  
✅ **Répartition claire** : 3 tendances + 3 tech (IA) | 2 int + 2 nat + 2 local (News)  
✅ **Autres sujets** : Liste compacte pour traçabilité  
✅ **Équilibre** : 75% sujets principaux, 25% autres

### Performance

✅ **Parallélisation** : IA + News en même temps  
✅ **5-8 minutes** : Exécution complète  
✅ **Budget maîtrisé** : 0.36€/jour  
✅ **Fiabilité** : Validation Markdown automatique

---

## 🛠️ Maintenance et évolutions futures

### Maintenance courante

- Vérifier quotidiennement l'exécution du workflow
- Surveiller les coûts OpenAI
- Vérifier la qualité des synthèses
- Ajuster les sources si nécessaire

### Évolutions possibles

1. **Ajout de sources** : Nouveaux sites institutionnels IA ou presse
2. **Amélioration synthèse** : Affiner les prompts pour plus de profondeur
3. **Métriques qualité** : Tracking diversité sources, longueur synthèses
4. **Notifications** : Alertes sur sujets critiques
5. **Export PDF** : Génération PDF depuis Markdown

### Points d'attention

⚠️ **web_search** : Dépend de la disponibilité OpenAI (pas de SLA)  
⚠️ **Sources** : URLs institutionnelles peuvent changer  
⚠️ **Budget** : Surveiller si augmentation tokens  
⚠️ **Qualité** : Vérifier régulièrement les synthèses

---

## 📚 Références

- **OpenAI GPT-4 Turbo** : https://platform.openai.com/docs/models/gpt-4-turbo-and-gpt-4
- **GitHub Actions** : https://docs.github.com/en/actions
- **Google Drive API** : https://developers.google.com/drive/api/guides/about-sdk
- **Markdown** : https://www.markdownguide.org/

---

*Document créé le 01 février 2026*
