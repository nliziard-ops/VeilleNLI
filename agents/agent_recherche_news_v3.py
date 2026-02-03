"""
Agent Recherche News v3 - Collecte PURE
Modèle : GPT-5.2 (OpenAI Responses API)
Rôle : Collecte factuelle brute SANS tri, SANS analyse, SANS synthèse
Budget : 10000 tokens max
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
MAX_TOKENS = 10000
OUTPUT_JSON = "recherche_news_brute.json"
MAX_ARTICLES = 25

# Sources News prioritaires
SOURCES_NEWS = [
    "https://legrandcontinent.eu/fr/",
    "https://elpais.com/",
    "https://www.bbc.com/news",
    "https://www.reuters.com",
    "https://www.lefigaro.fr/",
    "https://www.lemonde.fr/",
    "https://www.monde-diplomatique.fr/",
    "https://www.ouest-france.fr/",
    "https://www.letelegramme.fr/"
]


def collecter_actualites_news() -> Dict[str, Any]:
    """
    Collecte brute des actualités News via web search.
    AUCUNE analyse, AUCUN tri, AUCUNE synthèse.
    """
    if not OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY manquant")
        return {"articles": [], "erreur": "API key manquante"}
    
    client = OpenAI(api_key=OPENAI_API_KEY)
    date_fin = datetime.now()
    date_debut = date_fin - timedelta(days=7)
    
    # Prompt de collecte PURE (pas d'analyse)
    prompt = f"""Tu es un robot de collecte d'actualités. Tu ne fais AUCUNE analyse.

PÉRIODE : du {date_debut.strftime('%d/%m/%Y')} au {date_fin.strftime('%d/%m/%Y')}

SOURCES PRIORITAIRES :
- Le Grand Continent, El Pais, BBC, Reuters
- Le Figaro, Le Monde, Monde Diplomatique
- Ouest-France, Le Télégramme
- Sites d'actualités généralistes internationaux

MISSION : Collecte 20-{MAX_ARTICLES} actualités récentes.

RÉPARTITION CIBLE :
- 35% International (géopolitique, économie mondiale, environnement global)
- 35% National France (politique, économie, société françaises)
- 30% Local Bretagne/Pays de Loire (Nantes, Brest, Belle-Île, sports maritimes : voile, surf, kitesurf, wingfoil)

Pour CHAQUE actualité trouvée, retourne :
- titre : titre exact de l'article
- url : URL complète
- source : nom du site
- date_publication : YYYY-MM-DD (estimation si pas trouvée)
- contenu_brut : le contenu textuel complet que tu as trouvé (résumé automatique du web search)
- zone_geo : "International" OU "National" OU "Local"
- categorie_auto : catégorie automatique (Géopolitique, Économie mondiale, Environnement, Politique nationale, Économie France, Société, Politique locale, Économie régionale, Sports maritimes, Mer & littoral, Culture Bretagne)

FORMAT JSON STRICT :
{{
  "articles": [
    {{
      "titre": "...",
      "url": "https://...",
      "source": "...",
      "date_publication": "2026-02-01",
      "contenu_brut": "Le contenu complet trouvé...",
      "zone_geo": "International",
      "categorie_auto": "..."
    }}
  ],
  "periode": {{
    "debut": "{date_debut.strftime('%Y-%m-%d')}",
    "fin": "{date_fin.strftime('%Y-%m-%d')}"
  }},
  "nb_articles": 0
}}

IMPORTANT :
- Ne fais AUCUNE sélection, collecte TOUT ce que tu trouves
- Ne fais AUCUNE analyse qualitative
- Ne génère AUCUNE synthèse
- Retourne le JSON brut uniquement, sans markdown
- Pour Local : focus sur Nantes, sports maritimes (voile, surf, kite, wingfoil)
"""

    print(f"🌐 Lancement GPT-5.2 + web search LIVE (max {MAX_TOKENS} tokens)...")
    
    try:
        # Appel OpenAI Responses API avec web search LIVE
        response = client.responses.create(
            model=MODEL_RECHERCHE,
            tools=[{"type": "web_search", "external_web_access": True}],
            input=prompt,
            max_tokens=MAX_TOKENS
        )
        
        tokens_used = response.usage.total_tokens
        print(f"📊 Tokens utilisés : {tokens_used}/{MAX_TOKENS}")
        
        # Nettoyage du JSON
        json_text = response.output_text.strip()
        if json_text.startswith('```'):
            lines = json_text.split('\n')
            json_text = '\n'.join(lines[1:-1]) if len(lines) > 2 else json_text
            json_text = json_text.replace('```json', '').replace('```', '').strip()
        
        # Parse JSON
        data = json.loads(json_text)
        
        # Enrichissement des métadonnées
        data['date_collecte'] = date_fin.strftime('%Y-%m-%d')
        data['model_utilise'] = MODEL_RECHERCHE
        data['tokens_utilises'] = tokens_used
        data['agent'] = "Recherche News v3"
        data['nb_articles'] = len(data.get('articles', []))
        
        # Comptage répartition géographique
        repartition = {'international': 0, 'national': 0, 'local': 0}
        
        # Génération ID unique pour chaque article
        for article in data.get('articles', []):
            hash_input = f"{article.get('url', '')}{article.get('titre', '')}"
            article['id'] = hashlib.md5(hash_input.encode()).hexdigest()[:12]
            
            # Comptage zone géo
            zone = article.get('zone_geo', 'National')
            if zone == 'International':
                repartition['international'] += 1
            elif zone == 'Local':
                repartition['local'] += 1
            else:
                repartition['national'] += 1
        
        data['repartition'] = repartition
        
        print(f"✅ {data['nb_articles']} articles collectés")
        print(f"📍 Répartition : {repartition['international']} Int | {repartition['national']} Nat | {repartition['local']} Local")
        
        if data['nb_articles'] == 0:
            print("⚠️  ATTENTION : Aucun article trouvé")
        
        return data
    
    except json.JSONDecodeError as e:
        print(f"❌ Erreur JSON : {e}")
        print(f"Réponse brute : {response.output_text[:500]}...")
        traceback.print_exc()
        raise
    
    except Exception as e:
        print(f"❌ Erreur : {e}")
        traceback.print_exc()
        raise


def main():
    """Point d'entrée principal"""
    try:
        print("=" * 80)
        print("🤖 AGENT RECHERCHE NEWS v3 - COLLECTE PURE")
        print("=" * 80)
        print(f"📅 Période : 7 derniers jours")
        print(f"🎯 Objectif : {MAX_ARTICLES} articles max")
        print(f"💰 Budget : {MAX_TOKENS} tokens max")
        print(f"📍 Répartition : 35% Int | 35% Nat | 30% Local")
        print()
        
        # Collecte
        data = collecter_actualites_news()
        
        # Sauvegarde JSON
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
