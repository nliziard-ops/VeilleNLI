# 📚 VeilleNLI - Documentation

Bienvenue dans la documentation du projet VeilleNLI !

## 📄 Documents principaux

### README.md
**Documentation principale du projet**
- Architecture technique
- Guide d'utilisation
- Coûts et monitoring
- Structure des fichiers

👉 [Lire README.md](README.md)

### MIGRATION_COMPLETE.md
**Historique de la migration Anthropic → OpenAI**
- Chronologie détaillée (10-17 janvier 2026)
- Modifications techniques
- Analyse des coûts
- Leçons apprises

👉 [Lire MIGRATION_COMPLETE.md](MIGRATION_COMPLETE.md)

---

## 📦 Archive

Les documents de travail créés pendant la migration ont été archivés dans le dossier `archive/` :

- `archive/README_MIGRATION_V2.md` - Plan initial de migration
- `archive/RECAP_PHASE1.md` - Récap Phase 1
- `archive/VALIDATION_TESTS.md` - Tests initiaux

👉 [Voir le dossier archive/](archive/)

---

## 🔗 Liens rapides

- **Site web** : https://nliziard-ops.github.io/VeilleNLI/
- **Repository** : https://github.com/nliziard-ops/VeilleNLI
- **Workflows** : https://github.com/nliziard-ops/VeilleNLI/actions

---

## 🎯 Démarrage rapide

### Consulter les veilles
Visitez https://nliziard-ops.github.io/VeilleNLI/

### Relancer manuellement
1. Allez dans Actions → "Veille Quotidienne (IA + News)"
2. Cliquez "Run workflow"
3. Attendez 3-5 minutes
4. Le site se met à jour automatiquement

### Tests locaux
```bash
# 1. Cloner le repo
git clone https://github.com/nliziard-ops/VeilleNLI.git
cd VeilleNLI

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Configurer les variables d'environnement
export OPENAI_API_KEY="sk-..."
export TAVILY_API_KEY="tvly-..."

# 4. Tester un agent
python agents/agent_veille_ia.py

# 5. Servir le site localement
cd docs
python -m http.server 8000
# Ouvrir http://localhost:8000
```

---

## 📊 État du système

| Aspect | Statut |
|--------|--------|
| Migration OpenAI | ✅ Terminée |
| Workflow unique | ✅ Actif |
| Site web | ✅ En ligne |
| Budget | ✅ Optimisé (~0.16€/jour) |
| Documentation | ✅ À jour |

---

## 🤝 Contribution

Projet personnel de Nicolas Liziard.

Contact : [@nliziard-ops](https://github.com/nliziard-ops)

---

*Dernière mise à jour : 17 janvier 2026*
