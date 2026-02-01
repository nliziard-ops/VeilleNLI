"""
Agent 1 - Recherche Web IA
Modèle : GPT-5.2 (OpenAI)
Rôle : Collecte factuelle d'informations depuis sites institutionnels IA
Sans interprétation ni analyse - Restitution brute : catégorie, titre, résumé, synthèse, source+lien
"""

import os
import sys
import json
import hashlib
import traceback
from datetime import datetime, timedelta
from typing import Dict, Any
from openai import OpenAI


# ================================================================================
# CONFIGURATION
# ================================================================================

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# Modèle GPT-5.2 pour recherche web avec web_search tool
MODEL_RECHERCHE = "gpt-5.2"

# Fichier de sortie
OUTPUT_JSON = "recherche_ia_brute.json"

# Sources institutionnelles IA (définies par Nicolas)
SOURCES_IA = [
    "https://www.anthropic.com",  # Anthropic (Claude)
    "https://openai.com",          # OpenAI (GPT)
    "https://mistral.ai",          # Mistral AI (France)
    "https://www.deepseek.com",    # DeepSeek (Chine)
    "https://thehackernews.com",   # The Hacker News
    "https://www.deeplearning.ai", # DeepLearning.AI
    "https://ai.google",           # Google AI (ajout institutionnel)
    "https://www.nvidia.com/en-us/ai/" # NVIDIA AI (ajout institutionnel)
]


# ================================================================================
# RECHERCHE WEB AVEC GPT-5.2
# ================================================================================

def rechercher_actualites_ia() -> Dict[str, Any]:
    """
    Utilise GPT-5.2 avec web_search tool (live web access) pour collecter
    les actualités factuelles depuis les sources institutionnelles IA.
    
    Returns:
        Dictionnaire JSON avec articles
    """
    
    if not OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY manquante")
        return {"articles": []}
    
    print(f"🔍 Création client OpenAI pour recherche web...")
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    # Calculer période (7 derniers jours)
    date_fin = datetime.now()
    date_debut = date_fin - timedelta(days=7)
    
    # Préparer liste sources
    sources_text = "\n".join([f"- {source}" for source in SOURCES_IA])
    
    # Construire prompt de recherche factuelle
    prompt = f"""Tu es un collecteur d'informations factuelles sur l'Intelligence Artificielle.

**PÉRIODE** : du {date_debut.strftime('%d/%m/%Y')} au {date_fin.strftime('%d/%m/%Y')}

**SOURCES PRIORITAIRES À CONSULTER** :
{sources_text}

**TA MISSION - COLLECTE FACTUELLE UNIQUEMENT** :
1. Recherche les actualités IA/LLM publiées cette semaine sur ces sources institutionnelles
2. Pour chaque actualité trouvée, extrais UNIQUEMENT les faits :
   - Titre exact de l'article
   - Résumé court (2-3 lignes) - FACTS ONLY, pas d'interprétation
   - Contenu factuel complet de l'article (qui, quoi, quand, où)
   - Source exacte (nom du site)
   - URL complète de l'article
   - Date de publication estimée

3. Catégorise chaque actualité dans l'un de ces thèmes :
   - "Nouveaux modèles LLM" (lancements, versions, benchmarks)
   - "Agents autonomes" (AutoGPT, frameworks agentiques)
   - "Multimodal" (vision, audio, vidéo)
   - "Reasoning" (o1, o3, R1, chaîne de pensée)
   - "Open source" (Llama, Mistral, communauté)
   - "Recherche" (papiers ArXiv, conférences)
   - "Régulation" (AI Act, gouvernance)
   - "Safety" (alignment, risques)
   - "Industrie" (levées de fonds, acquisitions)
   - "Hardware" (GPU, TPU, Groq)
   - "France/Europe" (acteurs français, régulation UE)
   - "Asie" (Chine, DeepSeek, Baidu)

**FORMAT DE SORTIE JSON - STRUCTURE OBLIGATOIRE** :
Réponds UNIQUEMENT avec un JSON valide suivant ce format exact :

{{
  "articles": [
    {{
      "categorie": "Nouveaux modèles LLM",
      "titre": "Titre exact de l'article",
      "resume_court": "Résumé factuel en 2-3 lignes maximum",
      "synthese_complete": "Contenu complet factuel",
      "source": "Nom du site (ex: Anthropic, OpenAI)",
      "url": "https://url-complete.com",
      "date_publication": "2026-02-01"
    }}
  ],
  "periode": {{
    "debut": "{date_debut.strftime('%Y-%m-%d')}",
    "fin": "{date_fin.strftime('%Y-%m-%d')}"
  }},
  "sources_consultees": ["Anthropic", "OpenAI"]
}}

**CONSIGNES CRITIQUES** :
- Recherche 10-15 actualités maximum
- UNIQUEMENT des faits vérifiables
- AUCUNE interprétation, analyse, opinion
- Citations exactes quand pertinent
- URLs complètes obligatoires

**IMPORTANT** :
Tu es un COLLECTEUR, pas un ANALYSTE. Tu ne portes AUCUN jugement.
Utilise web_search pour accéder aux sites institutionnels.
Génère le JSON maintenant, sans préambule."""

    print("🌐 Lancement recherche web GPT-5.2 avec web_search (LIVE WEB)...")
    
    try:
        # Appel API GPT-5.2 avec Responses API + web_search tool + LIVE WEB
        response = client.responses.create(
            model=MODEL_RECHERCHE,
            tools=[{"type": "web_search", "external_web_access": True}],  # LIVE WEB = True
            input=prompt,
            max_tokens=8000  # Spécifié par Nicolas
        )
        
        print(f"📊 Tokens utilisés : {response.usage.total_tokens} (prompt: {response.usage.prompt_tokens}, completion: {response.usage.completion_tokens})")
        
        # Coût GPT-5.2 (estimation, à vérifier)
        cost_input = (response.usage.prompt_tokens / 1000) * 0.01
        cost_output = (response.usage.completion_tokens / 1000) * 0.03
        cost_total = cost_input + cost_output
        print(f"💰 Coût estimé : ${cost_total:.4f}")
        
        # Extraire JSON depuis output_text
        json_text = response.output_text.strip()
        
        # Nettoyer les backticks markdown si présents
        if json_text.startswith('```'):
            lines = json_text.split('\n')
            json_text = '\n'.join(lines[1:-1]) if len(lines) > 2 else json_text
            json_text = json_text.replace('```json', '').replace('```', '').strip()
        
        print(f"📝 Parsing JSON ({len(json_text)} caractères)...")
        
        data = json.loads(json_text)
        
        # Ajouter métadonnées
        data['date_collecte'] = date_fin.strftime('%Y-%m-%d')
        data['model_utilise'] = MODEL_RECHERCHE
        data['agent'] = "Recherche IA"
        
        # Vérifier structure
        if 'periode' not in data:
            data['periode'] = {
                'debut': date_debut.strftime('%Y-%m-%d'),
                'fin': date_fin.strftime('%Y-%m-%d')
            }
        
        # Générer IDs uniques
        for article in data.get('articles', []):
            hash_input = f"{article.get('url', '')}{article.get('titre', '')}"
            article['id'] = hashlib.md5(hash_input.encode()).hexdigest()[:12]
        
        print(f"✅ Recherche terminée : {len(data.get('articles', []))} articles collectés")
        
        return data
    
    except json.JSONDecodeError as e:
        print(f"❌ Erreur parsing JSON : {e}")
        print(f"Réponse brute (premiers 500 car) : {json_text[:500]}...")
        raise
    
    except Exception as e:
        print(f"❌ Erreur GPT-5.2 : {e}")
        traceback.print_exc()
        raise


