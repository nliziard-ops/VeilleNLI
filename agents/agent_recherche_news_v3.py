"""
Agent Recherche News v3 - COLLECTE PURE
Modèle : GPT-5.2 (OpenAI Responses API)
Rôle : Collecte factuelle BRUTE avec web search LIVE
Max tokens : 10000
"""

import os
import sys
import json
import hashlib
import traceback
from datetime import datetime, timedelta
from typing import Dict, Any, List
from openai import OpenAI

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
MODEL_RECHERCHE = "gpt-5.2"
MAX_TOKENS = 10000
OUTPUT_JSON = "recherche_news_brute.json"

SOURCES_NEWS = [
    "Le Grand Continent", "El Pais", "BBC News", "Reuters",
    "Le Figaro", "Le Monde", "Monde Diplomatique",
    "Ouest-France", "Le Télégramme de Brest"
]


def rechercher_actualites_news() -> Dict[str, Any]:
    """
    Collecte BRUTE des actualités générales sans tri ni analyse.
    Retourne JSON brut avec tous les articles trouvés (max 25).
    Distribution : 35% International, 35% France, 30% Local Bretagne.
    """
    if not OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY manquant")
        return {"articles": [], "error": "No API key"}
    
    client = OpenAI(api_key=OPENAI_API_KEY)
    date_fin = datetime.now()
    date_debut = date_fin - timedelta(days=7)
    
    # PROMPT DE COLLECTE PURE - AUCUNE ANALYSE
    prompt = f"""Tu es un collecteur d'information. Ta SEULE mission : collecter des actualités générales.

PÉRIODE : {date_debut.strftime('%d/%m/%Y')} au {date_fin.strftime('%d/%m/%Y')}

SOURCES PRIORITAIRES :
{', '.join(SOURCES_NEWS)}

DISTRIBUTION GÉOGRAPHIQUE CIBLE :
- 35% International (géopolitique, économie mondiale, environnement global)
- 35% France (politique nationale, économie France, société française)
- 30% Local Bretagne/Pays de Loire (Nantes, Brest, Belle-Île, sports maritimes)

CONSIGNES STRICTES :
1. Collecte 20-25 actualités maximum
2. NE FAIS AUCUN TRI
3. NE FAIS AUCUNE ANALYSE
4. NE FAIS AUCUNE SYNTHÈSE
5. Retourne UNIQUEMENT les informations brutes trouvées

CATÉGORIES POSSIBLES :
International : Géopolitique, Économie mondiale, Environnement global, Conflits
National : Politique française, Économie France, Société, Éducation, Santé
Local : Politique locale, Économie régionale, Sports maritimes (voile, surf, kitesurf, wingfoil), Mer & littoral, Culture Bretagne

ZONES GÉOGRAPHIQUES :
- International
- National (France)
- Local (Bretagne/Pays de Loire)

FORMAT JSON STRICT (sans markdown) :
{{
  "articles": [
    {{
      "titre": "Titre exact de l'article",
      "url": "https://url-complete.com/article",
      "source": "Nom de la source",
      "date_publication": "YYYY-MM-DD",
      "zone_geo": "International ou National ou Local",
      "categorie": "Catégorie parmi la liste ci-dessus",
      "contenu_brut": "Résumé factuel complet de l'article tel que trouvé (5-10 lignes)"
    }}
  ],
  "periode": {{
    "debut": "{date_debut.strftime('%Y-%m-%d')}",
    "fin": "{date_fin.strftime('%Y-%m-%d')}"
  }},
  "repartition_cible": {{
    "international": 35,
    "national": 35,
    "local": 30
  }},
  "sources_consultees": ["liste", "des", "sources"]
}}

FOCUS LOCAL : Actualités de Nantes, Brest, Belle-Île-en-Mer, sports de glisse maritime (voile, surf, kitesurf, wingfoil), événements maritimes et littoraux.

IMPORTANT : Réponds UNIQUEMENT en JSON valide, sans ```json ni aucun markdown.
"""

    print("=" * 80)
    print("🔍 COLLECTE BRUTE - GPT-5.2 + WEB SEARCH LIVE")
    print(f"📅 Période : {date_debut.strftime('%d/%m/%Y')} → {date_fin.strftime('%d/%m/%Y')}")
    print(f"🎯 Max tokens : {MAX_TOKENS}")
    print(f"🌍 Distribution : 35% Int | 35% Nat | 30% Local")
    print("=" * 80)
    
    try:
        # SYNTAXE OFFICIELLE OPENAI - Responses API avec web search LIVE
        response = client.responses.create(
            model=MODEL_RECHERCHE,
            tools=[{"type": "web_search", "external_web_access": True}],
            input=prompt,
            max_tokens=MAX_TOKENS
        )
        
        print(f"📊 Tokens utilisés : {response.usage.total_tokens}/{MAX_TOKENS}")
        
        # Nettoyage du JSON (au cas où il y aurait du markdown)
        json_text = response.output_text.strip()
        if json_text.startswith('```'):
            lines = json_text.split('\n')
            json_text = '\n'.join(lines[1:-1]) if len(lines) > 2 else json_text
            json_text = json_text.replace('```json', '').replace('```', '').strip()
        
        # Parse JSON
        data = json.loads(json_text)
        
        # Ajout métadonnées
        data['date_collecte'] = date_fin.strftime('%Y-%m-%d')
        data['model_utilise'] = MODEL_RECHERCHE
        data['agent'] = "Recherche News v3 (collecte pure)"
        data['max_tokens'] = MAX_TOKENS
        data['tokens_utilises'] = response.usage.total_tokens
        
        # Calcul répartition réelle
        if 'repartition_reelle' not in data:
            data['repartition_reelle'] = {'international': 0, 'national': 0, 'local': 0}
        
        # Génération ID unique + comptage zones
        articles = data.get('articles', [])
        for article in articles:
            hash_input = f"{article.get('url', '')}{article.get('titre', '')}"
            article['id'] = hashlib.md5(hash_input.encode()).hexdigest()[:12]
            
            zone = article.get('zone_geo', 'National')
            if zone == 'International':
                data['repartition_reelle']['international'] += 1
            elif zone == 'Local':
                data['repartition_reelle']['local'] += 1
            else:
                data['repartition_reelle']['national'] += 1
        
        nb_articles = len(articles)
        print(f"✅ {nb_articles} articles collectés")
        print(f"📊 Répartition : Int={data['repartition_reelle']['international']} | "
              f"Nat={data['repartition_reelle']['national']} | "
              f"Local={data['repartition_reelle']['local']}")
        
        if nb_articles == 0:
            print("⚠️  ATTENTION : Aucun article collecté")
        elif nb_articles > 25:
            print(f"⚠️  ATTENTION : {nb_articles} articles (limite 25 dépassée)")
        
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


def main():
    """Point d'entrée principal"""
    try:
        print("\n" + "=" * 80)
        print("🤖 AGENT RECHERCHE NEWS v3 - COLLECTE PURE")
        print("=" * 80 + "\n")
        
        # Collecte
        data = rechercher_actualites_news()
        
        # Sauvegarde JSON
        with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Fichier sauvegardé : {OUTPUT_JSON}")
        print(f"📦 Taille : {os.path.getsize(OUTPUT_JSON)} octets")
        
        print("\n" + "=" * 80)
        print("✅ COLLECTE TERMINÉE")
        print("=" * 80 + "\n")
        
        sys.exit(0)
    
    except Exception as e:
        print(f"\n❌ ERREUR FATALE : {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
