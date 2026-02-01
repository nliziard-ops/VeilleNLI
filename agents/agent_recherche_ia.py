"""
Agent 1 - Recherche Web IA
Modèle : GPT-5.2 (OpenAI)
Rôle : Collecte factuelle d'informations depuis sites institutionnels IA avec web search LIVE
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

# Modèle GPT-5.2 avec web_search
MODEL_RECHERCHE = "gpt-5.2"

# Fichier de sortie
OUTPUT_JSON = "recherche_ia_brute.json"

# Sources institutionnelles IA
SOURCES_IA = [
    "https://www.anthropic.com",
    "https://openai.com",
    "https://mistral.ai",
    "https://www.deepseek.com",
    "https://thehackernews.com",
    "https://www.deeplearning.ai",
    "https://ai.google",
    "https://www.nvidia.com/en-us/ai/"
]


# ================================================================================
# RECHERCHE WEB AVEC GPT-5.2
# ================================================================================

def rechercher_actualites_ia() -> Dict[str, Any]:
    """
    Utilise GPT-5.2 avec web_search (LIVE WEB) pour collecter actualités IA.
    """
    
    if not OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY manquante")
        return {"articles": []}
    
    print(f"🔍 Création client OpenAI...")
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    date_fin = datetime.now()
    date_debut = date_fin - timedelta(days=7)
    
    sources_text = "\n".join([f"- {source}" for source in SOURCES_IA])
    
    prompt = f"""Tu es un collecteur d'informations factuelles sur l'IA.

**PÉRIODE** : du {date_debut.strftime('%d/%m/%Y')} au {date_fin.strftime('%d/%m/%Y')}

**SOURCES À CONSULTER** :
{sources_text}

**MISSION** :
Recherche 10-15 actualités IA publiées cette semaine.
Pour chaque actualité :
- Titre exact
- Résumé court (2-3 lignes) - FAITS UNIQUEMENT
- Synthèse complète (contenu factuel)
- Catégorie (Nouveaux modèles LLM, Agents autonomes, Multimodal, Reasoning, Open source, Recherche, Régulation, Safety, Industrie, Hardware, France/Europe, Asie)
- Source (nom du site)
- URL complète
- Date publication (YYYY-MM-DD)

**FORMAT JSON** :
{{
  "articles": [
    {{
      "categorie": "...",
      "titre": "...",
      "resume_court": "...",
      "synthese_complete": "...",
      "source": "...",
      "url": "https://...",
      "date_publication": "2026-02-01"
    }}
  ],
  "periode": {{"debut": "{date_debut.strftime('%Y-%m-%d')}", "fin": "{date_fin.strftime('%Y-%m-%d')}"}},
  "sources_consultees": []
}}

Réponds UNIQUEMENT en JSON, sans markdown."""

    print("🌐 Recherche web GPT-5.2 avec LIVE WEB...")
    
    try:
        # Appel Responses API avec web_search + LIVE WEB
        response = client.responses.create(
            model=MODEL_RECHERCHE,
            tools=[{"type": "web_search", "external_web_access": True}],  # LIVE WEB activé
            input=prompt,
            max_tokens=8000
        )
        
        print(f"📊 Tokens : {response.usage.total_tokens}")
        
        json_text = response.output_text.strip()
        
        # Nettoyer markdown si présent
        if json_text.startswith('```'):
            lines = json_text.split('\n')
            json_text = '\n'.join(lines[1:-1]) if len(lines) > 2 else json_text
            json_text = json_text.replace('```json', '').replace('```', '').strip()
        
        data = json.loads(json_text)
        
        # Ajouter métadonnées
        data['date_collecte'] = date_fin.strftime('%Y-%m-%d')
        data['model_utilise'] = MODEL_RECHERCHE
        data['agent'] = "Recherche IA"
        
        # Générer IDs
        for article in data.get('articles', []):
            hash_input = f"{article.get('url', '')}{article.get('titre', '')}"
            article['id'] = hashlib.md5(hash_input.encode()).hexdigest()[:12]
        
        print(f"✅ {len(data.get('articles', []))} articles collectés")
        
        return data
    
    except json.JSONDecodeError as e:
        print(f"❌ Erreur JSON : {e}")
        raise
    except Exception as e:
        print(f"❌ Erreur GPT-5.2 : {e}")
        traceback.print_exc()
        raise


def sauvegarder_json(data: Dict[str, Any], filepath: str) -> None:
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ {filepath} sauvegardé")


def main():
    try:
        print("=" * 80)
        print("🤖 AGENT 1 - RECHERCHE IA (GPT-5.2 + LIVE WEB)")
        print("=" * 80)
        
        data = rechercher_actualites_ia()
        sauvegarder_json(data, OUTPUT_JSON)
        
        print("✅ TERMINÉ")
        sys.exit(0)
    except Exception as e:
        print(f"❌ ERREUR : {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
