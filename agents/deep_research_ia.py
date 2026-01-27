"""
Agent de Veille IA avec Recherche Web
Modèle : GPT-5.2 avec web_search
Rôle : Recherche web sur actualités IA/LLM → Analyse → Synthèse Markdown
Budget estimé : ~0.10€ par exécution
"""

import os
import sys
import traceback
from datetime import datetime, timedelta
from typing import Dict, Any
from openai import OpenAI


# ================================================================================
# CONFIGURATION
# ================================================================================

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# Modèle GPT-5.2 avec web search
MODEL_GPT52 = "gpt-5.2"

# Fichier de sortie
OUTPUT_MARKDOWN = "research_ia.md"

# Timeout (recherches longues)
REQUEST_TIMEOUT = 600  # 10 minutes

# Limite tokens de sortie
MAX_OUTPUT_TOKENS = 2000


# ================================================================================
# PROMPT RECHERCHE WEB IA
# ================================================================================

def generer_prompt_recherche() -> str:
    """
    Génère le prompt pour recherche web IA avec synthèse
    
    Returns:
        Prompt optimisé pour recherche web + analyse + synthèse
    """
    
    date_fin = datetime.now()
    date_debut = date_fin - timedelta(days=7)
    
    prompt = f"""Tu es un analyste expert en IA/LLM. Ta mission comporte 3 étapes :

ÉTAPE 1 : RECHERCHE WEB
Utilise l'outil de recherche web pour trouver des articles RÉELS et RÉCENTS sur l'IA/LLM.
N'invente JAMAIS d'URLs fictives.

ÉTAPE 2 : ANALYSE
Analyse les articles trouvés pour identifier les plus pertinents.

ÉTAPE 3 : SYNTHÈSE MARKDOWN
Génère un document Markdown structuré avec les articles sélectionnés.

PÉRIMÈTRE GÉOGRAPHIQUE :
- États-Unis (OpenAI, Anthropic, Meta, Google)
- Europe (Mistral AI France, startups européennes)
- Asie (DeepSeek Chine, entreprises asiatiques)
- **FOCUS SPÉCIAL** : IA à Nantes et en Bretagne (startups, écosystème local, événements)

SOURCES PRIORITAIRES :
- **Blogs officiels** : OpenAI Blog, Anthropic Blog, Google AI Blog, Meta AI Blog
- **Publications éditeurs** : Mistral AI, Hugging Face, Stability AI
- **Recherche académique** : ArXiv, Papers with Code, conférences (NeurIPS, ICML)
- **Communiqués officiels** : annonces produits, levées de fonds
- **Médias tech** : TechCrunch, The Verge, Wired, VentureBeat
- **Éviter** : agrégateurs secondaires, contenus marketing, republications

THÈMES À COUVRIR :
1. Nouveaux modèles LLM (GPT, Claude, Gemini, Llama, Mistral, DeepSeek)
2. Agents autonomes et Agentic AI
3. Multimodal AI (vision, audio, vidéo)
4. Reasoning models (o1, o3, R1, chain-of-thought)
5. Open source et écosystèmes (Hugging Face, communauté)
6. Recherche scientifique (papers ArXiv, conférences)
7. Régulation et gouvernance (AI Act Europe, législations)
8. Safety, Alignment, risques IA
9. Investissements et industrie (levées de fonds, acquisitions)
10. Hardware IA (NVIDIA, AMD, TPU, Groq, puces spécialisées)
11. **Startups françaises et européennes** (focus Mistral AI, Poolside, etc.)
12. **IA Nantes et Bretagne** : écosystème local, startups, événements, recherche

STRATÉGIE DE RECHERCHE :
1. Effectue 15-20 recherches web ciblées sur les thèmes ci-dessus
2. Pour chaque thème, cherche "actualité [thème] dernière semaine"
3. Vérifie la date de publication des articles trouvés
4. Priorise les sources officielles et les annonces récentes
5. Pour Nantes/Bretagne : "actualité IA Nantes", "startup IA Bretagne", etc.

CRITÈRES DE SÉLECTION :
- Actualité des 7 derniers jours PRIORITAIRE
- Accepter analyses/rapports récents sur événements plus anciens si très pertinents
- EXCLURE : contenu republié/recyclé, annonces marketing mineures, tutoriels basiques
- PRIVILÉGIER : vraies nouveautés, annonces officielles, résultats de recherche, sources primaires
- **CRITICAL** : TOUTES les URLs DOIVENT être RÉELLES (trouvées par web search)

PÉRIODE ANALYSÉE : du {date_debut.strftime('%d/%m/%Y')} au {date_fin.strftime('%d/%m/%Y')}

FORMAT DE SORTIE MARKDOWN :

```markdown
# Veille IA - Recherche Web
Date : {date_fin.strftime('%Y-%m-%d')}
Période : {date_debut.strftime('%d/%m/%Y')} - {date_fin.strftime('%d/%m/%Y')}

## Articles identifiés

### [TITRE ARTICLE 1]
- **Source** : [Nom média ou blog officiel]
- **URL** : [URL complète RÉELLE trouvée via web search]
- **Date** : [Date publication RÉELLE]
- **Thème** : [Thème principal parmi les 12 ci-dessus]
- **Résumé** : [3-4 lignes synthétiques reformulées]
- **Pertinence** : [Score 1-10]
- **Tags** : [tag1, tag2, tag3]
- **Zone géo** : [USA/Europe/Asie/France/Nantes-Bretagne]

### [TITRE ARTICLE 2]
[...]

[Répéter pour TOUS les articles trouvés - viser 15-20 articles minimum]

## Statistiques de la recherche
- Nombre total d'articles : [X]
- Période couverte : {date_debut.strftime('%d/%m/%Y')} à {date_fin.strftime('%d/%m/%Y')}
- Nombre de recherches web effectuées : [X]
- Répartition thématique :
  - Nouveaux modèles : [X]
  - Agents : [X]
  - Multimodal : [X]
  - Reasoning : [X]
  - Open source : [X]
  - Recherche : [X]
  - Régulation : [X]
  - Safety : [X]
  - Investissements : [X]
  - Hardware : [X]
  - France/Europe : [X]
  - Nantes/Bretagne : [X]
- Répartition géographique :
  - USA : [X]
  - Europe : [X]
  - Asie : [X]
  - France : [X]
  - Nantes/Bretagne : [X]
- Sources utilisées : [Liste des principaux médias/blogs]
```

CONSIGNES CRITIQUES :
- UTILISE LA RECHERCHE WEB pour CHAQUE thème important
- Vise 15-20 articles de haute qualité MINIMUM
- Reformule TOUS les résumés (JAMAIS de copier-coller)
- **URLs complètes RÉELLES OBLIGATOIRES** (trouvées via web search)
- **N'INVENTE JAMAIS d'URLs** - si tu n'as pas trouvé d'article récent, indique-le
- Score pertinence strict : 9-10 = exceptionnel, 7-8 = important, 5-6 = intéressant, <5 = à filtrer
- Privilégie sources originales (blogs officiels OpenAI/Anthropic/Mistral, papers ArXiv, communiqués)
- Pour Nantes/Bretagne : chercher startups locales, événements IA, initiatives régionales
- Équilibre géographique : 50% USA, 30% Europe, 15% Asie, 5% Nantes/Bretagne

Effectue maintenant :
1. RECHERCHE WEB (15-20 recherches)
2. ANALYSE des résultats
3. SYNTHÈSE au format Markdown avec URLs RÉELLES
"""
    
    return prompt


