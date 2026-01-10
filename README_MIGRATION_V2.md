# VeilleNLI - Migration v2.0 : Système Dynamique

## 🎯 Objectif

Migrer le système de veille vers une architecture dynamique avec :
- **Agents OpenAI** pour la collecte (au lieu d'Anthropic)
- **Site HTML dynamique** qui fetch `data.json`
- **Budget maîtrisé** : 25€ jusqu'à fin mars
- **Simplicité** : Pas de frameworks lourds

## 📊 Architecture v2.0

```
Agents OpenAI (IA + News)
         ↓
   Google Drive
   (Markdown)
         ↓
Agent Générateur JSON
         ↓
   docs/data.json
         ↓
  Site HTML dynamique
```

## ✅ Phase 1 : TERMINÉE ✨

### Fichiers créés

1. **`agents/agent_generateur_json.py`**
   - Parse les fichiers Markdown depuis Google Drive
   - Génère `docs/data.json` structuré
   - Extraction automatique : métadonnées, sujets, sources, points clés

2. **`docs/index.html`** (nouveau)
   - Site 100% dynamique
   - Fetch `data.json` au chargement
   - Bouton "Rafraîchir" fonctionnel
   - Design Comics/BD identique à v1

3. **`.github/workflows/update-data.yml`**
   - Génère `data.json` automatiquement
   - Commit et push vers GitHub
   - Déclenché après les agents collecteurs

4. **`docs/FORMAT_MARKDOWN_AGENTS.md`**
   - Format Markdown standardisé pour agents OpenAI
   - Documentation complète avec exemples
   - Checklist de validation

### Tests nécessaires

```bash
# 1. Tester localement le générateur JSON
export GOOGLE_DRIVE_CREDENTIALS='...'
export GOOGLE_DRIVE_FOLDER_ID='...'
python agents/agent_generateur_json.py

# 2. Vérifier data.json
cat docs/data.json | python -m json.tool

# 3. Tester le site en local
cd docs
python -m http.server 8000
# Ouvrir http://localhost:8000
```

### Déploiement

1. **Activer le workflow**
   - Aller dans Actions → "Mise à jour des données de veille"
   - Cliquer sur "Run workflow"
   - Vérifier que `data.json` est créé dans `docs/`

2. **Vérifier GitHub Pages**
   - Ouvrir https://nliziard-ops.github.io/VeilleNLI/
   - Vérifier que le site charge les données
   - Tester le bouton rafraîchir

## 🔜 Phase 2 : Migration agents vers OpenAI

### Agents à créer

1. **`agents/agent_veille_ia_openai.py`**
   - Remplace `agent_veille_ia.py` (Anthropic)
   - Utilise OpenAI API
   - Génère Markdown selon format standardisé
   - Optimisé pour coûts (gpt-4o-mini prioritaire)

2. **`agents/agent_veille_news_openai.py`**
   - Remplace `agent_veille_news.py`
   - Même structure que IA
   - Budget 0.50€ par exécution max

### Workflow à modifier

- **`.github/workflows/agents-collecteurs.yml`**
  - Remplacer appels Anthropic par OpenAI
  - Ajouter `OPENAI_API_KEY`
  - Garder upload vers Google Drive

### Budget OpenAI

**Estimation par semaine :**
- Agent IA : ~0.50€
- Agent News : ~0.50€
- **Total : 1€/semaine**
- **12 semaines (jan-mars) : 12€**
- **Marge : 13€ restants**

## 🧪 Phase 3 : Tests en parallèle

1. Exécuter agents OpenAI manuellement
2. Vérifier format Markdown généré
3. Tester génération data.json
4. Comparer avec site v1
5. Valider qualité contenu

## 🚀 Phase 4 : Basculement v2

1. Désactiver workflow ancien générateur web
2. Activer workflow mise à jour data.json
3. Mettre à jour index.html (déjà fait)
4. Communiquer changement

## 🧹 Phase 5 : Nettoyage

### Fichiers à supprimer

```bash
agents/agent_generateur_web.py
.github/workflows/agent-generateur.yml
config/styles_preferences.json
```

### Secrets à supprimer

```
ANTHROPIC_API_KEY
```

## 📝 Format Markdown pour agents OpenAI

**⚠️ À lire absolument : `docs/FORMAT_MARKDOWN_AGENTS.md`**

Points clés :
- Front matter YAML obligatoire
- Sections `## **[CATÉGORIE] – [Titre]**`
- Sous-sections : Résumé, Points de vue, Sources
- Format sources : `- Titre – URL`
- Points clés numérotés en synthèse finale

## 🔧 Dépannage

### data.json non généré

```bash
# Vérifier secrets GitHub
echo $GOOGLE_DRIVE_CREDENTIALS | jq .

# Tester en local
python agents/agent_generateur_json.py
```

### Site n'affiche rien

```bash
# Vérifier data.json existe
curl https://nliziard-ops.github.io/VeilleNLI/data.json

# Vérifier console navigateur (F12)
```

### Format Markdown invalide

- Relire `docs/FORMAT_MARKDOWN_AGENTS.md`
- Vérifier les sections obligatoires
- Tester le parser localement

## 📊 Monitoring

### Logs GitHub Actions

- Workflow "Mise à jour des données" : génération data.json
- Workflow "Agents Collecteurs" : collecte données

### Métriques importantes

- Taille de `data.json` (doit être < 500KB)
- Nombre de sujets IA et News
- Temps d'exécution workflows
- Coût OpenAI par exécution

## 🔗 Liens utiles

- **Site** : https://nliziard-ops.github.io/VeilleNLI/
- **Repository** : https://github.com/nliziard-ops/VeilleNLI
- **Actions** : https://github.com/nliziard-ops/VeilleNLI/actions
- **Format Markdown** : `docs/FORMAT_MARKDOWN_AGENTS.md`

## 📞 Prochaines actions

1. ✅ Tester le workflow "Mise à jour des données"
2. ✅ Vérifier que le site fonctionne
3. ⏳ Créer les agents OpenAI
4. ⏳ Tester en parallèle
5. ⏳ Basculer vers v2

---

**Version** : 2.0  
**Date** : Janvier 2026  
**Status Phase 1** : ✅ TERMINÉE
