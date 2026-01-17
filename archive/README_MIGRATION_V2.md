# VeilleNLI - Migration v2.0 : Système Dynamique

> **📦 DOCUMENT ARCHIVÉ** - Ce document a été créé pendant la migration.
> Consultez **MIGRATION_COMPLETE.md** pour la documentation finale.

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

---

**Status** : ✅ MIGRATION TERMINÉE  
**Archivé le** : 17 janvier 2026