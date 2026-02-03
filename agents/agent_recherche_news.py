"""
Agent 2 - Recherche Web News (COLLECTE PURE)
Modèle : GPT-5.2 (OpenAI Responses API)
Rôle : Collecte factuelle brute avec web search LIVE - AUCUNE analyse
Budget : 10 000 tokens maximum
"""

import os
import sys
import json
import hashlib
import traceback
from datetime import datetime, timedelta
from typing import Dict, Any, List
from openai import OpenAI

# ============================================
# CONFIGURATION
# ============================================
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
MODEL_RECHERCHE = "gpt-5.2"
MAX_TOKENS = 10000  # Budget strict
OUTPUT_JSON = "recherche_news_brute.json"

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

# ============================================
# FONCTION PRINCIPALE
# ============================================
def collecter_actualites_news_brutes() -> Dict[str, Any]:
    """
    Collecte brute d'actualités News via GPT-5.2 + web search LIVE.
    
    Contraintes :
    - AUCUNE analyse, AUCUN tri, AUCUNE synthèse
    - Retour JSON simple : titre, url, source, date, contenu_brut
    - Budget : 10 000 tokens maximum
    
    Returns:
        Dict contenant liste d'articles bruts
    """
    if not OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY manquante")
        return {"articles": [], "erreur": "API key manquante"}
    
    client = OpenAI(api_key=OPENAI_API_KEY)
    date_fin = datetime.now()
    date_debut = date_fin - timedelta(days=7)
    
    # Prompt ULTRA-SIMPLE : collecte brute uniquement
    prompt = f"""Tu es un robot collecteur d'actualités générales.

PÉRIODE : {date_debut.strftime('%d/%m/%Y')} au {date_fin.strftime('%d/%m/%Y')}

SOURCES PRIORITAIRES :
- Le Grand Continent (legrandcontinent.eu)
- El Pais (elpais.com)
- BBC News (bbc.com/news)
- Reuters (reuters.com)
- Le Figaro (lefigaro.fr)
- Le Monde (lemonde.fr)
- Monde Diplomatique (monde-diplomatique.fr)
- Ouest-France (ouest-france.fr)
- Le Télégramme (letelegramme.fr)

RÉPARTITION GÉOGRAPHIQUE :
- 35% International (géopolitique mondiale, économie internationale, environnement global)
- 35% National France (politique française, économie nationale, société)
- 30% Local Bretagne/Pays de Loire (Nantes, Brest, Belle-Île, voile, surf, kitesurf, wingfoil, mer & littoral)

INSTRUCTIONS :
1. Collecte TOUTES les actualités de la semaine (25-35 articles)
2. Pour chaque article trouvé, extrais UNIQUEMENT :
   - titre (string)
   - url (string, URL complète)
   - source (string, nom du site)
   - date_publication (string, format YYYY-MM-DD)
   - contenu_brut (string, texte complet de l'article ou résumé long si disponible)

3. NE FAIS PAS :
   - Analyse
   - Tri par importance
   - Synthèse
   - Résumé court
   - Catégorisation

FORMAT JSON STRICT (réponds UNIQUEMENT ce JSON, sans markdown) :
{{
  "articles": [
    {{
      "titre": "Titre exact de l'article",
      "url": "https://example.com/article",
      "source": "Nom du site",
      "date_publication": "2026-02-01",
      "contenu_brut": "Texte complet ou résumé long de l'article..."
    }}
  ]
}}

Collecte le maximum d'articles dans la limite des 10 000 tokens.
Réponds JSON uniquement, sans ```json ni commentaires."""

    print(f"🔍 Lancement collecte News (budget: {MAX_TOKENS} tokens)...")
    
    try:
        # Appel API OpenAI Responses avec web search LIVE
        response = client.responses.create(
            model=MODEL_RECHERCHE,
            tools=[{"type": "web_search", "external_web_access": True}],
            input=prompt,
            max_tokens=MAX_TOKENS
        )
        
        tokens_utilises = response.usage.total_tokens
        print(f"📊 Tokens utilisés : {tokens_utilises}/{MAX_TOKENS}")
        
        # Nettoyage JSON (suppression markdown si présent)
        json_text = response.output_text.strip()
        if json_text.startswith('```'):
            lines = json_text.split('\n')
            json_text = '\n'.join(lines[1:-1]) if len(lines) > 2 else json_text
            json_text = json_text.replace('```json', '').replace('```', '').strip()
        
        # Parse JSON
        data = json.loads(json_text)
        
        # Ajout métadonnées
        data['date_collecte'] = date_fin.strftime('%Y-%m-%d %H:%M:%S')
        data['model_utilise'] = MODEL_RECHERCHE
        data['agent'] = "Recherche News (collecte pure)"
        data['tokens_utilises'] = tokens_utilises
        data['periode'] = {
            "debut": date_debut.strftime('%Y-%m-%d'),
            "fin": date_fin.strftime('%Y-%m-%d')
        }
        
        # Génération ID unique pour chaque article
        for article in data.get('articles', []):
            hash_input = f"{article.get('url', '')}{article.get('titre', '')}"
            article['id'] = hashlib.md5(hash_input.encode()).hexdigest()[:12]
        
        nb_articles = len(data.get('articles', []))
        print(f"✅ {nb_articles} articles collectés (brut)")
        
        return data
    
    except json.JSONDecodeError as e:
        print(f"❌ Erreur parsing JSON : {e}")
        print(f"Réponse brute : {response.output_text[:500]}...")
        traceback.print_exc()
        raise
    
    except Exception as e:
        print(f"❌ Erreur collecte : {e}")
        traceback.print_exc()
        raise

# ============================================
# MAIN
# ============================================
def main():
    """Point d'entrée principal"""
    try:
        print("=" * 80)
        print("🤖 AGENT 2 - RECHERCHE NEWS (COLLECTE PURE)")
        print("=" * 80)
        print(f"Modèle : {MODEL_RECHERCHE}")
        print(f"Budget : {MAX_TOKENS} tokens")
        print(f"Mode : Web search LIVE")
        print("=" * 80)
        
        # Collecte
        data = collecter_actualites_news_brutes()
        
        # Sauvegarde JSON
        with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ Fichier généré : {OUTPUT_JSON}")
        print(f"📊 Statistiques :")
        print(f"  - Articles collectés : {len(data.get('articles', []))}")
        print(f"  - Tokens utilisés : {data.get('tokens_utilises', 0)}")
        print(f"  - Période : {data['periode']['debut']} → {data['periode']['fin']}")
        print("\n✅ COLLECTE TERMINÉE")
        
        sys.exit(0)
    
    except Exception as e:
        print(f"\n❌ ÉCHEC : {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