# ================================================================================
# RECHERCHE WEB AVEC GPT-5.2
# ================================================================================

def executer_recherche_web() -> str:
    """
    Lance une recherche web via GPT-5.2, analyse et synthétise
    
    Returns:
        Markdown structuré avec articles trouvés et URLs réelles
    """
    
    if not OPENAI_API_KEY:
        raise ValueError("❌ OPENAI_API_KEY manquante")
    
    print("🤖 Initialisation client OpenAI...")
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    prompt = generer_prompt_recherche()
    
    print(f"🔍 Lancement recherche web GPT-5.2 (timeout {REQUEST_TIMEOUT}s)...")
    print("⏳ Cette recherche peut prendre 2-4 minutes...")
    print("🌐 Web search activé pour URLs réelles")
    print("📊 Étapes : Recherche → Analyse → Synthèse")
    
    try:
        # API GPT-5.2 : client.responses.create()
        # SYNTAXE CORRIGÉE selon documentation OpenAI
        response = client.responses.create(
            model=MODEL_GPT52,
            input=prompt,
            max_output_tokens=MAX_OUTPUT_TOKENS,
            temperature=0.3,  # Au niveau racine, pas dans generation_config
            tools=[{"type": "web_search"}]  # Liste d'outils, pas dict
        )
        
        # Récupération du contenu (GPT-5.2 format)
        markdown_content = response.output_text.strip()
        
        # Nettoyer les backticks markdown si présents
        if markdown_content.startswith('```markdown'):
            lines = markdown_content.split('\n')
            markdown_content = '\n'.join(lines[1:-1]) if len(lines) > 2 else markdown_content
            markdown_content = markdown_content.replace('```markdown', '').replace('```', '').strip()
        
        print(f"✅ Recherche et synthèse terminées")
        print(f"📊 Tokens générés : {response.usage.output_tokens}")
        print(f"📝 Markdown généré : {len(markdown_content)} caractères")
        
        return markdown_content
    
    except Exception as e:
        print(f"❌ Erreur lors de la recherche : {e}")
        traceback.print_exc()
        raise


