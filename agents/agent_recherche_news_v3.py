"""
Agent Recherche News v3 - Collecte PURE par recherche web libre
Modèle : GPT-5.2 (OpenAI Responses API)
Stratégie : Recherche web générique sans sources imposées
Rôle : Collecte factuelle brute SANS tri, SANS analyse, SANS synthèse
Note : 26 articles pour permettre fusion/croisement par agent synthèse
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
MAX_ARTICLES = 26

def collecter_actualites_news() -> Dict[str, Any]:
    """
    Collecte les actualités via recherche web libre.
    
    Returns:
        Dict avec articles, métadonnées et statistiques
    """
    if not OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY manquant")
        return {"articles": [], "erreur": "API key manquante"}
    
    client = OpenAI(api_key=OPENAI_API_KEY)
    date_fin = datetime.now()
    date_debut = date_fin - timedelta(days=7)
    
    # Prompt de collecte PURE - Recherche web libre sans sources imposées
    prompt = f"""Tu es un robot de collecte d'actualités via web search - COLLECTE FACTUELLE PURE

MISSION:
Utilise la fonction web search pour trouver 26 articles d'actualité récents publiés dans les 7 derniers jours ({date_debut.strftime('%d/%m/%Y')} au {date_fin.strftime('%d/%m/%Y')}).

OBJECTIF: 26 articles
Pourquoi 26? L'agent de synthèse suivant pourra fusionner plusieurs articles (ex: 2 articles avec points de vue différents → 1 article synthétique).
Résultat final visé: ~6 articles synthétisés + ~20 articles liste.

