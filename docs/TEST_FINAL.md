# 🧪 Test Final - Instructions de lancement

## ✅ Corrections appliquées (Commit: 6c6f0cd)

### Changements finaux
- ✅ Workflow exécute depuis la **racine** du repo
- ✅ Fichier JSON créé à la **racine** : `articles_filtres_ia.json`
- ✅ Upload/Download d'artifact depuis la **racine**
- ✅ Ajout de **logs de vérification** pour diagnostiquer

---

## 🚀 Comment lancer le test

### Option 1 : Via GitHub UI (Recommandé)

1. **Ouvrir** : https://github.com/nliziard-ops/VeilleNLI/actions
2. **Cliquer** sur "Agents Veille IA - OpenAI (2 agents)" dans la liste de gauche
3. **Cliquer** sur le bouton bleu "Run workflow" en haut à droite
4. **Sélectionner** la branche "main"
5. **Cliquer** "Run workflow" (bouton vert)

### Option 2 : Via GitHub CLI

```bash
gh workflow run veille-ia-openai.yml --repo nliziard-ops/VeilleNLI
```

---

## 📊 Ce que tu devrais voir

### ✅ Job 1 - Agent Collecteur (2-3 min)

**Étapes attendues :**
1. ✅ Checkout code
2. ✅ Setup Python 3.11
3. ✅ Install dependencies
4. ✅ Run Agent 1 - Collecteur
   ```
   🔍 Lancement de 12 recherches Tavily...
     [1/12] AI LLM news this week
     [2/12] OpenAI GPT latest announcements
     ...
   ✅ 87 articles bruts collectés
   🤖 Filtrage et classification avec GPT-4o-mini...
   📊 Tokens utilisés : 3421 (prompt: 2145, completion: 1276)
   💾 JSON sauvegardé : articles_filtres_ia.json
   📊 Taille : 15234 octets
   ✅ AGENT 1 TERMINÉ AVEC SUCCÈS
   ```
5. ✅ Verify JSON file exists
   ```
   📁 Vérification du fichier JSON...
   -rw-r--r-- 1 runner runner 15234 Jan 11 09:42 articles_filtres_ia.json
   📊 Taille du fichier:
   15K     articles_filtres_ia.json
   ```
6. ✅ Upload artifact
   ```
   Uploading artifact 'articles-filtres-ia'...
   ✓ Upload complete
   ```

### ✅ Job 2 - Agent Synthèse (1-2 min)

**Étapes attendues :**
1. ✅ Checkout code
2. ✅ Setup Python 3.11
3. ✅ Install dependencies
4. ✅ Download artifact
   ```
   Downloading artifact 'articles-filtres-ia'...
   ✓ Download complete
   ```
5. ✅ Verify downloaded JSON
   ```
   📁 Vérification du JSON téléchargé...
   -rw-r--r-- 1 runner runner 15234 Jan 11 09:42 articles_filtres_ia.json
   ```
6. ✅ Run Agent 2 - Synthèse
   ```
   📂 ÉTAPE 1/3 : Chargement du JSON filtré (Agent 1)
   ✅ JSON chargé : 15 articles
   📊 Thèmes : Nouveaux modèles LLM, Open source & écosystèmes, ...
   
   📝 ÉTAPE 2/3 : Génération synthèse Markdown (GPT-4o)
   🤖 Génération de la synthèse Markdown avec GPT-4o...
   📊 Tokens utilisés : 7521 (prompt: 1834, completion: 5687)
   💰 Coût estimé : $0.0642
   ✅ Synthèse générée : 22145 caractères
   
   ☁️  ÉTAPE 3/3 : Upload vers Google Drive
   ☁️  Upload vers Google Drive...
   ✅ Fichier VeilleIA.md mis à jour sur Google Drive
   
   ✅ AGENT 2 TERMINÉ AVEC SUCCÈS
   ```

---

## 🔍 Points de vérification

### Pendant l'exécution

- [ ] **Job 1** : Status "In progress" puis "Success" (vert)
- [ ] **Job 2** : Attend Job 1, puis "In progress", puis "Success" (vert)
- [ ] **Durée totale** : 3-5 minutes

### Après l'exécution

1. **GitHub Actions** :
   - [ ] Les 2 jobs sont verts ✅
   - [ ] Artifact "articles-filtres-ia" créé (visible dans la page du workflow)
   
2. **Logs détaillés** :
   - [ ] Agent 1 : 12 recherches Tavily effectuées
   - [ ] Agent 1 : ~80-100 articles bruts collectés
   - [ ] Agent 1 : ~15-18 articles filtrés finaux
   - [ ] Agent 1 : JSON créé et vérifié
   - [ ] Agent 2 : JSON chargé avec succès
   - [ ] Agent 2 : Synthèse générée (~20000-25000 caractères)
   - [ ] Agent 2 : Upload Google Drive réussi

3. **Google Drive** :
   - [ ] Fichier `VeilleIA.md` présent
   - [ ] Dernière modification = date/heure du workflow
   - [ ] Contenu = synthèse Markdown bien formatée

---

## 💰 Coût du test

| Agent | Modèle | Tokens | Coût |
|-------|--------|--------|------|
| Agent 1 | GPT-4o-mini | ~3500 | $0.001 |
| Agent 2 | GPT-4o | ~7500 | $0.064 |
| **Total** | - | ~11000 | **$0.065** |

**Environ 0.06€ par exécution**

---

## ❌ Si échec

### Erreur : "No files were found"
→ Vérifier que `articles_filtres_ia.json` est créé à la racine (step "Verify JSON")

### Erreur : "Artifact not found"
→ Vérifier que Job 1 a bien uploadé l'artifact (step "Upload artifact")

### Erreur : OpenAI API
→ Vérifier `OPENAI_API_KEY` dans Secrets
→ Vérifier le crédit OpenAI restant

### Erreur : Tavily API
→ Vérifier `TAVILY_API_KEY` dans Secrets
→ Vérifier le quota Tavily (1000 req/mois gratuit)

### Erreur : Google Drive
→ Vérifier `GOOGLE_DRIVE_CREDENTIALS` et `GOOGLE_DRIVE_FOLDER_ID`

---

## ✅ Si succès

**Prochaines étapes :**

1. ✅ **Valider** la qualité de la synthèse dans `VeilleIA.md`
2. 🔄 **Dupliquer** pour Veille News (Phase 3)
3. 🌐 **Créer** le frontend web (Phase 4)
4. 🧹 **Nettoyer** les anciens agents Anthropic (Phase 5)

---

## 📝 Notes

- Le workflow s'exécutera **automatiquement tous les jours à 6h00 Paris**
- Tu peux le **désactiver** temporairement dans Settings → Actions
- Les artifacts sont **conservés 1 jour** (suffisant pour le test)
- Le fichier `VeilleIA.md` sur Google Drive est **écrasé** à chaque exécution

---

**Date de préparation** : 2026-01-11 10:40 UTC
**Commit de correction** : 6c6f0cd5c26c3f333193a714dfc4e279bad8427a
