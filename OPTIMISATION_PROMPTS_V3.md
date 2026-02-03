# 📋 Optimisation des Prompts - Agents Recherche v3

**Date** : 03/02/2026  
**Version** : v3.1 (optimisée)

---

## 🎯 Objectif

Améliorer la qualité et la précision de la collecte d'actualités en optimisant les prompts des agents de recherche IA et News.

---

## ✨ Améliorations Agent Recherche IA

### Sources enrichies

**Avant** : 8 sources génériques  
**Après** : 12 sources avec URLs précises

```
Ajout de :
- Hugging Face: huggingface.co/blog
- Meta AI: ai.meta.com/blog
- AWS AI/ML: aws.amazon.com/blogs/machine-learning
- The Hacker News (cybersecurity AI)
```

### Contraintes renforcées

- ✅ **EXACTEMENT 25 articles** (plus de fourchette 20-25)
- ✅ **URLs complètes et valides** obligatoires
- ✅ **Diversification** : max 3-4 articles par source
- ✅ **Exemple de résultat** fourni dans le prompt
- ✅ **Validation du format JSON** plus stricte

### Logging amélioré

```python
# Affichage de la répartition par catégorie
📊 Répartition par catégorie :
   • Nouveaux modèles LLM: 8
   • Open source: 5
   • Industrie & Applications: 4
   ...
```

---

## ✨ Améliorations Agent Recherche News

### Sources organisées par zone

**Avant** : Liste plate de 9 sources  
**Après** : Structuration claire par zone géographique

```
INTERNATIONAL (35% = 9 articles):
- Le Grand Continent, El País, BBC, Reuters, The Guardian

NATIONAL (35% = 9 articles):
- Le Figaro, Le Monde, Monde Diplo, Libération, Les Échos

LOCAL (30% = 7 articles):
- Ouest-France (Nantes), Le Télégramme (Bretagne), Presse Océan
```

### Répartition stricte

**Avant** : 35-35-30 (vague)  
**Après** : **9 Int + 9 Nat + 7 Local** (exact)

### Focus local détaillé

```
FOCUS LOCAL OBLIGATOIRE (7 articles) :
- Nantes : politique, économie, culture, projets urbains
- Sports maritimes : voile, surf, kitesurf, wingfoil
- Mer & littoral : ports, pêche, environnement marin
- Bretagne : initiatives, économie maritime, patrimoine
```

### Exemples concrets

Ajout de 3 exemples complets (1 par zone) pour guider GPT-5.2 :
- Exemple International (géopolitique Ukraine)
- Exemple National (réforme retraites)
- Exemple Local (pôle nautique Nantes)

### Validation renforcée

```python
# Vérification de la répartition locale
if repartition['local'] < 5:
    print(f"⚠️  Attention : seulement {repartition['local']} articles locaux")
```

---

## 📊 Comparaison Avant/Après

| Critère | Avant v3.0 | Après v3.1 |
|---------|------------|------------|
| **Sources IA** | 8 génériques | 12 avec URLs précises |
| **Sources News** | 9 liste plate | 15 structurées par zone |
| **Nombre articles** | 20-25 variable | 25 exactement |
| **Répartition News** | 35-35-30 (%) | 9-9-7 (exact) |
| **Exemples** | 0 | 4 (1 IA + 3 News) |
| **Validation** | Basique | Stricte + alertes |
| **Logging** | Minimal | Détaillé par catégorie |

---

## 🎯 Bénéfices Attendus

### Pour l'Agent IA

1. **Diversité** : Meilleures sources (Hugging Face, Meta AI, AWS)
2. **Fraîcheur** : URLs précises vers blogs officiels
3. **Qualité** : Limite par source évite la surreprésentation
4. **Traçabilité** : Logs détaillés par catégorie

### Pour l'Agent News

1. **Respect de la répartition** : 9-9-7 au lieu de ~35-35-30
2. **Focus local renforcé** : Consignes précises (Nantes, sports maritimes)
3. **Diversité sujets** : Catégories détaillées par zone
4. **Guidance** : 3 exemples concrets pour GPT-5.2

---

## 🔧 Impact sur les Coûts

**Aucun impact négatif** :
- Tokens utilisés : similaires (~10k par agent)
- Temps d'exécution : comparable
- Qualité attendue : **meilleure**

---

## 🧪 Tests Recommandés

### Après déploiement

1. **Lancer le workflow** manuellement
2. **Vérifier les logs** :
   - Nombre exact d'articles (25 pour chaque agent)
   - Répartition News (9-9-7)
   - Diversité des sources
3. **Comparer avec version précédente** :
   - Qualité des URLs
   - Pertinence du contenu local
   - Fraîcheur des articles IA

---

## 📝 Notes

- Les prompts sont plus longs mais **plus précis**
- GPT-5.2 bénéficie des exemples concrets
- La validation stricte permet de détecter rapidement les problèmes
- Les logs améliorés facilitent le debug

---

*Optimisation réalisée le 03/02/2026*
