"""
Agent 1 - Collecteur et Filtre IA
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

# Fichier de sortie - utiliser le répertoire courant pour GitHub Actions
OUTPUT_JSON = "articles_filtres_ia.json"


# ================================================================================
# TAVILY SEARCH
# ================================================================================

def recherche_tavily(query: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """
    Effectue une recherche web via Tavily API
    
    Args:
        query: Requête de recherche
        max_results: Nombre maximum de résultats
        
    Returns:
        Liste d'articles avec titre, URL, snippet, date
    """
    if not TAVILY_API_KEY:
        print("❌ TAVILY_API_KEY manquante")
        return []
    
    url = "https://api.tavily.com/search"
    
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "max_results": max_results,
        "search_depth": "basic",  # basic = rapide et économique
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
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur HTTP Tavily pour '{query}': {e}")
        return []
    except Exception as e:
        print(f"❌ Erreur inattendue Tavily pour '{query}': {e}")
        traceback.print_exc()
        return []


# ================================================================================
# COLLECTE MULTI-REQUÊTES
# ================================================================================

def collecter_articles_bruts() -> List[Dict[str, Any]]:
    """
    Lance 12 recherches ciblées sur différents thèmes IA/LLM
    
    Returns:
        Liste brute d'articles (avec doublons potentiels)
    """
    
    # Calculer la période (7 derniers jours)
    date_fin = datetime.now()
    date_debut = date_fin - timedelta(days=7)
    
    # Requêtes ciblées pour maximiser la couverture
    requetes = [
        "AI LLM news this week",
        "OpenAI GPT latest announcements",
        "Anthropic Claude updates",
        "Google Gemini AI news",
        "Meta Llama open source",
        "AI regulation Europe 2026",
        "AI research papers this week",
        "AI cybersecurity threats",
        "enterprise AI applications",
        "AI hardware chips news",
        "AI France Nantes startup",
        "open source AI models"
    ]
    
    print(f"🔍 Lancement de {len(requetes)} recherches Tavily...")
    
    articles_bruts = []
    for i, query in enumerate(requetes, 1):
        print(f"  [{i}/{len(requetes)}] {query}")
        resultats = recherche_tavily(query, max_results=8)
        
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
        print("⚠️  Aucun article collecté - vérifier la connexion Tavily")
    
    return articles_bruts


# ================================================================================
# FILTRAGE ET CLASSIFICATION GPT-4o-mini
# ================================================================================

def filtrer_et_classifier(articles_bruts: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Utilise GPT-4o-mini pour :
    - Supprimer doublons
    - Filtrer pertinence IA/LLM
    - Classifier par thème
    - Attribuer score de pertinence
    
    Args:
        articles_bruts: Liste d'articles bruts
        
    Returns:
        Dictionnaire JSON structuré prêt pour Agent 2
    """
    
    if len(articles_bruts) == 0:
        print("⚠️  Pas d'articles à filtrer, création d'un JSON vide")
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
    
    # Calculer dates
    date_fin = datetime.now()
    date_debut = date_fin - timedelta(days=7)
    
    # Préparer les articles pour le prompt (limiter à 100 pour éviter dépassement tokens)
    articles_input = articles_bruts[:100]
    print(f"📝 Préparation de {len(articles_input)} articles pour GPT-4o-mini...")
    
    # Créer un texte compact pour GPT
    articles_text = "\n\n".join([
        f"[{i+1}] {art['titre']}\nURL: {art['url']}\nSnippet: {art['snippet'][:200]}..."
        for i, art in enumerate(articles_input)
    ])
    
    prompt = f"""Tu es un agent de filtrage et classification d'actualités IA/LLM.

**PÉRIODE ANALYSÉE** : du {date_debut.strftime('%d/%m/%Y')} au {date_fin.strftime('%d/%m/%Y')}

**ARTICLES BRUTS À ANALYSER** :
{articles_text}

**TA MISSION** :
1. Supprimer les doublons (même sujet, sources différentes → garder la meilleure)
2. Filtrer uniquement les articles pertinents sur IA/LLM/GenAI
3. Exclure : annonces mineures, marketing produits, tutoriels basiques
4. Classifier chaque article dans UN thème principal :
   - Nouveaux modèles LLM
   - Open source & écosystèmes
   - Recherche scientifique
   - Régulation & gouvernance
   - Industrie & investissements
   - Cybersécurité & risques
   - Applications entreprises
   - Hardware & compute
   - Europe & France
   - Nantes & Région Ouest

5. Attribuer un score de pertinence (1-10) selon l'importance de l'actualité

**FORMAT DE SORTIE JSON** :
```json
{{
  "articles": [
    {{
      "titre": "Titre exact de l'article",
      "source": "Nom du média (ex: TechCrunch, Le Monde)",
      "url": "URL complète",
      "date_estimee": "2026-01-10",
      "theme": "Nouveaux modèles LLM",
      "snippet": "Résumé en 2-3 lignes des points clés",
      "pertinence": 9,
      "tags": ["GPT-5", "OpenAI", "benchmark"]
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
- Vise 12-18 articles finaux maximum (les plus importants)
- Reformule les snippets (pas de copier-coller)
- Détecte les doublons même avec titres légèrement différents
- Sois strict sur la pertinence (ignorer le bruit médiatique)

Génère le JSON maintenant :"""

    print("🤖 Appel API GPT-4o-mini pour filtrage...")
    
    try:
        response = client.chat.completions.create(
            model=MODEL_COLLECTEUR,
            messages=[
                {"role": "system", "content": "Tu es un agent de filtrage d'actualités IA. Tu réponds UNIQUEMENT en JSON valide, sans markdown, sans commentaires."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,  # Peu créatif, très factuel
            max_tokens=4000
        )
        
        # Extraire le JSON de la réponse
        print(f"📊 Tokens utilisés : {response.usage.total_tokens} (prompt: {response.usage.prompt_tokens}, completion: {response.usage.completion_tokens})")
        
        json_text = response.choices[0].message.content.strip()
        
        # Nettoyer les backticks markdown si présents
        if json_text.startswith('```'):
            lines = json_text.split('\n')
            json_text = '\n'.join(lines[1:-1]) if len(lines) > 2 else json_text
            json_text = json_text.replace('```json', '').replace('```', '').strip()
        
        print(f"📝 Parsing de la réponse JSON ({len(json_text)} caractères)...")
        
        # Parser le JSON
        data = json.loads(json_text)
        
        # Ajouter métadonnées
        data['date_collecte'] = date_fin.strftime('%Y-%m-%d')
        data['periode'] = {
            'debut': date_debut.strftime('%Y-%m-%d'),
            'fin': date_fin.strftime('%Y-%m-%d')
        }
        data['model_utilise'] = MODEL_COLLECTEUR
        
        # Générer IDs uniques pour chaque article
        for article in data['articles']:
            hash_input = f"{article['url']}{article['titre']}"
            article['id'] = hashlib.md5(hash_input.encode()).hexdigest()[:12]
        
        # Calculer statistiques thématiques
        themes_count = {}
        for article in data['articles']:
            theme = article['theme']
            themes_count[theme] = themes_count.get(theme, 0) + 1
        
        data['themes'] = themes_count
        data['statistiques']['articles_finaux'] = len(data['articles'])
        
        print(f"✅ Filtrage terminé : {len(data['articles'])} articles retenus")
        
        return data
    
    except json.JSONDecodeError as e:
        print(f"❌ Erreur parsing JSON : {e}")
        print(f"Réponse brute (premiers 500 car) : {json_text[:500]}...")
        raise
    
    except Exception as e:
        print(f"❌ Erreur GPT-4o-mini : {e}")
        traceback.print_exc()
        raise


# ================================================================================
# SAUVEGARDE JSON
# ================================================================================

def sauvegarder_json(data: Dict[str, Any], filepath: str) -> None:
    """
    Sauvegarde le JSON structuré
    
    Args:
        data: Données à sauvegarder
        filepath: Chemin du fichier
    """
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
    """Point d'entrée principal de l'agent collecteur"""
    
    try:
        print("=" * 80)
        print("🤖 AGENT 1 - COLLECTEUR IA (GPT-4o-mini)")
        print("=" * 80)
        print(f"⏰ Exécution : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"📂 Répertoire de travail : {os.getcwd()}")
        print()
        
        # Vérifier les clés API
        print("🔑 Vérification des clés API...")
        if not OPENAI_API_KEY:
            print("❌ ERREUR CRITIQUE : OPENAI_API_KEY manquante")
            sys.exit(1)
        else:
            print(f"✅ OPENAI_API_KEY présente ({OPENAI_API_KEY[:10]}...)")
        
        if not TAVILY_API_KEY:
            print("❌ ERREUR CRITIQUE : TAVILY_API_KEY manquante")
            sys.exit(1)
        else:
            print(f"✅ TAVILY_API_KEY présente ({TAVILY_API_KEY[:10]}...)")
        
        print()
        
        # Étape 1 : Collecte brute via Tavily
        print("📡 ÉTAPE 1/3 : Collecte d'articles via Tavily")
        print("-" * 80)
        articles_bruts = collecter_articles_bruts()
        print()
        
        # Étape 2 : Filtrage et classification via GPT-4o-mini
        print("🧹 ÉTAPE 2/3 : Filtrage et classification (GPT-4o-mini)")
        print("-" * 80)
        data_filtree = filtrer_et_classifier(articles_bruts)
        print()
        
        # Étape 3 : Sauvegarde JSON
        print("💾 ÉTAPE 3/3 : Sauvegarde du JSON structuré")
        print("-" * 80)
        sauvegarder_json(data_filtree, OUTPUT_JSON)
        print()
        
        # Résumé final
        print("=" * 80)
        print("✅ AGENT 1 TERMINÉ AVEC SUCCÈS")
        print("=" * 80)
        print(f"📊 Statistiques finales :")
        print(f"   - Articles bruts collectés : {data_filtree['statistiques']['articles_bruts']}")
        print(f"   - Articles après filtrage : {data_filtree['statistiques']['articles_finaux']}")
        print(f"   - Doublons supprimés : {data_filtree['statistiques'].get('doublons_supprimes', 0)}")
        print()
        print(f"📂 Fichier JSON : {OUTPUT_JSON}")
        print(f"🔗 Prêt pour Agent 2 (Synthèse)")
        print()
        
        sys.exit(0)
    
    except KeyboardInterrupt:
        print("\n⚠️  Interruption manuelle (Ctrl+C)")
        sys.exit(130)
    
    except Exception as e:
        print("\n" + "=" * 80)
        print("❌ ERREUR FATALE")
        print("=" * 80)
        print(f"Type d'erreur : {type(e).__name__}")
        print(f"Message : {e}")
        print("\nTraceback complet :")
        traceback.print_exc()
        print("=" * 80)
        sys.exit(1)


if __name__ == "__main__":
    main()
