"""
Agent Deep Research IA
Modèle : GPT-4o avec web_search activé
Rôle : Recherche approfondie sur actualités IA/LLM → Markdown structuré
Budget estimé : ~0.05-0.10€ par recherche
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

# Modèle avec web search
MODEL_DEEP_RESEARCH = "gpt-4o"  # GPT-4o avec capacité web_search

# Fichier de sortie
OUTPUT_MARKDOWN = "research_ia.md"

# Timeout (recherches longues)
REQUEST_TIMEOUT = 600  # 10 minutes


# ================================================================================
# PROMPT DEEP RESEARCH IA
# ================================================================================

def generer_prompt_deep_research() -> str:
    """
    Génère le prompt pour Deep Research IA avec web search
    
    Returns:
        Prompt optimisé pour recherche web
    """
    
    date_fin = datetime.now()
    date_debut = date_fin - timedelta(days=7)
    
    prompt = f"""Tu es un analyste expert en IA/LLM qui effectue une recherche web approfondie sur les développements récents en intelligence artificielle.

IMPORTANT : Tu DOIS utiliser la recherche web pour trouver des articles RÉELS et RÉCENTS. N'invente JAMAIS d'URLs fictives.

OBJECTIF : Identifier et analyser les actualités IA/LLM IMPORTANTES des 7 derniers jours en utilisant la recherche web.

PÉRIMÈTRE GÉOGRAPHIQUE :
- États-Unis (OpenAI, Anthropic, Meta, Google)
- Europe (Mistral AI France, startups européennes)
- Asie (DeepSeek Chine, entreprises asiatiques)
- **FOCUS SPÉCIAL** : IA à Nantes et en Bretagne (startups, écosystème local, événements)

SOURCES PRIORITAIRES - UTILISER LA RECHERCHE WEB POUR TROUVER :
- **Blogs officiels** : OpenAI Blog, Anthropic Blog, Google AI Blog, Meta AI Blog
- **Publications éditeurs** : Mistral AI, Hugging Face, Stability AI
- **Recherche académique** : ArXiv, Papers with Code, conférences (NeurIPS, ICML)
- **Communiqués officiels** : annonces produits, levées de fonds
- **Médias tech de référence** : TechCrunch, The Verge, Wired, VentureBeat
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

STRATÉGIE DE RECHERCHE WEB :
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
- **CRITICAL** : TOUTES les URLs DOIVENT être RÉELLES (vérifiées par web search)

PÉRIODE ANALYSÉE : du {date_debut.strftime('%d/%m/%Y')} au {date_fin.strftime('%d/%m/%Y')}

FORMAT DE SORTIE MARKDOWN :

```markdown
# Recherche Deep - Veille IA
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

Effectue ta recherche web approfondie maintenant et génère le Markdown complet avec URLs RÉELLES.
"""
    
    return prompt


# ================================================================================
# DEEP RESEARCH AVEC GPT-4o + WEB SEARCH
# ================================================================================

def executer_deep_research() -> str:
    """
    Lance une recherche approfondie via GPT-4o avec web_search
    
    Returns:
        Markdown structuré avec articles trouvés et URLs réelles
    """
    
    if not OPENAI_API_KEY:
        raise ValueError("❌ OPENAI_API_KEY manquante")
    
    print("🤖 Initialisation client OpenAI...")
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    prompt = generer_prompt_deep_research()
    
    print(f"🔍 Lancement Deep Research avec web_search (timeout {REQUEST_TIMEOUT}s)...")
    print("⏳ Cette recherche peut prendre 2-4 minutes...")
    print("🌐 Web search activé pour URLs réelles")
    
    try:
        response = client.chat.completions.create(
            model=MODEL_DEEP_RESEARCH,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            tools=[
                {
                    "type": "web_search"
                }
            ],
            timeout=REQUEST_TIMEOUT
        )
        
        markdown_content = response.choices[0].message.content.strip()
        
        # Nettoyer les backticks markdown si présents
        if markdown_content.startswith('```markdown'):
            lines = markdown_content.split('\n')
            markdown_content = '\n'.join(lines[1:-1]) if len(lines) > 2 else markdown_content
            markdown_content = markdown_content.replace('```markdown', '').replace('```', '').strip()
        
        print(f"✅ Recherche terminée")
        print(f"📊 Tokens utilisés : {response.usage.total_tokens}")
        
        # Estimation coût GPT-4o
        # gpt-4o : ~$2.50/1M input tokens, ~$10/1M output tokens
        cost_input = (response.usage.prompt_tokens / 1_000_000) * 2.50
        cost_output = (response.usage.completion_tokens / 1_000_000) * 10
        cost_total = cost_input + cost_output
        
        print(f"💰 Coût estimé : ${cost_total:.4f} (GPT-4o + web_search)")
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
        print("🔬 DEEP RESEARCH IA - GPT-4o avec Web Search")
        print("=" * 80)
        print(f"⏰ Exécution : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"📂 Répertoire : {os.getcwd()}")
        print()
        
        if not OPENAI_API_KEY:
            print("❌ ERREUR : OPENAI_API_KEY manquante")
            sys.exit(1)
        
        print("🔍 ÉTAPE 1/2 : Deep Research avec web_search en cours...")
        print("-" * 80)
        markdown = executer_deep_research()
        print()
        
        print("💾 ÉTAPE 2/2 : Sauvegarde du résultat")
        print("-" * 80)
        sauvegarder_markdown(markdown, OUTPUT_MARKDOWN)
        print()
        
        print("=" * 80)
        print("✅ DEEP RESEARCH IA TERMINÉ")
        print("=" * 80)
        print(f"📄 Fichier : {OUTPUT_MARKDOWN}")
        print(f"🔗 Prêt pour agent de mise en forme")
        print(f"✅ URLs réelles vérifiables (web_search activé)")
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
