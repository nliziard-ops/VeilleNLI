# 🔧 Corrections appliquées - Problème de chemins fichiers

## ❌ Problème initial

Les erreurs suivantes sont apparues lors du premier test :

```
Agent 1: No files were found with the provided path: /tmp/articles_filtres_ia.json
Agent 2: Artifact not found for name: articles-filtres-ia
```

## 🔍 Cause racine

Le répertoire `/tmp/` dans GitHub Actions n'est **pas partagé** entre les jobs. Chaque job s'exécute dans un runner isolé avec son propre filesystem.

## ✅ Solutions appliquées

### 1. Agent 1 - Collecteur (`agent_collecteur_ia.py`)

**Avant :**
```python
OUTPUT_JSON = "/tmp/articles_filtres_ia.json"
```

**Après :**
```python
OUTPUT_JSON = "articles_filtres_ia.json"  # Répertoire courant
```

### 2. Agent 2 - Synthèse (`agent_synthese_ia.py`)

**Avant :**
```python
INPUT_JSON = "/tmp/articles_filtres_ia.json"
```

**Après :**
```python
INPUT_JSON = "articles_filtres_ia.json"  # Répertoire courant
```

### 3. Workflow GitHub Actions (`.github/workflows/veille-ia-openai.yml`)

**Modifications :**

**Agent 1 - Upload artifact :**
```yaml
# Avant
path: /tmp/articles_filtres_ia.json

# Après
- name: Run Agent 1
  run: |
    cd agents
    python agent_collecteur_ia.py

- name: Upload artifact
  path: agents/articles_filtres_ia.json  # Chemin correct
```

**Agent 2 - Download artifact :**
```yaml
# Avant
path: /tmp/

# Après
- name: Download artifact
  path: agents/  # Télécharge dans agents/

- name: Run Agent 2
  run: |
    cd agents
    python agent_synthese_ia.py
```

## 📋 Fichiers modifiés

| Fichier | SHA avant | SHA après | Commit |
|---------|-----------|-----------|--------|
| `agents/agent_collecteur_ia.py` | `8f3fce6` | `c8f2e55` | [3e8cac3](https://github.com/nliziard-ops/VeilleNLI/commit/3e8cac3) |
| `agents/agent_synthese_ia.py` | `1f1a31d` | `b249758` | [f1d7167](https://github.com/nliziard-ops/VeilleNLI/commit/f1d7167) |
| `.github/workflows/veille-ia-openai.yml` | `f157d3e` | `e0f9bac` | [d7ef494](https://github.com/nliziard-ops/VeilleNLI/commit/d7ef494) |

## 🧪 Test de validation

Pour vérifier que les corrections fonctionnent :

1. **Aller sur GitHub Actions** : https://github.com/nliziard-ops/VeilleNLI/actions
2. **Cliquer sur** "Agents Veille IA - OpenAI (2 agents)"
3. **Run workflow** → Sélectionner "main" → **Run workflow**
4. **Vérifier que** :
   - ✅ Agent 1 crée bien `articles_filtres_ia.json` dans `agents/`
   - ✅ Upload artifact réussit
   - ✅ Agent 2 télécharge l'artifact
   - ✅ Agent 2 trouve le fichier JSON et génère la synthèse
   - ✅ Upload Google Drive réussit

## 💡 Leçons apprises

### ❌ Ne pas faire :
- Utiliser `/tmp/` pour partager des données entre jobs GitHub Actions
- Supposer que le filesystem est partagé entre jobs

### ✅ Bonnes pratiques :
- Utiliser le **répertoire de travail** (`./`) ou des sous-répertoires (`agents/`)
- Utiliser les **artifacts GitHub Actions** pour transférer des fichiers entre jobs
- Toujours spécifier le `path:` complet lors de l'upload/download d'artifacts
- Utiliser `cd` avant d'exécuter les scripts pour garantir le bon répertoire de travail

## 🎯 Résultat attendu

Après ces corrections, le workflow devrait fonctionner comme suit :

```
Job 1 (Agent Collecteur):
  → cd agents/
  → python agent_collecteur_ia.py
  → Crée agents/articles_filtres_ia.json
  → Upload artifact "articles-filtres-ia"

Job 2 (Agent Synthèse):
  → Download artifact → agents/articles_filtres_ia.json
  → cd agents/
  → python agent_synthese_ia.py
  → Lit agents/articles_filtres_ia.json
  → Upload VeilleIA.md vers Google Drive
```

---

*Corrections appliquées le 2026-01-11*
