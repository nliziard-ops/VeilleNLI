# ✅ Phase 3 - Agents News TERMINÉE

## 🎉 Résumé

La **Veille Actualités** est maintenant opérationnelle avec la même architecture 2-agents que la Veille IA !

---

## 📦 Fichiers créés

### Agents Python
1. **`agents/agent_collecteur_news.py`** ✅
   - Modèle : GPT-4o-mini
   - 10 recherches Tavily ciblées actualités FR/INT
   - Filtrage et classification
   - Output : `articles_filtres_news.json`

2. **`agents/agent_synthese_news.py`** ✅
   - Modèle : GPT-4o
   - Lecture JSON pré-filtré
   - Génération synthèse Markdown
   - Upload : `VeilleNews.md` sur Google Drive

### Workflow
3. **`.github/workflows/veille-news-openai.yml`** ✅
   - Exécution quotidienne à 6h Paris
   - Orchestration 2 agents en séquence
   - Gestion artifacts entre jobs

---

## 🎯 Thèmes couverts - Veille News

### Recherches Tavily (10 requêtes)
1. Actualités France semaine
2. Politique française actualité
3. Économie France entreprises
4. International Europe actualités
5. Écologie transition énergétique France
6. Actualités Nantes Pays de la Loire
7. Bretagne Belle-Île actualités
8. Technologie innovation France
9. Société France actualités
10. Mer littoral Atlantique actualités

### Classification des articles
- Politique française
- Économie & Entreprises
- International & Europe
- Écologie & Transition
- Société
- Technologie & Innovation
- Nantes & Région Ouest
- Culture

---

## 💰 Coûts estimés

### Par exécution
| Agent | Modèle | Tokens | Coût |
|-------|--------|--------|------|
| Agent 1 News | GPT-4o-mini | ~2500 | $0.001 |
| Agent 2 News | GPT-4o | ~6000 | $0.045 |
| **Total News** | - | ~8500 | **$0.046** |

### Total quotidien (IA + News)
| Veille | Coût/jour |
|--------|-----------|
| Veille IA | $0.065 |
| Veille News | $0.046 |
| **TOTAL** | **$0.111** |

**Coût mensuel** : ~3.33$ (~3€)
**Autonomie avec 25€** : **8.3 mois** ✅

---

## 🚀 Test du workflow News

### Instructions
1. **Va sur** : https://github.com/nliziard-ops/VeilleNLI/actions
2. **Clique** "Agents Veille News - OpenAI (2 agents)"
3. **Run workflow** → **Run workflow**

### Validation attendue
- [ ] ✅ Agent 1 : 10 recherches Tavily
- [ ] ✅ Agent 1 : ~80 articles bruts collectés
- [ ] ✅ Agent 1 : 8-12 articles filtrés
- [ ] ✅ Agent 1 : JSON créé
- [ ] ✅ Agent 2 : JSON chargé
- [ ] ✅ Agent 2 : Synthèse générée
- [ ] ✅ Agent 2 : Upload Google Drive réussi
- [ ] ✅ Fichier `VeilleNews.md` sur Google Drive

---

## 📊 État du projet

### ✅ Terminé

**Phase 1** : OpenAI API Key configurée
**Phase 2** : Agents Veille IA (2 agents OpenAI)
- ✅ Agent collecteur IA (GPT-4o-mini)
- ✅ Agent synthèse IA (GPT-4o)
- ✅ Workflow automatisé
- ✅ Output : `VeilleIA.md`

**Phase 3** : Agents Veille News (2 agents OpenAI)
- ✅ Agent collecteur News (GPT-4o-mini)
- ✅ Agent synthèse News (GPT-4o)
- ✅ Workflow automatisé
- ✅ Output : `VeilleNews.md`

### 🔜 Prochaines étapes

**Phase 4** : Frontend web
- [ ] Site web lisant `VeilleIA.md` + `VeilleNews.md`
- [ ] Proxy sécurisé Google Drive (GitHub Actions)
- [ ] Design sobre et élégant
- [ ] Déploiement GitHub Pages

**Phase 5** : Nettoyage
- [ ] Supprimer `agent_veille_ia.py` (Anthropic)
- [ ] Supprimer `agent_veille_news.py` (Anthropic)
- [ ] Supprimer `agent_generateur_web.py` (ancien)
- [ ] Désactiver workflow `agents-collecteurs.yml`
- [ ] Supprimer secret `ANTHROPIC_API_KEY`

---

## 📈 Architecture globale

```
┌─────────────────────────────────────────────────────────────┐
│                    VEILLE IA (quotidienne)                  │
├─────────────────────────────────────────────────────────────┤
│ Agent 1 (GPT-4o-mini) → Tavily → Filtrage → JSON           │
│ Agent 2 (GPT-4o) → Synthèse → VeilleIA.md → Google Drive   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                  VEILLE NEWS (quotidienne)                  │
├─────────────────────────────────────────────────────────────┤
│ Agent 1 (GPT-4o-mini) → Tavily → Filtrage → JSON           │
│ Agent 2 (GPT-4o) → Synthèse → VeilleNews.md → Google Drive │
└─────────────────────────────────────────────────────────────┘

                            ↓

┌─────────────────────────────────────────────────────────────┐
│              FRONTEND WEB (GitHub Pages)                    │
├─────────────────────────────────────────────────────────────┤
│ Lit VeilleIA.md + VeilleNews.md via proxy sécurisé         │
│ Affichage élégant avec navigation                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Métriques de succès

### Veille IA
- ✅ 12 recherches Tavily
- ✅ ~100 articles bruts
- ✅ 15-18 articles filtrés
- ✅ Synthèse ~22000 caractères
- ✅ 10-15 minutes de lecture

### Veille News
- 🔜 10 recherches Tavily
- 🔜 ~80 articles bruts
- 🔜 8-12 articles filtrés
- 🔜 Synthèse ~18000 caractères
- 🔜 10-12 minutes de lecture

---

## 📞 Support

**Repository** : https://github.com/nliziard-ops/VeilleNLI
**Commit Phase 3** : 1e9a6db8d4ddb792cd5a41269af9d47c93e6368d

---

*Généré le 2026-01-11 - Phase 3 terminée*
