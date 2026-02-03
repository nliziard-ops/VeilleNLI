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
    
    # Prompt de collecte PURE optimisé
    prompt = f"""ROBOT DE COLLECTE D'ACTUALITÉS GÉNÉRALES - AUCUNE ANALYSE

PÉRIODE: {date_debut.strftime('%d/%m/%Y')} au {date_fin.strftime('%d/%m/%Y')} (7 derniers jours)

SOURCES PAR ZONE GÉOGRAPHIQUE:

INTERNATIONAL (35% = 9 articles):
- Le Grand Continent: legrandcontinent.eu
- El País (Espagne): elpais.com
- BBC News: bbc.com/news
- Reuters: reuters.com
- The Guardian: theguardian.com/international

NATIONAL FRANCE (35% = 9 articles):
- Le Figaro: lefigaro.fr
- Le Monde: lemonde.fr
- Le Monde Diplomatique: monde-diplomatique.fr
- Libération: liberation.fr
- Les Échos: lesechos.fr

LOCAL BRETAGNE/PAYS DE LOIRE (30% = 7 articles):
- Ouest-France édition Nantes: ouest-france.fr (rechercher Nantes, Loire-Atlantique, Pays de la Loire)
- Le Télégramme: letelegramme.fr (Bretagne, Finistère, Morbihan, Côtes-d'Armor, Ille-et-Vilaine)
- Presse Océan: presseocean.fr (Nantes, Loire-Atlantique)

OBJECTIF: Collecter EXACTEMENT 25 articles (9 Int + 9 Nat + 7 Local)

CONSIGNES STRICTES:
1. Collecte BRUTE uniquement - PAS de sélection qualitative, PAS d'analyse, PAS de synthèse
2. RESPECTER la répartition 35-35-30 (9-9-7)
3. Vérifier que chaque URL est valide et accessible
4. Diversifier les sujets (pas que politique ou économie)
5. Pour LOCAL: privilégier Nantes, sports maritimes, économie régionale

ZONES GÉOGRAPHIQUES (obligatoire):
- International: géopolitique, économie mondiale, conflits, climat, tech mondiale
- National: politique française, économie France, société, culture, justice
- Local: Nantes, Bretagne, Pays de Loire, sports maritimes, mer, économie régionale

CATÉGORIES (choisir la plus pertinente):
INTERNATIONAL:
- Géopolitique (conflits, diplomatie, alliances)
- Économie mondiale (commerce, finance, énergie)
- Environnement & Climat (COP, accords, catastrophes)

NATIONAL:
- Politique nationale (gouvernement, partis, élections)
- Économie France (industrie, emploi, réformes)
- Société (éducation, santé, social, justice)

LOCAL:
- Politique locale (municipalité, région, projets urbains)
- Économie régionale (entreprises, emploi, innovation)
- Sports maritimes (voile, Route du Rhum, Vendée Globe, surf, kitesurf, wingfoil)
- Mer & littoral (ports, pêche, environnement marin, côtes)
- Culture Bretagne (festivals, patrimoine, langue bretonne)

FORMAT JSON STRICT (sans markdown, sans commentaires):
{{
  "articles": [
    {{
      "titre": "Titre exact de l'article",
      "url": "https://source-officielle.com/article-complet",
      "source": "Nom de la source (ex: Le Monde, BBC)",
      "date_publication": "YYYY-MM-DD",
      "contenu_brut": "Résumé factuel de 2-3 phrases extrait du contenu réel",
      "zone_geo": "International OU National OU Local",
      "categorie_auto": "Catégorie la plus pertinente parmi celles listées"
    }}
  ],
  "periode": {{
    "debut": "{date_debut.strftime('%Y-%m-%d')}", 
    "fin": "{date_fin.strftime('%Y-%m-%d')}"
  }},
  "nb_articles": 25,
  "repartition": {{
    "international": 9,
    "national": 9,
    "local": 7
  }}
}}

EXEMPLES DE RÉSULTATS ATTENDUS:

INTERNATIONAL:
{{
  "titre": "La Russie intensifie ses frappes sur l'infrastructure énergétique ukrainienne",
  "url": "https://www.lemonde.fr/international/article/2026/01/28/...",
  "source": "Le Monde",
  "date_publication": "2026-01-28",
  "contenu_brut": "Moscou a lancé une série de frappes massives visant les centrales électriques et les réseaux de distribution en Ukraine. Ces attaques surviennent avant l'hiver et visent à affaiblir la résistance ukrainienne.",
  "zone_geo": "International",
  "categorie_auto": "Géopolitique"
}}

NATIONAL:
{{
  "titre": "Réforme des retraites : nouvelles manifestations prévues dans toute la France",
  "url": "https://www.lefigaro.fr/actualite-france/2026/01/29/...",
  "source": "Le Figaro",
  "date_publication": "2026-01-29",
  "contenu_brut": "Les syndicats appellent à une journée de mobilisation nationale contre le projet de réforme des retraites. Des perturbations sont attendues dans les transports et les services publics.",
  "zone_geo": "National",
  "categorie_auto": "Société"
}}

LOCAL:
{{
  "titre": "Nantes : le nouveau pôle nautique de l'Erdre ouvre ses portes",
  "url": "https://www.ouest-france.fr/pays-de-la-loire/nantes/...",
  "source": "Ouest-France",
  "date_publication": "2026-01-30",
  "contenu_brut": "La métropole nantaise inaugure un complexe dédié aux sports d'eau avec espaces pour aviron, kayak et voile. Le projet vise à renforcer l'attractivité sportive de la région et à accueillir des compétitions nationales.",
  "zone_geo": "Local",
  "categorie_auto": "Sports maritimes"
}}

FOCUS LOCAL OBLIGATOIRE (7 articles minimum):
- Nantes : politique municipale, grands projets, économie, culture
- Sports maritimes : voile (courses, clubs), surf, kitesurf, wingfoil, ports
- Mer & environnement : littoral, pêche, biodiversité marine
- Bretagne : initiatives régionales, économie maritime, patrimoine

IMPORTANT:
- Retourner UNIQUEMENT le JSON (pas de texte avant/après)
- 25 articles OBLIGATOIRE : 9 Int + 9 Nat + 7 Local
- URLs complètes et valides
- Dates au format YYYY-MM-DD
- Contenu factuel (pas d'opinion)
- Diversité des sujets au sein de chaque zone"""

    print(f"🌐 Lancement GPT-5.2 + web search LIVE...")
    print(f"📅 Recherche sur 7 jours : {date_debut.strftime('%d/%m')} - {date_fin.strftime('%d/%m')}")
    print(f"🎯 Répartition : 9 Int | 9 Nat | 7 Local")
    
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
        data = json.loads(json_text)
        
        # Validation basique
        if 'articles' not in data or not isinstance(data['articles'], list):
            raise ValueError("Format JSON invalide : clé 'articles' manquante")
        
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
        
        print(f"✅ {data['nb_articles']} articles collectés")
        print(f"📍 Répartition : {repartition['international']} Int | {repartition['national']} Nat | {repartition['local']} Local")
        
        # Vérification de la répartition
        if repartition['local'] < 5:
            print(f"⚠️  Attention : seulement {repartition['local']} articles locaux (objectif: 7)")
        
        print(f"📊 Répartition par catégorie :")
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {cat}: {count}")
        
        return data
    
    except json.JSONDecodeError as e:
        print(f"❌ Erreur JSON : {e}")
        print(f"Réponse brute (500 premiers chars) :")
        print(response.output_text[:500])
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
        print(f"🎯 Objectif : {MAX_ARTICLES} articles EXACTEMENT (9 Int + 9 Nat + 7 Local)")
        print(f"🌐 Modèle : {MODEL_RECHERCHE} + web search live")
        print()
        
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
