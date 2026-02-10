"""
Agent Recherche News v3 - Collecte PURE par lecture pages d'accueil
Modèle : GPT-5.2 (OpenAI Responses API)
Stratégie : Lecture directe des pages d'accueil des sources (évite blocage anti-bot)
Rôle : Collecte factuelle brute SANS tri, SANS analyse, SANS synthèse
"""

import os
import sys
import json
import hashlib
import traceback
from datetime import datetime, timedelta
from typing import Dict, Any, List
from openai import OpenAI

# Configuration
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
MODEL_RECHERCHE = "gpt-5.2"
OUTPUT_JSON = "recherche_news_brute.json"
MAX_ARTICLES_TOTAL = 25

# Sources d'actualités - Pages d'accueil uniquement
SOURCES_NEWS = {
    "international": [
        {"nom": "BBC News", "url": "https://www.bbc.com/news", "articles_cible": 3},
        {"nom": "Reuters", "url": "https://www.reuters.com", "articles_cible": 3},
        {"nom": "The Guardian", "url": "https://www.theguardian.com/international", "articles_cible": 3},
    ],
    "national": [
        {"nom": "Le Monde", "url": "https://www.lemonde.fr", "articles_cible": 3},
        {"nom": "Le Figaro", "url": "https://www.lefigaro.fr", "articles_cible": 3},
        {"nom": "Libération", "url": "https://www.liberation.fr", "articles_cible": 3},
    ],
    "local": [
        {"nom": "Ouest-France", "url": "https://www.ouest-france.fr/bretagne", "articles_cible": 4},
        {"nom": "Le Télégramme", "url": "https://www.letelegramme.fr", "articles_cible": 3},
    ]
}

def collecter_depuis_source(client: OpenAI, source: Dict[str, Any], zone_geo: str) -> List[Dict[str, Any]]:
    """
    Collecte les articles depuis une page d'accueil de source.
    
    Args:
        client: Client OpenAI
        source: Dict avec nom, url, articles_cible
        zone_geo: "International", "National" ou "Local"
    
    Returns:
        Liste des articles collectés (peut être vide en cas d'erreur)
    """
    date_fin = datetime.now()
    date_debut = date_fin - timedelta(days=7)
    
    prompt = f"""Tu es un robot de lecture de page web - EXTRACTION FACTUELLE PURE

MISSION:
Va sur la page d'accueil : {source['url']}
Lis le contenu HTML de cette page.
Extrais les {source['articles_cible']} articles les plus récents visibles sur cette page d'accueil.

EXTRACTION:
Pour chaque article trouvé sur la page d'accueil, extrais:
- Le TITRE complet de l'article
- Le RÉSUMÉ/CHAPEAU s'il est visible sur la page d'accueil (2-3 phrases max)
- L'URL complète de l'article
- La date de publication si visible

IMPORTANT:
- NE VA PAS sur les liens des articles individuels
- Extrais UNIQUEMENT ce qui est visible sur la page d'accueil
- Si le résumé n'est pas visible, mets "Résumé non disponible sur page d'accueil"
- Privilégie les articles publiés dans les 7 derniers jours ({date_debut.strftime('%d/%m/%Y')} au {date_fin.strftime('%d/%m/%Y')})

CATÉGORIES (choisis LA PLUS pertinente selon le sujet):
International: Géopolitique | Économie mondiale | Environnement & Climat
National: Politique nationale | Économie France | Société
Local: Politique locale | Économie régionale | Sports maritimes | Mer & littoral | Culture Bretagne

FORMAT JSON STRICT (sans markdown, sans commentaires):
{{
  "source": "{source['nom']}",
  "url_source": "{source['url']}",
  "articles": [
    {{
      "titre": "Titre exact de l'article",
      "url": "https://...",
      "source": "{source['nom']}",
      "date_publication": "YYYY-MM-DD ou null si non visible",
      "contenu_brut": "Résumé/chapeau extrait de la page d'accueil",
      "zone_geo": "{zone_geo}",
      "categorie_auto": "Catégorie pertinente"
    }}
  ],
  "nb_articles": {source['articles_cible']},
  "statut": "succès"
}}

RETOURNE UNIQUEMENT LE JSON (pas de texte avant/après)."""

    try:
        print(f"  📖 Lecture de {source['nom']} ({source['url']})...")
        
        response = client.responses.create(
            model=MODEL_RECHERCHE,
            tools=[{"type": "web_search", "external_web_access": True}],
            input=prompt
        )
        
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
            print(f"    ❌ Erreur parsing JSON pour {source['nom']}: {e}")
            print(f"    🔍 Réponse brute (300 premiers chars): {response.output_text[:300]}")
            return []
        
        articles = data.get('articles', [])
        nb_articles = len(articles)
        
        print(f"    ✅ {nb_articles} articles extraits de {source['nom']}")
        
        return articles
    
    except Exception as e:
        print(f"    ❌ Erreur lors de la lecture de {source['nom']}: {e}")
        print(f"    ⏭️  Passage à la source suivante...")
        traceback.print_exc()
        return []

