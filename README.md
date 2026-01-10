# 🔍 VeilleNLI v2.0

**Système automatisé de veille hebdomadaire intelligente - Architecture dynamique**

Un système de veille automatisée qui génère chaque semaine des synthèses d'actualités personnalisées sur l'IA et l'actualité générale, avec un site web dynamique au style comics pour les consulter.

---

## 🎯 Nouveauté v2.0 : Architecture Dynamique

**Migration complète** vers une architecture moderne :
- ✅ **Site HTML 100% dynamique** (fetch `data.json`)
- ✅ **Agent générateur JSON** (parse Markdown → JSON structuré)
- ✅ **Bouton rafraîchir** fonctionnel
- ✅ **Format Markdown standardisé** pour futurs agents OpenAI
- ✅ **Budget maîtrisé** : 25€ sur 3 mois

---

## 📋 Vue d'ensemble

VeilleNLI est orchestré par GitHub Actions avec :

1. **Agents collecteurs** (IA + News) : Génèrent fichiers Markdown
2. **Agent générateur JSON** : Parse Markdown → `data.json`
3. **Site web dynamique** : Fetch et affiche `data.json`

### 🏗️ Architecture v2.0

```
Agents (Anthropic/OpenAI)
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

## 🤖 Les Composants

### 1. Agents Collecteurs

**Agent Veille IA** (`agent_veille_ia.py`)
- Synthétise actualité IA/LLM hebdomadaire
- 9 catégories : modèles, open source, recherche, régulation, etc.
- Minimum 3 sources par sujet
- Sortie : `VeilleIA.md` sur Google Drive

**Agent Veille News** (`agent_veille_news.py`)
- Synthétise actualité générale
- 6 catégories : politique, économie, international, etc.
- Focus local : Nantes & Bretagne
- Sortie : `VeilleNews.md` sur Google Drive

### 2. Agent Générateur JSON (`agent_generateur_json.py`) ✨ NOUVEAU

**Mission** : Parser les Markdown et générer JSON structuré

**Fonctionnalités** :
- Télécharge Markdown depuis Google Drive
- Extrait métadonnées, titres, résumés, sources, points clés
- Génère icônes automatiques par catégorie
- Tronque résumés à 40 mots
- Sépare sujets importants (6) / secondaires (reste)
- Sortie : `docs/data.json`

### 3. Site Web Dynamique (`docs/index.html`) ✨ NOUVEAU

**Caractéristiques** :
- **100% dynamique** : fetch `data.json` au chargement
- **Bouton rafraîchir** : recharge les données
- **Navigation IA/News** : 2 onglets
- **Cards comics** : 6 sujets principaux par onglet
- **Expand/collapse** : résumés tronqués cliquables
- **Modals détaillés** : sources, points de vue, fiabilité
- **Design BD** : identique à v1

---

## ⚙️ Workflows GitHub Actions

### Workflow "Agents Collecteurs" (existant)

**Déclenchement** : Samedi 6h30
- Exécute agents IA + News
- Upload Markdown sur Google Drive

### Workflow "Mise à jour des données" ✨ NOUVEAU

**Déclenchement** : 
- Manuel (workflow_dispatch)
- Automatique après agents collecteurs
- Programmé (lundi 8h)

**Actions** :
1. Exécute `agent_generateur_json.py`
2. Génère `docs/data.json`
3. Commit et push automatique

---

## 📊 Format des données

### Structure `data.json`

```json
{
  "version": "2.0",
  "date_generation": "2026-01-10T15:30:00",
  "veilles": {
    "ia": {
      "metadata": {...},
      "titre": "Veille IA – Semaine du...",
      "edition": "Édition Tensor",
      "introduction": "...",
      "sujets_importants": [
        {
          "titre": "...",
          "icone": "🤖",
          "resume": "...",
          "resume_court": "...",
          "resume_complet": "...",
          "points_de_vue": [...],
          "fiabilite": [...],
          "sources": [...]
        }
      ],
      "sujets_secondaires": [...],
      "points_cles": [...]
    },
    "news": {...}
  }
}
```

### Format Markdown (agents)

**Documentation complète** : `docs/FORMAT_MARKDOWN_AGENTS.md`

**Structure obligatoire** :
- Front matter YAML
- Sections `## **[CATÉGORIE] – [Titre]**`
- Sous-sections : Résumé, Points de vue, Sources
- Format sources : `- Titre – URL`

