# Solution : Garantir 6 sujets principaux dans les fichiers Markdown

**Date** : 11 janvier 2026  
**Problème** : Les fichiers VeilleIA.md et VeilleNews.md ne contenaient que 2 articles principaux au lieu de 6  
**Impact** : Le site web n'affichait qu'1 seul article détaillé  

---

## 🎯 PROBLÈME IDENTIFIÉ

Les fichiers Markdown générés par les agents de synthèse contenaient :
- ✅ 2 articles principaux détaillés (avec sections Résumé, Points de vue, Analyse, Sources)
- ❌ 4-6 sujets dans "Autres sujets" (format bref)

Le site web devait afficher **6 articles principaux en cards détaillées**, mais n'en avait que 2.

---

## ✅ SOLUTION DÉPLOYÉE

### 1. **Agent Validateur Markdown** (`agents/agent_validateur_markdown.py`)

**Rôle** : Garantir que chaque fichier Markdown contient au minimum 6 sujets principaux.

**Fonctionnement** :
1. Télécharge `VeilleIA.md` et `VeilleNews.md` depuis Google Drive
2. Parse la structure Markdown
3. Compte le nombre d'articles principaux (sections `## [THEME] – Titre`)
4. **Si < 6 articles** :
   - Promeut automatiquement des sujets depuis "Autres sujets"
   - Les convertit en articles principaux avec structure complète
5. Reformate le fichier selon structure standardisée
6. Upload le fichier corrigé sur Google Drive

**Quand s'exécute-t-il ?**  
Automatiquement après chaque exécution des agents de synthèse (veille-ia-openai.yml et veille-news-openai.yml)

---

### 2. **Workflow GitHub Actions** (`.github/workflows/validation-markdown.yml`)

**Déclenchement** :
- Automatiquement après workflows `veille-ia-openai` et `veille-news-openai`
- Manuellement via GitHub Actions UI

**Actions** :
- Installe dépendances Python (google-api-python-client)
- Exécute `agent_validateur_markdown.py`
- Valide et reformate VeilleIA.md et VeilleNews.md

---

### 3. **Workflow Synchronisation** (`.github/workflows/sync-markdown.yml`)

**Rôle** : Copier les fichiers Markdown depuis Google Drive vers le repository GitHub (dossier `docs/markdown/`)

**Déclenchement** :
- Automatiquement après workflow `validation-markdown`
- Manuellement via GitHub Actions UI

**Actions** :
- Télécharge VeilleIA.md et VeilleNews.md depuis Google Drive
- Copie vers `docs/markdown/`
- Commit automatique des changements
- Le site GitHub Pages lit directement ces fichiers

---

### 4. **Site Web Corrigé** (`docs/index.html`)

**Améliorations apportées** :

#### Parser Markdown robuste
- Détection correcte des articles principaux : `## [THEME] – Titre`
- Extraction complète des sections (Résumé, Points de vue, Analyse, Signaux faibles, Sources)
- Gestion des "Autres sujets" : `### Titre`

#### Liens 100% cliquables
- Fonction `linkifyText()` qui convertit automatiquement toutes les URLs en liens HTML
- Format : `<a href="URL" target="_blank" rel="noopener noreferrer">URL</a>`
- Application sur les sources ET les autres sujets

#### Structure garantie
- Affichage de **6 articles principaux maximum** en cards détaillées
- Si plus de 6 articles principaux dans le Markdown, les excédents vont automatiquement dans "Autres sujets"
- Section "Autres sujets de la semaine" en liste compacte

#### Détails dépliables fonctionnels
- Bouton "Lire plus" déploie les détails complets de l'article
- Affichage des points de vue croisés, analyses, signaux faibles et sources
- Animation fluide de dépliage/repliage

---

## 🔄 FLUX AUTOMATISÉ COMPLET

```
┌──────────────────────────────────────────────────────────────┐
│ 1. Agents Collecteurs (6h Paris)                              │
│    - agent_collecteur_ia.py (GPT-4o-mini)                    │
│    - agent_collecteur_news.py (GPT-4o-mini)                  │
│    → Génèrent articles_filtres_ia.json                       │
│    → Génèrent articles_filtres_news.json                     │
└────────────────────┬─────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────────────────────┐
│ 2. Agents Synthèse                                            │
│    - agent_synthese_ia.py (GPT-4o)                           │
│    - agent_synthese_news.py (GPT-4o)                         │
│    → Génèrent VeilleIA.md (brouillon)                        │
│    → Génèrent VeilleNews.md (brouillon)                      │
│    → Upload vers Google Drive                                 │
└────────────────────┬─────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────────────────────┐
│ 3. Agent Validateur (NOUVEAU)                                 │
│    - agent_validateur_markdown.py                             │
│    → Télécharge fichiers depuis Drive                        │
│    → Valide structure (6 sujets minimum)                     │
│    → Reformate si nécessaire                                  │
│    → Upload fichiers corrigés sur Drive                       │
└────────────────────┬─────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────────────────────┐
│ 4. Sync vers GitHub (NOUVEAU)                                 │
│    - sync-markdown.yml workflow                               │
│    → Copie VeilleIA.md vers docs/markdown/                   │
│    → Copie VeilleNews.md vers docs/markdown/                 │
│    → Commit automatique                                       │
└────────────────────┬─────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────────────────────┐
│ 5. Site Web (GitHub Pages)                                    │
│    - index.html lit docs/markdown/*.md                        │
│    → Parse Markdown avec liens cliquables                    │
│    → Affiche 6 cards + liste "Autres sujets"                 │
│    → https://nliziard-ops.github.io/VeilleNLI/              │
└──────────────────────────────────────────────────────────────┘
```

