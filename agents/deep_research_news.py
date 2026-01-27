"""
Agent Deep Research News
Modèle : GPT-5.2 avec web_search activé
Rôle : Recherche approfondie actualités générales + sport maritime → Markdown structuré
Budget estimé : Variable selon usage
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
MODEL_DEEP_RESEARCH = "gpt-5.2"

# Fichier de sortie
OUTPUT_MARKDOWN = "research_news.md"

# Timeout (recherches longues)
REQUEST_TIMEOUT = 600  # 10 minutes

# Limite tokens de sortie
MAX_OUTPUT_TOKENS = 2000


# ================================================================================
# PROMPT DEEP RESEARCH NEWS
# ================================================================================

def generer_prompt_deep_research() -> str:
    """
    Génère le prompt pour Deep Research News avec web search
    
    Returns:
        Prompt optimisé pour recherche web actualités
    """
    
    date_fin = datetime.now()
    date_debut = date_fin - timedelta(days=7)
    
    prompt = f"""Tu es un journaliste expert qui effectue une recherche web approfondie sur l'actualité générale et sportive.

IMPORTANT : Tu DOIS utiliser la recherche web pour trouver des articles RÉELS et RÉCENTS. N'invente JAMAIS d'URLs fictives.

OBJECTIF : Identifier les actualités IMPORTANTES des 7 derniers jours en utilisant la recherche web.

PÉRIMÈTRE GÉOGRAPHIQUE :

**International :**
- Europe : France, Royaume-Uni, Allemagne, Union Européenne
- États-Unis
- Asie : Chine, Japon, Inde

**National France :**
- Actualités nationales françaises (politique, économie, société, culture)