RÉPARTITION GÉOGRAPHIQUE (flexible selon l'actualité):
- INTERNATIONAL: géopolitique, économie mondiale, tech, climat, environnement
- NATIONAL FRANCE: politique, économie, société, justice, culture
- LOCAL Bretagne/Nantes: 
  * 🌊 MER & VOILE: voile, courses nautiques, surf, kitesurf, wingfoil, sports maritimes
  * Économie régionale, ports, littoral, pêche
  * Politique locale, société, culture Bretagne

IMPORTANT - Répartition flexible: 
La répartition International/National/Local dépend de l'actualité trouvée.
Pas de quota rigide, mais équilibre souhaité.

QUALITÉ DES SOURCES:
✅ Privilégie: médias reconnus, sources fiables, objectives, réputées
✅ Diversifie: maximum 3 articles par source
❌ Évite: blogs personnels, réseaux sociaux, sources partisanes/sensationnalistes

MÉTHODE DE RECHERCHE:
1. Fais des recherches web génériques variées:
   - "actualités internationales récentes février 2026"
   - "actualités France politique économie février 2026"
   - "actualités Bretagne Nantes voile sports maritimes février 2026"
   - "courses voile surf kitesurf actualités février 2026"
2. Collecte des articles de SOURCES DIFFÉRENTES
3. Vérifie que les articles sont RÉCENTS (7 derniers jours)

CATÉGORIES (choisis LA PLUS pertinente):
International: Géopolitique | Économie mondiale | Environnement & Climat | Tech
National: Politique nationale | Économie France | Société | Justice
Local: Mer & Voile | Sports maritimes | Économie régionale | Politique locale | Culture Bretagne

FORMAT JSON STRICT (sans markdown, sans commentaires):
{{
  "articles": [
    {{
      "titre": "Titre exact de l'article",
      "url": "https://source.com/article",
      "source": "Nom de la source",
      "date_publication": "YYYY-MM-DD",
      "contenu_brut": "Résumé factuel 2-3 phrases du contenu",
      "zone_geo": "International OU National OU Local",
      "categorie_auto": "Catégorie pertinente"
    }}
  ],
  "periode": {{
    "debut": "{date_debut.strftime('%Y-%m-%d')}",
    "fin": "{date_fin.strftime('%Y-%m-%d')}"
  }},
  "nb_articles": 26,
  "repartition": {{"international": X, "national": Y, "local": Z}}
}}

CONSIGNES STRICTES:
- Retourner UNIQUEMENT le JSON (pas de texte avant/après)
- 26 articles OBLIGATOIRE
- URLs complètes et valides
- Dates au format YYYY-MM-DD
- Contenu factuel (pas d'opinion)
- Sources fiables et diversifiées
- Articles RÉCENTS (7 derniers jours maximum)
- Pour LOCAL: ne pas oublier MER & VOILE (courses, sports nautiques)"""

    print(f"🌐 Lancement GPT-5.2 + web search LIVE...")
    print(f"📅 Recherche : {date_debut.strftime('%d/%m')} - {date_fin.strftime('%d/%m')}")
    print(f"🎯 Objectif : {MAX_ARTICLES} articles (répartition flexible)")
    print(f"🏆 Priorité : sources fiables, diversifiées, objectives")
    print()
    
    try:
        response = client.responses.create(
            model=MODEL_RECHERCHE,
            tools=[{"type": "web_search", "external_web_access": True}],
            input=prompt
        )
        
        tokens_used = response.usage.total_tokens
        print(f"📊 Tokens utilisés : {tokens_used}")
        
        # Nettoyage du JSON
        json_text = response.output_text.strip()
        if json_text.startswith('```'):
            lines = json_text.split('\n')
            json_text = '\n'.join(lines[1:-1]) if len(lines) > 2 else json_text
            json_text = json_text.replace('```json', '').replace('```', '').strip()
        
        # Parse JSON
        try:
            data = json.loads(json_text)
        except json.JSONDecodeError as e:
            print(f"❌ Erreur parsing JSON : {e}")
            print(f"🔍 Réponse brute (500 premiers chars):")
            print(response.output_text[:500])
            raise
        
        # Validation basique
        if 'articles' not in data:
            print(f"⚠️ Clé 'articles' manquante. Clés présentes: {list(data.keys())}")
            data['articles'] = []
        
        if not isinstance(data['articles'], list):
            print(f"⚠️ 'articles' n'est pas une liste. Type: {type(data['articles'])}")
            data['articles'] = []
        
        # Enrichissement métadonnées
        data['date_collecte'] = date_fin.strftime('%Y-%m-%d %H:%M:%S')
        data['model_utilise'] = MODEL_RECHERCHE
        data['tokens_utilises'] = tokens_used
        data['agent'] = "Recherche News v3 - Web search libre"
        data['nb_articles'] = len(data.get('articles', []))
        
        # Calcul de la répartition réelle
        repartition = {'international': 0, 'national': 0, 'local': 0}
        categories = {}
        sources = {}
        
        for article in data.get('articles', []):
            # ID unique
            hash_input = f"{article.get('url', '')}{article.get('titre', '')}"
            article['id'] = hashlib.md5(hash_input.encode()).hexdigest()[:12]
            
            # Répartition par zone
            zone = article.get('zone_geo', 'National')
            if zone == 'International':
                repartition['international'] += 1
            elif zone == 'Local':
                repartition['local'] += 1
            else:
                repartition['national'] += 1
            
            # Répartition par catégorie
            cat = article.get('categorie_auto', 'Non classé')
            categories[cat] = categories.get(cat, 0) + 1
            
            # Comptage des sources (diversité)
            source = article.get('source', 'Inconnue')
            sources[source] = sources.get(source, 0) + 1
        
        data['repartition'] = repartition
        
        nb_articles = data['nb_articles']
        print(f"\n{'✅' if nb_articles > 0 else '⚠️'} {nb_articles} articles collectés")
        
        if nb_articles == 0:
            print("❌ PROBLÈME: Aucun article collecté !")
            print("🔍 Vérifier si GPT-5.2 a accès au web search")
        elif nb_articles < MAX_ARTICLES:
            print(f"⚠️ Attention : seulement {nb_articles}/{MAX_ARTICLES} articles")
        else:
            print(f"📍 Répartition : {repartition['international']} Int | {repartition['national']} Nat | {repartition['local']} Local")
            
            print(f"📊 Répartition par catégorie (top 5) :")
            for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"   • {cat}: {count}")
            
            print(f"🏢 Diversité des sources : {len(sources)} sources différentes")
            sources_multiples = {s: c for s, c in sources.items() if c > 3}
            if sources_multiples:
                print(f"⚠️ Sources avec >3 articles : {sources_multiples}")
        
        return data
    
    except json.JSONDecodeError as e:
        print(f"❌ Erreur JSON : {e}")
        print(f"🔍 Réponse brute complète :")
        print(response.output_text)
        traceback.print_exc()
        raise
    
    except Exception as e:
        print(f"❌ Erreur : {e}")
        traceback.print_exc()
        raise

def main():
    try:
        print("=" * 80)
        print("🤖 AGENT RECHERCHE NEWS v3 - WEB SEARCH LIBRE")
        print("=" * 80)
        print(f"📅 Période : 7 derniers jours")
        print(f"🎯 Objectif : {MAX_ARTICLES} articles (fusion possible par synthèse)")
        print(f"🌐 Modèle : {MODEL_RECHERCHE} + web search live")
        print(f"🏆 Stratégie : sources fiables, diversifiées, objectives")
        print()
        
        data = collecter_actualites_news()
        
        # Sauvegarde JSON
        with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print()
        print(f"✅ Fichier généré : {OUTPUT_JSON}")
        print(f"📊 {data['nb_articles']} articles • {data['tokens_utilises']} tokens")
        
        print("=" * 80)
        
        # Exit code selon le nombre d'articles
        if data['nb_articles'] == 0:
            print("⚠️ WARNING: Aucun article collecté, mais pas d'erreur bloquante")
            sys.exit(0)  # Ne pas bloquer le workflow
        else:
            sys.exit(0)
    
    except Exception as e:
        print()
        print(f"❌ ÉCHEC : {e}")
        print("=" * 80)
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
