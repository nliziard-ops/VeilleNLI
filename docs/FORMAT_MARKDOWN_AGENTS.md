# FORMAT MARKDOWN POUR LES AGENTS DE VEILLE

## Vue d'ensemble

Ce document définit le format Markdown **OBLIGATOIRE** que tous les agents OpenAI doivent respecter pour générer les fichiers de veille (VeilleIA.md et VeilleNews.md).

## Structure globale du fichier

```markdown
---
agent: [Nom de l'agent]
date: YYYY-MM-DD
catégorie: [Catégorie principale]
---

# **Veille [Thématique] – Semaine du DD/MM/YYYY au DD/MM/YYYY**
**Édition [Nom créatif sobre]**

---

## **Introduction**

[Paragraphe de 3-4 lignes résumant le climat global, les tendances clés, les signaux faibles]

---

## **Table des matières**

1. [Catégorie 1]
2. [Catégorie 2]
...

---

## **[CATÉGORIE] – [Titre du sujet]**

### **Résumé**
[5 lignes max : faits essentiels, enjeux, impacts potentiels]

### **Points de vue croisés**

**Source 1 – [Nom du média/site]**
[Angle éditorial, analyse principale]

**Source 2 – [Nom du média/site]**
[Divergences, critiques, nuances]

**Source 3 – [Nom du média/site]**
[Apport complémentaire ou technique]

### **Fiabilité & signaux faibles**
- [Points incertains ou non confirmés]
- [Rumeurs à surveiller]
- [Indicateurs d'évolution ou risques]

### **Sources**
- [Titre source 1] – [URL]
- [Titre source 2] – [URL]
- [Titre source 3] – [URL]

---

[Répéter pour chaque sujet majeur - 10 à 15 sujets]

---

## **Synthèse finale**

### **Points clés de la semaine**
1. [Événement majeur 1]
2. [Événement majeur 2]
3. [Événement majeur 3]
4. [Événement majeur 4]
5. [Événement majeur 5]

### **Divergences d'analyse notables**
- [Point de désaccord entre sources]

### **Signaux faibles & opportunités**
- [Tendances émergentes]

### **Risques & menaces**
- [Points d'attention]

### **À surveiller la semaine prochaine**
- [Sujets en développement]

---

**Fin de l'édition**
```

## Règles de parsing

Le parser automatique extrait les sections selon ces règles :

### Sections principales (deviennent des "cards")
- **Détection** : Titre de niveau 2 commençant par `## **[CATÉGORIE] – `
- **Limite** : Les 6 premières sections après la Table des matières
- **Exclusions** : Introduction, Table des matières, Synthèse finale

### Sections secondaires (liste compacte)
- **Détection** : Toutes les sections après les 6 premières
- **Affichage** : Titre + début du résumé (200 caractères max)

### Points clés (synthèse finale)
- **Détection** : Section `## **Synthèse finale**` puis `### **Points clés de la semaine**`
- **Format** : Liste numérotée (1. 2. 3...) ou liste à puces (- ou •)
- **Limite** : Maximum 5 points extraits

## Contraintes obligatoires

### Markdown valide
- Pas de HTML dans le Markdown
- Utiliser uniquement Markdown standard (CommonMark)
- Échapper les caractères spéciaux si nécessaire

### Structure des titres
- **Niveau 1** (`#`) : Titre principal du document uniquement
- **Niveau 2** (`##`) : Catégories principales de sujets
- **Niveau 3** (`###`) : Sous-sections (Résumé, Points de vue croisés, etc.)
- **Niveau 4** (`####`) : À éviter, utiliser du texte en gras si nécessaire

### Sections obligatoires par sujet
1. `### **Résumé**` - OBLIGATOIRE
2. `### **Points de vue croisés**` - OBLIGATOIRE
3. `### **Fiabilité & signaux faibles**` - OPTIONNEL
4. `### **Sources**` - OBLIGATOIRE

### Format des sources
```markdown
### **Sources**
- Titre complet de l'article – https://url-complete.com
- Titre complet de l'article 2 – https://url-complete-2.com
```

**Interdictions** :
- ❌ Liens sans titre : `- https://url.com`
- ❌ Markdown dans les URLs : `[Titre](url)`
- ✅ Format correct : `- Titre – https://url.com`

## Résumé court vs complet

Le système génère automatiquement :
- **Résumé court** : 40 premiers mots du contenu de la section `### **Résumé**`
- **Résumé complet** : Totalité du contenu de `### **Résumé**`

**Conseil** : Rédiger le résumé entre 40 et 120 mots pour un bon équilibre.

## Flexibilité du format

### Nombre de sujets
- **Minimum** : 6 sujets (pour remplir les 6 cards principales)
- **Maximum** : Illimité (les sujets après le 6e iront en section secondaire)
- **Recommandé** : 10-15 sujets au total

### Nombre de sources
- **Minimum** : 3 sources par sujet
- **Recommandé** : 3-5 sources
- **Maximum** : Illimité

### Longueur des sections
- Aucune limite de longueur pour les sections
- Le parser extrait automatiquement ce dont il a besoin
- Privilégier la qualité et la précision

## Checklist de validation

Avant de soumettre un fichier Markdown, vérifier :

- [ ] Le fichier commence par un front matter YAML valide
- [ ] Le titre principal est de niveau 1 (`#`)
- [ ] Au moins 6 sujets sont présents avec structure complète
- [ ] Chaque sujet a une section `### **Résumé**`
- [ ] Chaque sujet a une section `### **Sources**` avec au moins 3 sources
- [ ] Les sources suivent le format : `- Titre – URL`
- [ ] La section `## **Synthèse finale**` est présente
- [ ] Les points clés sont au format liste numérotée ou à puces
- [ ] Aucun HTML n'est présent dans le Markdown
- [ ] Tous les liens sont valides (commencent par http:// ou https://)

## Notes d'implémentation

Ce format est conçu pour être :
- **Flexible** : nombre variable de sujets et de sources
- **Robuste** : le parser gère les variations mineures
- **Évolutif** : possibilité d'ajouter des sections sans casser le système
- **Lisible** : par l'humain ET par la machine

**Important** : Le parser est tolérant aux variations mineures, mais respecter ce format garantit un affichage optimal sur le site web.