# ================================================================================
# SAUVEGARDE MARKDOWN
# ================================================================================

def sauvegarder_markdown(contenu: str, filepath: str) -> None:
    """
    Sauvegarde le Markdown généré
    
    Args:
        contenu: Contenu Markdown
        filepath: Chemin du fichier
    """
    print(f"💾 Sauvegarde dans {filepath}...")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(contenu)
    
    file_size = os.path.getsize(filepath)
    print(f"✅ Fichier sauvegardé : {filepath}")
    print(f"📊 Taille : {file_size} octets ({file_size / 1024:.2f} KB)")


# ================================================================================
# MAIN
# ================================================================================

def main():
    """Point d'entrée principal"""
    
    try:
        print("=" * 80)
        print("🔍 VEILLE IA - GPT-5.2 avec Recherche Web")
        print("=" * 80)
        print(f"⏰ Exécution : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"📂 Répertoire : {os.getcwd()}")
        print()
        
        if not OPENAI_API_KEY:
            print("❌ ERREUR : OPENAI_API_KEY manquante")
            sys.exit(1)
        
        print("🔍 ÉTAPE 1/2 : Recherche web + Analyse + Synthèse")
        print("-" * 80)
        markdown = executer_recherche_web()
        print()
        
        print("💾 ÉTAPE 2/2 : Sauvegarde du résultat")
        print("-" * 80)
        sauvegarder_markdown(markdown, OUTPUT_MARKDOWN)
        print()
        
        print("=" * 80)
        print("✅ VEILLE IA TERMINÉE")
        print("=" * 80)
        print(f"📄 Fichier : {OUTPUT_MARKDOWN}")
        print(f"🔗 Prêt pour agent de mise en forme")
        print(f"✅ URLs réelles vérifiables (GPT-5.2 web_search)")
        print()
        
        sys.exit(0)
    
    except Exception as e:
        print("\n" + "=" * 80)
        print("❌ ERREUR FATALE")
        print("=" * 80)
        print(f"Type : {type(e).__name__}")
        print(f"Message : {e}")
        traceback.print_exc()
        print("=" * 80)
        sys.exit(1)


if __name__ == "__main__":
    main()
