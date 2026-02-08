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
    
    # Prompt de collecte PURE - Format strictement aligné sur recherche_ia_v3
    prompt = f"""Tu es un robot de collecte d'actualités via web search - AUCUNE ANALYSE

Utilise la fonction web search pour trouver des articles publiés dans les 7 derniers jours ({date_debut.strftime('%d/%m/%Y')} au {date_fin.strftime('%d/%m/%Y')}).

RÉPARTITION:
- articles INTERNATIONAUX (géopolitique, économie mondiale, tech, climat)
- articles NATIONAUX FRANCE (politique, économie, société, justice)
- articles LOCAUX Bretagne/Pays de Loire (Nantes, Rennes, sports maritimes, économie régionale)

MÉTHODE DE RECHERCHE:
1. Utilise des requêtes web search génériques (pas d'accès direct aux sites)
2. Exemples de requêtes:
   - "actualités internationales géopolitique février 2026"
   - "actualités France politique février 2026"
   - "actualités Bretagne Nantes sports maritimes février 2026"
3. Récupère les résultats via web search (pas de scraping direct)

CONSIGNES:
1. Cherche des articles RÉCENTS (7 derniers jours maximum)
2. URLs complètes et valides
3. Diversifie les sujets (pas que politique/économie)
4. Pour LOCAL: Nantes, Bretagne, sports maritimes (voile, surf, kitesurf), mer, ports

CATÉGORIES (choisis LA PLUS pertinente):
International: Géopolitique | Économie mondiale | Environnement & Climat
National: Politique nationale | Économie France | Société
Local: Politique locale | Économie régionale | Sports maritimes | Mer & littoral | Culture Bretagne

FORMAT JSON STRICT (sans markdown, sans commentaires):
{{
  "articles": [
    {{
      "titre": "Titre exact de l'article",
      "url": "https://source.com/article",
      "source": "Nom source",
      "date_publication": "YYYY-MM-DD",
      "contenu_brut": "Résumé factuel 2-3 phrases",
      "zone_geo": "International OU National OU Local",
      "categorie_auto": "Catégorie pertinente"
    }}
  ],
  "periode": {{"debut": "{date_debut.strftime('%Y-%m-%d')}", "fin": "{date_fin.strftime('%Y-%m-%d')}"}},
  "nb_articles": 25,
  "repartition": {{"international": 9, "national": 9, "local": 7}}
}}

IMPORTANT:
- Utilise UNIQUEMENT le web search (pas d'accès direct aux sites)
- Retourner UNIQUEMENT le JSON (pas de texte avant/après)
- 25 articles OBLIGATOIRE (ni plus, ni moins)
- URLs complètes et valides
- Dates au format YYYY-MM-DD
- Contenu factuel (pas d'opinion)"""

    print(f"🌐 Lancement GPT-5.2 + web search LIVE...")
    print(f"📅 Recherche : {date_debut.strftime('%d/%m')} - {date_fin.strftime('%d/%m')}")
    print(f"🎯 Objectif : 9 Int | 9 Nat | 7 Local")
    
    try:
        response = client.responses.create(
            model=MODEL_RECHERCHE,
            tools=[{"type": "web_search", "external_web_access": True}],
            input=prompt
        )
        
        tokens_used = response.usage.total_tokens
        print(f"📊 Tokens utilisés : {tokens_used}")
        
        # DEBUG: Afficher les 1000 premiers caractères de la réponse brute
        print(f"\n🔍 DEBUG - Réponse brute (1000 premiers chars):")
        print(response.output_text[:1000])
        print("...\n")
        
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
            print(f"🔍 Contenu complet de la réponse:")
            print(response.output_text)
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
        data['agent'] = "Recherche News v3"
        data['nb_articles'] = len(data.get('articles', []))
        
        # Calcul de la répartition réelle
        repartition = {'international': 0, 'national': 0, 'local': 0}
        categories = {}
        
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
        
        data['repartition'] = repartition
        
        nb_articles = data['nb_articles']
        print(f"\n{'✅' if nb_articles > 0 else '⚠️'} {nb_articles} articles collectés")
        
        if nb_articles == 0:
            print("❌ PROBLÈME: Aucun article collecté !")
            print("🔍 Vérifier si GPT-5.2 a accès au web search")
            print("🔍 Vérifier si les sources sont accessibles")
        else:
            print(f"📍 Répartition : {repartition['international']} Int | {repartition['national']} Nat | {repartition['local']} Local")
            
            if repartition['local'] < 5:
                print(f"⚠️ Attention : seulement {repartition['local']} articles locaux (objectif: 7)")
            
            print(f"📊 Répartition par catégorie :")
            for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
                print(f"   • {cat}: {count}")
        
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
        print("🤖 AGENT RECHERCHE NEWS v3 - COLLECTE PURE")
        print("=" * 80)
        print(f"📅 Période : 7 derniers jours")
        print(f"🎯 Objectif : {MAX_ARTICLES} articles (9 Int + 9 Nat + 7 Local)")
        print(f"🌐 Modèle : {MODEL_RECHERCHE} + web search live")
        print()
        
        data = collecter_actualites_news()
        
        # Sauvegarde JSON
        with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print()
        print(f"✅ Fichier généré : {OUTPUT_JSON}")
        print(f"📊 {data['nb_articles']} articles • {data['tokens_utilises']} tokens")
        
        # Afficher le contenu du fichier pour debug
        print(f"\n🔍 Contenu du fichier {OUTPUT_JSON} :")
        with open(OUTPUT_JSON, 'r', encoding='utf-8') as f:
            print(f.read()[:500])
        
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
        sys.exit(1)

if __name__ == "__main__":
    main()
