# ⚠️ NETTOYAGE MANUEL REQUIS

## Fichiers à supprimer manuellement

Les workflows suivants ont été remplacés par `veille-openai-v3.yml` et doivent être supprimés :

### À supprimer via l'interface GitHub :

1. ✅ `.github/workflows/deep-research-daily.yml`
2. ✅ `.github/workflows/list-models.yml`  
3. ✅ `.github/workflows/veille-openai-complete.yml`
4. ✅ `.github/workflows/veille-quotidienne.yml`
5. ✅ `.github/workflows/update-data.yml` (fichier vide)

### Fichiers .disabled créés (à conserver temporairement) :

- `.github/workflows/deep-research-daily.yml.disabled`
- `.github/workflows/list-models.yml.disabled`
- `.github/workflows/veille-openai-complete.yml.disabled`
- `.github/workflows/veille-quotidienne.yml.disabled2`

## Procédure de suppression

**Via l'interface web GitHub :**

1. Aller sur https://github.com/nliziard-ops/VeilleNLI
2. Naviguer vers `.github/workflows/`
3. Pour chaque fichier `.yml` (sans .disabled) :
   - Cliquer sur le fichier
   - Cliquer sur l'icône 🗑️ (poubelle) en haut à droite
   - Ajouter message : "🗑️ Suppression workflow obsolète"
   - Cliquer "Commit changes"

**Via ligne de commande (plus rapide) :**

```bash
git pull origin main

# Supprimer les anciens workflows
git rm .github/workflows/deep-research-daily.yml
git rm .github/workflows/list-models.yml
git rm .github/workflows/veille-openai-complete.yml
git rm .github/workflows/veille-quotidienne.yml
git rm .github/workflows/update-data.yml

# Commit et push
git commit -m "🗑️ Suppression workflows obsolètes (remplacés par v3)"
git push origin main
```

## ⚡ Workflow actif

**Seul workflow actif :**
- ✅ `.github/workflows/veille-openai-v3.yml` (avec cron quotidien 6h00)

## 📝 Une fois le nettoyage terminé

Supprimer ce fichier :
```bash
git rm .github/workflows/CLEANUP_README.md
git commit -m "🧹 Nettoyage terminé"
git push
```

---

**Date :** 2026-02-03  
**Architecture :** v3 - Séparation Collecte/Synthèse