# ================================================================================
# SAUVEGARDE JSON
# ================================================================================

def sauvegarder_json(data: Dict[str, Any], filepath: str) -> None:
    """
    Sauvegarde le JSON de recherche brute
    
    Args:
        data: Données à sauvegarder
        filepath: Chemin du fichier
    """
    print(f"💾 Sauvegarde du JSON dans {filepath}...")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    file_size = os.path.getsize(filepath)
    print(f"✅ JSON sauvegardé : {filepath}")
    print(f"📊 Taille : {file_size} octets ({file_size / 1024:.2f} KB)")


# ================================================================================
# MAIN
# ================================================================================

def main():
    """Point d'entrée principal de l'agent recherche IA"""
    
    try:
        print("=" * 80)
        print("🤖 AGENT 1 - RECHERCHE WEB IA (GPT-5.2 + LIVE WEB SEARCH)")
        print("=" * 80)
        print(f"⏰ Exécution : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"📂 Répertoire de travail : {os.getcwd()}")
        print()
        
        # Vérifier clé API
        print("🔑 Vérification clé API...")
        if not OPENAI_API_KEY:
            print("❌ ERREUR CRITIQUE : OPENAI_API_KEY manquante")
            sys.exit(1)
        else:
            print(f"✅ OPENAI_API_KEY présente ({OPENAI_API_KEY[:10]}...)")
        
        print()
        
        # Recherche web
        print("📡 RECHERCHE WEB FACTUELLE IA (GPT-5.2)")
        print("-" * 80)
        print("Sources institutionnelles :")
        for source in SOURCES_IA:
            print(f"  • {source}")
        print()
        
        data = rechercher_actualites_ia()
        print()
        
        # Sauvegarde
        print("💾 SAUVEGARDE JSON")
        print("-" * 80)
        sauvegarder_json(data, OUTPUT_JSON)
        print()
        
        # Résumé
        print("=" * 80)
        print("✅ AGENT 1 RECHERCHE IA TERMINÉ")
        print("=" * 80)
        print(f"📊 {len(data.get('articles', []))} articles collectés")
        print(f"📂 Fichier JSON : {OUTPUT_JSON}")
        print(f"🔗 Prêt pour Agent 3 (Synthèse IA)")
        print()
        
        sys.exit(0)
    
    except KeyboardInterrupt:
        print("\n⚠️  Interruption manuelle (Ctrl+C)")
        sys.exit(130)
    
    except Exception as e:
        print("\n" + "=" * 80)
        print("❌ ERREUR FATALE")
        print("=" * 80)
        print(f"Type : {type(e).__name__}")
        print(f"Message : {e}")
        print("\nTraceback :")
        traceback.print_exc()
        print("=" * 80)
        sys.exit(1)


if __name__ == "__main__":
    main()
