"""
Agent Recherche News v3 - Collecte PURE
Modèle : GPT-5.2 (OpenAI Responses API)
Rôle : Collecte factuelle brute SANS tri, SANS analyse, SANS synthèse
Note : GPT-5.2 ne supporte pas max_tokens dans responses.create()
"""

import os
import sys
import json
import hashlib
import traceback
from datetime import datetime, timedelta
from typing import Dict, Any
from openai import OpenAI

# Configuration
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
MODEL_RECHERCHE = "gpt-5.2"
OUTPUT_JSON = "recherche_news_brute.json"
MAX_ARTICLES = 25

def collecter_actualites_news() -> Dict[str, Any]:
    if not OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY manquant")
        return {"articles": [], "erreur": "API key manquante"}
    
    client = OpenAI(api_key=OPENAI_API_KEY)
    date_fin = datetime.now()
    date_debut = date_fin - timedelta(days=7)
    
    prompt = f"""ROBOT COLLECTE - PAS D'ANALYSE

PÉRIODE: {date_debut.strftime('%d/%m/%Y')} → {date_fin.strftime('%d/%m/%Y')}

SOURCES: Le Grand Continent, El Pais, BBC, Reuters, Le Figaro, Le Monde, Monde Diplo, Ouest-France, Télégramme

COLLECTE: 20-{MAX_ARTICLES} actus

RÉPARTITION: 35% International | 35% National France | 30% Local Bretagne/Pays de Loire

POUR CHAQUE:
- titre
- url (https://...)
- source
- date_publication (YYYY-MM-DD)
- contenu_brut (résumé web search)
- zone_geo (International|National|Local)
- categorie_auto (Géopolitique|Économie mondiale|Environnement|Politique nationale|Économie France|Société|Politique locale|Économie régionale|Sports maritimes|Mer & littoral|Culture Bretagne)

JSON UNIQUEMENT:
{{
  "articles": [{{
    "titre": "...",
    "url": "https://...",
    "source": "...",
    "date_publication": "2026-02-01",
    "contenu_brut": "...",
    "zone_geo": "International",
    "categorie_auto": "..."
  }}],
  "periode": {{"debut": "{date_debut.strftime('%Y-%m-%d')}", "fin": "{date_fin.strftime('%Y-%m-%d')}"}},
  "nb_articles": 0
}}

LOCAL: Nantes, sports maritimes (voile, surf, kite, wingfoil).
PAS DE SÉLECTION. JSON BRUT SANS MARKDOWN."""

    print(f"🌐 Lancement GPT-5.2 + web search LIVE...")
    
    try:
        response = client.responses.create(
            model=MODEL_RECHERCHE,
            tools=[{"type": "web_search", "external_web_access": True}],
            input=prompt
        )
        
        tokens_used = response.usage.total_tokens
        print(f"📊 Tokens utilisés : {tokens_used}")
        
        json_text = response.output_text.strip()
        if json_text.startswith('```'):
            lines = json_text.split('\n')
            json_text = '\n'.join(lines[1:-1]) if len(lines) > 2 else json_text
            json_text = json_text.replace('```json', '').replace('```', '').strip()
        
        data = json.loads(json_text)
        
        data['date_collecte'] = date_fin.strftime('%Y-%m-%d')
        data['model_utilise'] = MODEL_RECHERCHE
        data['tokens_utilises'] = tokens_used
        data['agent'] = "Recherche News v3"
        data['nb_articles'] = len(data.get('articles', []))
        
        repartition = {'international': 0, 'national': 0, 'local': 0}
        
        for article in data.get('articles', []):
            hash_input = f"{article.get('url', '')}{article.get('titre', '')}"
            article['id'] = hashlib.md5(hash_input.encode()).hexdigest()[:12]
            
            zone = article.get('zone_geo', 'National')
            if zone == 'International':
                repartition['international'] += 1
            elif zone == 'Local':
                repartition['local'] += 1
            else:
                repartition['national'] += 1
        
        data['repartition'] = repartition
        
        print(f"✅ {data['nb_articles']} articles collectés")
        print(f"📍 {repartition['international']} Int | {repartition['national']} Nat | {repartition['local']} Local")
        return data
    
    except Exception as e:
        print(f"❌ Erreur : {e}")
        traceback.print_exc()
        raise

def main():
    try:
        print("=" * 80)
        print("🤖 AGENT RECHERCHE NEWS v3 - COLLECTE PURE")
        print("=" * 80)
        print(f"📅 Période : 7 derniers jours")
        print(f"🎯 Objectif : {MAX_ARTICLES} articles max")
        print(f"📍 Répartition : 35% Int | 35% Nat | 30% Local")
        print()
        
        data = collecter_actualites_news()
        
        with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print()
        print(f"✅ Fichier généré : {OUTPUT_JSON}")
        print(f"📊 {data['nb_articles']} articles • {data['tokens_utilises']} tokens")
        print("=" * 80)
        sys.exit(0)
    
    except Exception as e:
        print()
        print(f"❌ ÉCHEC : {e}")
        print("=" * 80)
        sys.exit(1)

if __name__ == "__main__":
    main()