def collecter_actualites_news() -> Dict[str, Any]:
    """
    Collecte les actualités en lisant les pages d'accueil des sources.
    
    Returns:
        Dict avec articles, métadonnées et statistiques
    """
    if not OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY manquant")
        return {"articles": [], "erreur": "API key manquante"}
    
    client = OpenAI(api_key=OPENAI_API_KEY)
    date_fin = datetime.now()
    date_debut = date_fin - timedelta(days=7)
    
    tous_articles = []
    erreurs_sources = []
    tokens_total = 0
    
    print(f"🌐 Collecte par lecture des pages d'accueil...")
    print(f"📅 Période ciblée : {date_debut.strftime('%d/%m/%Y')} - {date_fin.strftime('%d/%m/%Y')}")
    print()
    
    # Collecte par zone géographique
    for zone, sources in SOURCES_NEWS.items():
        zone_label = zone.capitalize()
        print(f"📍 Zone {zone_label} : {len(sources)} sources")
        
        for source in sources:
            articles = collecter_depuis_source(client, source, zone_label)
            
            if articles:
                tous_articles.extend(articles)
            else:
                erreurs_sources.append(source['nom'])
        
        print()
    
    # Enrichissement des articles avec ID unique
    for article in tous_articles:
        hash_input = f"{article.get('url', '')}{article.get('titre', '')}"
        article['id'] = hashlib.md5(hash_input.encode()).hexdigest()[:12]
    
    # Calcul de la répartition
    repartition = {'international': 0, 'national': 0, 'local': 0}
    categories = {}
    
    for article in tous_articles:
        zone = article.get('zone_geo', 'National')
        if zone == 'International':
            repartition['international'] += 1
        elif zone == 'Local':
            repartition['local'] += 1
        else:
            repartition['national'] += 1
        
        cat = article.get('categorie_auto', 'Non classé')
        categories[cat] = categories.get(cat, 0) + 1
    
    # Construction du résultat
    data = {
        "articles": tous_articles,
        "periode": {
            "debut": date_debut.strftime('%Y-%m-%d'),
            "fin": date_fin.strftime('%Y-%m-%d')
        },
        "nb_articles": len(tous_articles),
        "repartition": repartition,
        "date_collecte": date_fin.strftime('%Y-%m-%d %H:%M:%S'),
        "model_utilise": MODEL_RECHERCHE,
        "agent": "Recherche News v3 - Lecture pages d'accueil",
        "sources_traitees": sum(len(s) for s in SOURCES_NEWS.values()),
        "sources_en_erreur": erreurs_sources if erreurs_sources else []
    }
    
    # Rapport final
    nb_articles = data['nb_articles']
    print(f"{'✅' if nb_articles > 0 else '⚠️'} {nb_articles} articles collectés au total")
    
    if nb_articles == 0:
        print("❌ PROBLÈME: Aucun article collecté !")
        print("🔍 Toutes les sources ont échoué")
    else:
        print(f"📍 Répartition : {repartition['international']} Int | {repartition['national']} Nat | {repartition['local']} Local")
        
        if erreurs_sources:
            print(f"⚠️ Sources en erreur ({len(erreurs_sources)}): {', '.join(erreurs_sources)}")
        
        print(f"📊 Répartition par catégorie :")
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"   • {cat}: {count}")
    
    return data

def main():
    try:
        print("=" * 80)
        print("🤖 AGENT RECHERCHE NEWS v3 - LECTURE PAGES D'ACCUEIL")
        print("=" * 80)
        print(f"📅 Période : 7 derniers jours")
        print(f"🎯 Objectif : ~{MAX_ARTICLES_TOTAL} articles (répartition automatique)")
        print(f"🌐 Modèle : {MODEL_RECHERCHE} + web search live")
        print(f"📖 Stratégie : Lecture directe des pages d'accueil (anti-bot)")
        print()
        
        data = collecter_actualites_news()
        
        # Sauvegarde JSON
        with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print()
        print(f"✅ Fichier généré : {OUTPUT_JSON}")
        print(f"📊 {data['nb_articles']} articles")
        
        if data.get('sources_en_erreur'):
            print(f"⚠️ {len(data['sources_en_erreur'])} sources en erreur (non bloquant)")
        
        print("=" * 80)
        
        # Exit code : succès même si certaines sources ont échoué
        sys.exit(0)
    
    except Exception as e:
        print()
        print(f"❌ ÉCHEC : {e}")
        print("=" * 80)
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
