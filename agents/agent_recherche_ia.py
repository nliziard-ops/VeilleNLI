"""
Agent 1 - Recherche Web IA
Modèle : GPT-5.2 (OpenAI Responses API)
Rôle : Collecte factuelle avec web search LIVE
"""

import os
import sys
import json
import hashlib
import traceback
from datetime import datetime, timedelta
from typing import Dict, Any
from openai import OpenAI

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
MODEL_RECHERCHE = "gpt-5.2"
OUTPUT_JSON = "recherche_ia_brute.json"

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

def rechercher_actualites_ia() -> Dict[str, Any]:
    if not OPENAI_API_KEY:
        return {"articles": []}
    
    client = OpenAI(api_key=OPENAI_API_KEY)
    date_fin = datetime.now()
    date_debut = date_fin - timedelta(days=7)
    
    prompt = f"""Recherche actualités IA du {date_debut.strftime('%d/%m/%Y')} au {date_fin.strftime('%d/%m/%Y')}.

Sources : Anthropic, OpenAI, Mistral, DeepSeek, HackerNews, DeepLearning.AI, Google AI, NVIDIA AI

Collecte 10-15 actualités. Pour chaque :
- titre, resume_court (2-3 lignes), synthese_complete
- categorie (Nouveaux modèles LLM, Agents autonomes, Multimodal, Reasoning, Open source, Recherche, Régulation, Safety, Industrie, Hardware, France/Europe, Asie)
- source, url, date_publication (YYYY-MM-DD)

FORMAT JSON :
{{
  "articles": [{{
    "categorie": "...",
    "titre": "...",
    "resume_court": "...",
    "synthese_complete": "...",
    "source": "...",
    "url": "https://...",
    "date_publication": "2026-02-01"
  }}],
  "periode": {{"debut": "{date_debut.strftime('%Y-%m-%d')}", "fin": "{date_fin.strftime('%Y-%m-%d')}"}},
  "sources_consultees": []
}}

Réponds JSON uniquement, sans markdown."""

    print("🌐 GPT-5.2 + web search LIVE...")
    
    try:
        # SYNTAXE OFFICIELLE OPENAI - Responses API
        response = client.responses.create(
            model=MODEL_RECHERCHE,
            tools=[{"type": "web_search", "external_web_access": True}],  # LIVE WEB
            input=prompt,
            max_tokens=8000
        )
        
        print(f"📊 Tokens : {response.usage.total_tokens}")
        
        json_text = response.output_text.strip()
        if json_text.startswith('```'):
            lines = json_text.split('\n')
            json_text = '\n'.join(lines[1:-1]) if len(lines) > 2 else json_text
            json_text = json_text.replace('```json', '').replace('```', '').strip()
        
        data = json.loads(json_text)
        data['date_collecte'] = date_fin.strftime('%Y-%m-%d')
        data['model_utilise'] = MODEL_RECHERCHE
        data['agent'] = "Recherche IA"
        
        for article in data.get('articles', []):
            hash_input = f"{article.get('url', '')}{article.get('titre', '')}"
            article['id'] = hashlib.md5(hash_input.encode()).hexdigest()[:12]
        
        print(f"✅ {len(data.get('articles', []))} articles")
        return data
    
    except Exception as e:
        print(f"❌ Erreur : {e}")
        traceback.print_exc()
        raise

def main():
    try:
        print("=" * 80)
        print("🤖 AGENT 1 - GPT-5.2 + WEB SEARCH LIVE")
        print("=" * 80)
        
        data = rechercher_actualites_ia()
        
        with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print("✅ TERMINÉ")
        sys.exit(0)
    except Exception as e:
        print(f"❌ {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
