"""
Agent 1 - Collecteur et Filtre Actualités
Modèle : GPT-4o-mini (économique)
Rôle : Recherche web → Filtrage → Classification → JSON
"""

import os
import sys
import json
import hashlib
import traceback
from datetime import datetime, timedelta
from typing import List, Dict, Any
from openai import OpenAI
import requests


# ================================================================================
# CONFIGURATION
# ================================================================================

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
TAVILY_API_KEY = os.environ.get('TAVILY_API_KEY')

# Modèle économique pour filtrage
MODEL_COLLECTEUR = "gpt-4o-mini-2024-07-18"

# Fichier de sortie
OUTPUT_JSON = "articles_filtres_news.json"


# ================================================================================
# TAVILY SEARCH
# ================================================================================

def recherche_tavily(query: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """Effectue une recherche web via Tavily API"""
    if not TAVILY_API_KEY:
        print("❌ TAVILY_API_KEY manquante")
        return []
    
    url = "https://api.tavily.com/search"
    
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "max_results": max_results,
        "search_depth": "basic",
        "include_answer": False,
        "include_raw_content": False,
        "include_images": False
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        resultats = []
        for item in data.get('results', []):
            resultats.append({
                'titre': item.get('title', ''),
                'url': item.get('url', ''),
                'snippet': item.get('content', ''),
                'score': item.get('score', 0.0)
            })
        
        return resultats
    
    except Exception as e:
        print(f"❌ Erreur Tavily pour '{query}': {e}")
        return []


# ================================================================================
# COLLECTE MULTI-REQUÊTES
# ================================================================================

def collecter_articles_bruts() -> List[Dict[str, Any]]:
    """Lance 10 recherches ciblées sur actualités françaises/internationales"""
    
    # Requêtes ciblées pour actualités
    # ⏰ TOUTES les requêtes incluent un marqueur temporel (cette semaine, derniers jours, récentes)
    requetes = [
        "actualités France cette semaine",
        "politique française derniers jours",
        "économie France entreprises cette semaine",
        "international Europe actualités récentes",
        "écologie transition énergétique France dernière semaine",
        "actualités Nantes Pays de la Loire cette semaine",
        "Bretagne actualités derniers jours",
        "technologie innovation France cette semaine",
        "société France actualités récentes",
        "mer littoral Atlantique derniers jours"
    ]
    
    print(f"🔍 Lancement de {len(requetes)} recherches Tavily...")
    
    articles_bruts = []
    for i, query in enumerate(requetes, 1):
        print(f"  [{i}/{len(requetes)}] {query}")
        resultats = recherche_tavily(query, max_results=12)
        
        for res in resultats:
            articles_bruts.append({
                'titre': res['titre'],
                'url': res['url'],
                'snippet': res['snippet'],
                'score_tavily': res['score'],
                'requete_source': query
            })
    
    print(f"✅ {len(articles_bruts)} articles bruts collectés")
    
    if len(articles_bruts) == 0:
        print("⚠️  Aucun article collecté")
    
    return articles_bruts


# ================================================================================
# FILTRAGE ET CLASSIFICATION GPT-4o-mini
# ================================================================================

def filtrer_et_classifier(articles_bruts: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Filtre et classifie les articles avec GPT-4o-mini"""
    
    if len(articles_bruts) == 0:
        date_fin = datetime.now()
        date_debut = date_fin - timedelta(days=7)
        return {
            "articles": [],
            "statistiques": {
                "articles_bruts": 0,
                "doublons_supprimes": 0,
                "articles_non_pertinents": 0,
                "articles_finaux": 0
            },
            "date_collecte": date_fin.strftime('%Y-%m-%d'),
            "periode": {
                "debut": date_debut.strftime('%Y-%m-%d'),
                "fin": date_fin.strftime('%Y-%m-%d')
            },
            "model_utilise": MODEL_COLLECTEUR,
            "themes": {}
        }
    
    print(f"🤖 Création client OpenAI...")
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    date_fin = datetime.now()
    date_debut = date_fin - timedelta(days=7)
    
    articles_input = articles_bruts[:150]
    print(f"📝 Préparation de {len(articles_input)} articles pour GPT-4o-mini...")
    
    articles_text = "\n\n".join([
        f"[{i+1}] {art['titre']}\nURL: {art['url']}\nSnippet: {art['snippet'][:200]}..."
        for i, art in enumerate(articles_input)
    ])
    
    prompt = f"""Tu es un agent de filtrage d'actualités générales françaises et internationales.

**PÉRIODE ANALYSÉE** : du {date_debut.strftime('%d/%m/%Y')} au {date_fin.strftime('%d/%m/%Y')}

**ARTICLES BRUTS À ANALYSER** :
{articles_text}

**TA MISSION** :
1. Supprimer les doublons (même sujet, sources différentes → garder la meilleure)
2. Filtrer les articles pertinents pour un cadre français cultivé
3. Exclure : people, fait divers mineurs, sports (sauf événements majeurs)
4. Classifier chaque article dans UN thème principal :
   - Politique française
   - Économie & Entreprises
   - International & Europe
   - Écologie & Transition
   - Société
   - Technologie & Innovation
   - Nantes & Région Ouest
   - Culture

5. Attribuer un score de pertinence (1-10)

**FORMAT DE SORTIE JSON** :
```json
{{
  "articles": [
    {{
      "titre": "Titre exact de l'article",
      "source": "Nom du média (ex: Le Monde, Les Échos)",
      "url": "URL complète",
      "date_estimee": "2026-01-10",
      "theme": "Politique française",
      "snippet": "Résumé en 2-3 lignes",
      "pertinence": 8,
      "tags": ["gouvernement", "réforme", "débat"]
    }}
  ],
  "statistiques": {{
    "articles_bruts": {len(articles_bruts)},
    "doublons_supprimes": 0,
    "articles_non_pertinents": 0,
    "articles_finaux": 0
  }}
}}
```

**CONSIGNES** :
- Vise 8-12 articles finaux (les plus importants)
- Reformule les snippets
- Détecte les doublons
- Privilégie sources françaises sérieuses (Le Monde, Figaro, Échos, Libération, Ouest-France)

Génère le JSON maintenant :"""

    print("🤖 Appel API GPT-4o-mini pour filtrage...")
    
    try:
        response = client.chat.completions.create(
            model=MODEL_COLLECTEUR,
            messages=[
                {"role": "system", "content": "Tu es un agent de filtrage d'actualités. Tu réponds UNIQUEMENT en JSON valide, sans markdown, sans commentaires."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=3000
        )
        
        print(f"📊 Tokens utilisés : {response.usage.total_tokens}")
        
        json_text = response.choices[0].message.content.strip()
        
        # Nettoyer markdown
        if json_text.startswith('```'):
            lines = json_text.split('\n')
            json_text = '\n'.join(lines[1:-1]) if len(lines) > 2 else json_text
            json_text = json_text.replace('```json', '').replace('```', '').strip()
        
        data = json.loads(json_text)
        
        # Ajouter métadonnées
        data['date_collecte'] = date_fin.strftime('%Y-%m-%d')
        data['periode'] = {
            'debut': date_debut.strftime('%Y-%m-%d'),
            'fin': date_fin.strftime('%Y-%m-%d')
        }
        data['model_utilise'] = MODEL_COLLECTEUR
        
        # Générer IDs
        for article in data['articles']:
            hash_input = f"{article['url']}{article['titre']}"
            article['id'] = hashlib.md5(hash_input.encode()).hexdigest()[:12]
        
        # Statistiques thématiques
        themes_count = {}
        for article in data['articles']:
            theme = article['theme']
            themes_count[theme] = themes_count.get(theme, 0) + 1
        
        data['themes'] = themes_count
        data['statistiques']['articles_finaux'] = len(data['articles'])
        
        print(f"✅ Filtrage terminé : {len(data['articles'])} articles retenus")
        
        return data
    
    except Exception as e:
        print(f"❌ Erreur GPT-4o-mini : {e}")
        traceback.print_exc()
        raise


# ================================================================================
# SAUVEGARDE JSON
# ================================================================================

def sauvegarder_json(data: Dict[str, Any], filepath: str) -> None:
    """Sauvegarde le JSON structuré"""
    print(f"💾 Sauvegarde du JSON dans {filepath}...")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    file_size = os.path.getsize(filepath)
    print(f"✅ JSON sauvegardé : {filepath}")
    print(f"📊 Taille : {file_size} octets ({file_size / 1024:.2f} KB)")


# ================================================================================
# MAIN
# ================================================================================

def main():
    """Point d'entrée principal"""
    
    try:
        print("=" * 80)
        print("🤖 AGENT 1 - COLLECTEUR NEWS (GPT-4o-mini)")
        print("=" * 80)
        print(f"⏰ Exécution : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"📂 Répertoire : {os.getcwd()}")
        print()
        
        # Vérifier clés API
        print("🔑 Vérification des clés API...")
        if not OPENAI_API_KEY:
            print("❌ ERREUR : OPENAI_API_KEY manquante")
            sys.exit(1)
        else:
            print(f"✅ OPENAI_API_KEY présente")
        
        if not TAVILY_API_KEY:
            print("❌ ERREUR : TAVILY_API_KEY manquante")
            sys.exit(1)
        else:
            print(f"✅ TAVILY_API_KEY présente")
        
        print()
        
        # Collecte
        print("📡 ÉTAPE 1/3 : Collecte d'articles via Tavily")
        print("-" * 80)
        articles_bruts = collecter_articles_bruts()
        print()
        
        # Filtrage
        print("🧹 ÉTAPE 2/3 : Filtrage et classification (GPT-4o-mini)")
        print("-" * 80)
        data_filtree = filtrer_et_classifier(articles_bruts)
        print()
        
        # Sauvegarde
        print("💾 ÉTAPE 3/3 : Sauvegarde du JSON")
        print("-" * 80)
        sauvegarder_json(data_filtree, OUTPUT_JSON)
        print()
        
        # Résumé
        print("=" * 80)
        print("✅ AGENT 1 NEWS TERMINÉ AVEC SUCCÈS")
        print("=" * 80)
        print(f"📊 Statistiques :")
        print(f"   - Articles bruts : {data_filtree['statistiques']['articles_bruts']}")
        print(f"   - Articles filtrés : {data_filtree['statistiques']['articles_finaux']}")
        print()
        print(f"📂 Fichier JSON : {OUTPUT_JSON}")
        print(f"🔗 Prêt pour Agent 2 (Synthèse)")
        print()
        
        sys.exit(0)
    
    except Exception as e:
        print("\n" + "=" * 80)
        print("❌ ERREUR FATALE")
        print("=" * 80)
        print(f"Type : {type(e).__name__}")
        print(f"Message : {e}")
        traceback.print_exc()
        print("=" * 80)
        sys.exit(1)


if __name__ == "__main__":
    main()