---

## 🔧 Configuration

### Secrets GitHub requis

```bash
ANTHROPIC_API_KEY=sk-ant-xxxxx
GOOGLE_DRIVE_CREDENTIALS={"type": "service_account", ...}
GOOGLE_DRIVE_FOLDER_ID=1aBcDeFgHiJkLmN
OPENAI_API_KEY=sk-xxxxx  # Pour Phase 2
```

### Installation locale

```bash
git clone https://github.com/nliziard-ops/VeilleNLI.git
cd VeilleNLI

pip install -r requirements.txt

# Variables d'environnement
export GOOGLE_DRIVE_CREDENTIALS='...'
export GOOGLE_DRIVE_FOLDER_ID='...'

# Générer data.json
python agents/agent_generateur_json.py

# Tester le site
cd docs && python -m http.server 8000
```

---

## 🌐 Accès au site

**URL** : https://nliziard-ops.github.io/VeilleNLI/

**Fonctionnalités** :
- 🔄 Bouton rafraîchir
- 🤖 Onglet IA / 📰 Onglet News
- 📱 Responsive mobile
- 🎨 Design Comics/BD

---

## 📈 Statistiques

- **Fréquence** : Hebdomadaire (samedi)
- **Sujets par veille** : 10-15 (IA) / 8-10 (News)
- **Hiérarchisation** : 6 importants + secondaires
- **Sources minimales** : 3 par sujet
- **Temps lecture** : 10-15 min par veille

---

## 🗺️ Roadmap Migration

### ✅ Phase 1 : Infrastructure dynamique (TERMINÉE)
- Agent générateur JSON
- Site HTML dynamique
- Workflow GitHub Actions
- Documentation format Markdown

### ⏳ Phase 2 : Agents OpenAI
- `agent_veille_ia_openai.py`
- `agent_veille_news_openai.py`
- Budget : ~1€/semaine

### ⏳ Phase 3 : Tests en parallèle
- Validation format Markdown
- Vérification qualité contenu
- Tests de coûts

### ⏳ Phase 4 : Basculement v2
- Activation agents OpenAI
- Désactivation ancien système

### ⏳ Phase 5 : Nettoyage
- Suppression `agent_generateur_web.py`
- Suppression `ANTHROPIC_API_KEY`

---

## 📚 Documentation

- **`README_MIGRATION_V2.md`** : Guide migration complet
- **`docs/FORMAT_MARKDOWN_AGENTS.md`** : Format standardisé
- **`RECAP_PHASE1.md`** : Récapitulatif Phase 1
- **Code** : Commentaires français + docstrings

---

## 🔒 Sécurité

- Credentials Google Drive en secrets GitHub
- Pas d'exposition côté client
- HTTPS uniquement (GitHub Pages)
- Variables d'environnement pour config sensible

---

## 💰 Budget OpenAI

**Total** : 25€ (janvier - mars 2026)
**Estimation** : 1€/semaine (agents IA + News)
**Marge** : 13€

---

## 🆕 Changelog

### Version 2.0 - Janvier 2026

**Nouvelles fonctionnalités** :
- ✅ Site 100% dynamique avec fetch JSON
- ✅ Agent générateur JSON (parsing Markdown)
- ✅ Bouton rafraîchir fonctionnel
- ✅ Format Markdown standardisé
- ✅ Workflow automatisé data.json
- ✅ Documentation complète

**Architecture** :
- Migration vers système dynamique
- Préparation agents OpenAI
- Optimisation coûts

---

## 🛠️ Évolutions futures

- [ ] Migration agents vers OpenAI (Phase 2)
- [ ] Export PDF synthèses
- [ ] Archivage anciennes semaines
- [ ] Dashboard statistiques
- [ ] Mode sombre/clair
- [ ] Recherche dans archives
- [ ] Notifications email

---

## 📄 Licence

Projet personnel - Tous droits réservés

---

## 👤 Auteur

**Nicolas Liziard**  
Data Consultant chez CCR Consulting  
Nantes, France

---

## 🙏 Remerciements

- **Anthropic Claude** pour les capacités IA
- **GitHub Actions** pour l'orchestration
- **Google Drive API** pour le stockage
- **GitHub Pages** pour l'hébergement

---

**Dernière mise à jour** : 10 janvier 2026  
**Version** : 2.0 - Architecture Dynamique  
**Statut** : Phase 1 terminée, Phase 2 en cours