**Local Bretagne et Pays de la Loire :**
- Bretagne (toute la région : Finistère, Côtes-d'Armor, Morbihan, Ille-et-Vilaine)
- Pays de la Loire (Loire-Atlantique, Maine-et-Loire, Mayenne, Sarthe, Vendée)
- **Focus spécifiques** : Belle-Île-en-Mer, Nantes, Saint-Nazaire, Brest, Lorient

THÈMES À COUVRIR :

**1. Actualités générales (60% du contenu) :**
- Politique (national et international)
- Économie et finance
- Société et culture
- Environnement et climat
- Technologie (hors IA déjà couverte ailleurs)
- Santé et sciences
- Justice et sécurité

**2. Sport maritime et nautique (40% du contenu) :**
- **Voile et course au large** : Vendée Globe, Ocean Race, Route du Rhum, transat, records
- **Surf** : compétitions, spots, championnats
- **Planche à voile** : événements, championnats
- **Kitesurf** : compétitions, spots bretons
- **Wingfoil** : discipline émergente, événements
- **Événements nautiques locaux** : régates Bretagne/Atlantique, manifestations maritimes

STRATÉGIE DE RECHERCHE WEB :
1. Effectue 15-20 recherches web ciblées sur différents thèmes et zones géographiques
2. Pour actualités générales : "actualité [thème] dernière semaine France"
3. Pour sport maritime : "actualité voile", "compétition surf Bretagne", "régates Atlantique"
4. Pour local : "actualité Nantes dernière semaine", "actualité Bretagne", "Belle-Île-en-Mer"
5. Vérifie la date de publication des articles trouvés
6. Priorise sources fiables : AFP, Reuters, Le Monde, Ouest-France, médias locaux

CRITÈRES DE SÉLECTION :
- Actualité des 7 derniers jours STRICTEMENT
- Importance : événements majeurs, décisions politiques, faits marquants
- **ÉQUILIBRE GÉOGRAPHIQUE** : 
  - 35% International (Europe/USA/Asie)
  - 35% National France
  - 30% Local (Bretagne/Pays de la Loire/Nantes/Belle-Île)
- **ÉQUILIBRE THÉMATIQUE** :
  - 60% Actualités générales
  - 40% Sport maritime
- **CRITICAL** : TOUTES les URLs DOIVENT être RÉELLES (vérifiées par web search)

PÉRIODE ANALYSÉE : du {date_debut.strftime('%d/%m/%Y')} au {date_fin.strftime('%d/%m/%Y')}

FORMAT DE SORTIE MARKDOWN :

# Recherche Deep - Actualités
Date : {date_fin.strftime('%Y-%m-%d')}
Période : {date_debut.strftime('%d/%m/%Y')} - {date_fin.strftime('%d/%m/%Y')}

## Articles identifiés

### [TITRE ARTICLE 1]
- **Source** : [Nom média]
- **URL** : [URL complète RÉELLE trouvée via web search]
- **Date** : [Date publication RÉELLE]
- **Catégorie** : [International/National/Local/Sport maritime]
- **Thème** : [Politique/Économie/Sport/Société/etc.]
- **Résumé** : [3-4 lignes synthétiques]
- **Pertinence** : [Score 1-10]
- **Zone géo** : [Europe/USA/Asie/France/Bretagne/Nantes/Belle-Île/Pays-de-Loire]

### [TITRE ARTICLE 2]
[...]

[Répéter pour TOUS les articles trouvés - viser 20-25 articles minimum]

## Statistiques de la recherche
- Nombre total d'articles : [X]
- Période couverte : {date_debut.strftime('%d/%m/%Y')} à {date_fin.strftime('%d/%m/%Y')}
- Nombre de recherches web effectuées : [X]
- Répartition géographique :
  - International : [X] articles
  - National France : [X] articles
  - Local (Bretagne/Pays de la Loire) : [X] articles
- Répartition thématique :
  - Politique : [X]
  - Économie : [X]
  - Société : [X]
  - Environnement : [X]
  - Sport maritime : [X]
  - Santé : [X]
  - Autres : [X]
- Sport maritime détail :
  - Voile/course au large : [X]
  - Surf : [X]
  - Planche à voile : [X]
  - Kitesurf : [X]
  - Wingfoil : [X]
- Sources utilisées : [Liste des principaux médias]

CONSIGNES CRITIQUES :
- UTILISE LA RECHERCHE WEB pour CHAQUE zone géographique et thème
- Vise 20-25 articles équilibrés MINIMUM
- **Sport maritime** : MINIMUM 8-10 articles si actualités disponibles
- **Local Bretagne/Nantes/Belle-Île** : MINIMUM 6-7 articles
- **National France** : MINIMUM 8-10 articles
- **URLs complètes RÉELLES OBLIGATOIRES** (trouvées via web search)
- **N'INVENTE JAMAIS d'URLs** - si tu n'as pas trouvé d'article récent, indique-le
- Reformule TOUS les résumés (JAMAIS de copier-coller)
- Score pertinence : 9-10 = événement majeur, 7-8 = important, 5-6 = intéressant
- Privilégie diversité thématique ET géographique
- Pour sport maritime : chercher Vendée Globe, régates locales, compétitions surf Bretagne
- Pour local : Ouest-France, Presse-Océan, médias régionaux

Effectue ta recherche web approfondie maintenant et génère le Markdown complet avec URLs RÉELLES.
"""
    
    return prompt


# ================================================================================
# DEEP RESEARCH AVEC GPT-5.2 + WEB SEARCH
# ================================================================================

def executer_deep_research() -> str:
    """
    Lance une recherche approfondie via GPT-5.2 avec web_search
    
    Returns:
        Markdown structuré avec articles trouvés et URLs réelles
    """
    
    if not OPENAI_API_KEY:
        raise ValueError("❌ OPENAI_API_KEY manquante")
    
    print("🤖 Initialisation client OpenAI...")
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    prompt = generer_prompt_deep_research()
    
    print(f"🔍 Lancement Deep Research GPT-5.2 avec web_search (timeout {REQUEST_TIMEOUT}s)...")
    print("⏳ Cette recherche peut prendre 2-4 minutes...")
    print("🌐 Web search activé pour URLs réelles")
    
    try:
        # API GPT-5.2 : client.responses.create()
        # SYNTAXE CORRIGÉE : generation_config pour les paramètres de génération
        response = client.responses.create(
            model=MODEL_DEEP_RESEARCH,
            input=prompt,  # Format GPT-5.2 : input au lieu de messages
            max_output_tokens=MAX_OUTPUT_TOKENS,
            tools={
                "web_search": {}  # Active l'outil de recherche web GPT-5.2
            },
            tool_choice="auto",
            generation_config={
                "temperature": 0.3,
                "presence_penalty": 0.2,
                "frequency_penalty": 0.0
            },
            response_format={
                "type": "text"
            }
        )
        
        # Récupération du contenu GPT-5.2 : response.output_text
        markdown_content = response.output_text.strip()
        
        # Nettoyer les backticks markdown si présents
        if markdown_content.startswith('```markdown'):
            lines = markdown_content.split('\n')
            markdown_content = '\n'.join(lines[1:-1]) if len(lines) > 2 else markdown_content
            markdown_content = markdown_content.replace('```markdown', '').replace('```', '').strip()
        
        print(f"✅ Recherche terminée")
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
        print("📰 DEEP RESEARCH NEWS - GPT-5.2 avec Web Search")
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
        print("✅ DEEP RESEARCH NEWS TERMINÉ")
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