---

## 🚀 MISE EN PLACE

### Étape 1 : Reformater les fichiers actuels

Les fichiers actuels (VeilleIA.md et VeilleNews.md) ne contiennent que 2 articles principaux.

**Action requise** : Exécuter manuellement le workflow de validation

1. Aller sur : https://github.com/nliziard-ops/VeilleNLI/actions/workflows/validation-markdown.yml
2. Cliquer sur "Run workflow" (bouton à droite)
3. Sélectionner branche "main"
4. Cliquer sur "Run workflow"

Le workflow va :
- Télécharger les fichiers actuels
- Promouvoir 4 sujets depuis "Autres sujets" vers articles principaux
- Reformater pour avoir 6 sections principales
- Upload les fichiers corrigés

### Étape 2 : Synchroniser vers GitHub Pages

1. Aller sur : https://github.com/nliziard-ops/VeilleNLI/actions/workflows/sync-markdown.yml
2. Cliquer sur "Run workflow"
3. Le workflow va copier les fichiers depuis Drive vers `docs/markdown/`

### Étape 3 : Vérifier le site

1. Attendre 1-2 minutes (déploiement GitHub Pages)
2. Ouvrir : https://nliziard-ops.github.io/VeilleNLI/
3. Vérifier que les 2 onglets (Veille IA / Actualités) affichent bien 6 articles en cards

---

## 📊 STRUCTURE MARKDOWN STANDARDISÉE

```markdown
---
agent: Veille IA (2 agents OpenAI)
date: 2026-01-11
catégorie: Intelligence Artificielle
---

# Veille IA & LLM – Semaine du 04/01/2026 au 11/01/2026

**Édition Tensor**

---

## Introduction

[Texte d'introduction]

---

## [SUJET 1] – Titre accrocheur

### Résumé
[Texte du résumé]

### Points de vue croisés

**Source 1**
[Contenu]

**Source 2**
[Contenu]

### Analyse & implications
- Impacts sectoriels : [...]
- Opportunités : [...]

### Signaux faibles
- [Points incertains]

### Sources
- Source 1 – https://example.com/article1
- Source 2 – https://example.com/article2

---

[RÉPÉTER POUR SUJETS 2, 3, 4, 5, 6]

---

## Autres sujets de la semaine

### Titre sujet A
**Thème** : Catégorie
**Résumé** : [2-3 lignes]
**Source** : Média – https://example.com

### Titre sujet B
**Thème** : Catégorie
**Résumé** : [2-3 lignes]
**Source** : Média – https://example.com

---

**Fin de l'édition**
*Veille générée automatiquement par système 2-agents OpenAI*
```

---

## 🔧 MAINTENANCE FUTURE

### Automatique
- Les workflows s'exécutent automatiquement après chaque génération
- Aucune intervention manuelle requise
- Les fichiers sont toujours garantis avec 6 sujets minimum

### Manuel (si nécessaire)
- Lancer "🔍 Validation Markdown" si les fichiers semblent incorrects
- Lancer "📋 Sync Markdown" si le site n'affiche pas les dernières données

---

## 📝 FICHIERS MODIFIÉS/CRÉÉS

### Nouveaux fichiers
- `agents/agent_validateur_markdown.py` - Agent de validation
- `.github/workflows/validation-markdown.yml` - Workflow validation
- `.github/workflows/sync-markdown.yml` - Workflow synchronisation
- `docs/SOLUTION_6_SUJETS.md` - Cette documentation

### Fichiers modifiés
- `docs/index.html` - Parser amélioré + liens cliquables

### Fichiers inchangés
- Agents collecteurs et synthèse (fonctionnent normalement)
- Workflows existants (veille-ia-openai.yml, veille-news-openai.yml)

---

## ✅ VALIDATION

**Critères de succès** :
- ✅ Site web affiche 6 articles principaux en cards détaillées
- ✅ Tous les liens sources sont cliquables (s'ouvrent dans nouvel onglet)
- ✅ Section "Autres sujets" contient les sujets supplémentaires
- ✅ Navigation IA/Actualités fonctionnelle
- ✅ Boutons "Lire plus" déploient les détails
- ✅ Design préservé

**Comment tester** :
1. Exécuter workflow validation manuellement
2. Exécuter workflow sync manuellement
3. Rafraîchir le site : https://nliziard-ops.github.io/VeilleNLI/
4. Vérifier chaque onglet (Veille IA et Actualités)
5. Cliquer sur "Lire plus" pour vérifier détails et sources

---

## 💡 AMÉLIORATIONS FUTURES POSSIBLES

1. **Style visuel** : Améliorer design des cards, couleurs, typographie
2. **Filtres** : Ajouter filtres par thème, date, pertinence
3. **Recherche** : Fonction de recherche dans les articles
4. **Export** : Bouton pour télécharger la synthèse en PDF
5. **Archives** : Accès aux veilles précédentes

---

**Fin de la documentation**  
*Solution déployée le 11 janvier 2026*
