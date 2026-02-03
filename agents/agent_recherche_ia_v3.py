"""
Agent Recherche IA v3 - Collecte PURE
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
OUTPUT_JSON = "recherche_ia_brute.json"
MAX_ARTICLES = 25

def collecter_actualites_ia() -> Dict[str, Any]:
    """
    Collecte brute des actualités IA via web search.
    AUCUNE analyse, AUCUN tri, AUCUNE synthèse.
    """
    if not OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY manquant")
        return {"articles": [], "erreur": "API key manquante"}
    
    client = OpenAI(api_key=OPENAI_API_KEY)
    date_fin = datetime.now()
    date_debut = date_fin - timedelta(days=7)
    
    # Prompt de collecte PURE optimisé
    prompt = f"""ROBOT DE COLLECTE D'ACTUALITÉS IA/LLM - AUCUNE ANALYSE

PÉRIODE: {date_debut.strftime('%d/%m/%Y')} au {date_fin.strftime('%d/%m/%Y')} (7 derniers jours)

SOURCES PRIORITAIRES (vérifier blogs/news officiels):
- Anthropic: anthropic.com/news
- OpenAI: openai.com/news | openai.com/research
- Mistral AI: mistral.ai/news
- DeepSeek: deepseekai.com
- The Hacker News (cybersecurity AI): thehackernews.com
- Hacker News AI discussions: news.ycombinator.com
- DeepLearning.AI: deeplearning.ai/the-batch
- Google AI Blog: blog.google/technology/ai
- NVIDIA AI: blogs.nvidia.com/blog/category/deep-learning
- Hugging Face: huggingface.co/blog
- Meta AI: ai.meta.com/blog
- AWS AI/ML: aws.amazon.com/blogs/machine-learning

OBJECTIF: Collecter EXACTEMENT 25 articles récents (publiés dans les 7 derniers jours)

CONSIGNES STRICTES:
1. Collecte BRUTE uniquement - PAS de sélection, PAS d'analyse, PAS de synthèse
2. Vérifier que chaque URL est valide et accessible
3. Extraire le contenu réel depuis les sources (pas de spéculation)
4. Diversifier les sources (pas plus de 3-4 articles par source)
5. Privilégier les annonces officielles et articles techniques

CATÉGORIES (choisir la plus pertinente):
- Nouveaux modèles LLM (sorties, benchmarks, capacités)
- Agents & Agentic AI (frameworks, orchestration, autonomie)
- Multimodal (vision, audio, vidéo intégrés aux LLM)
- Reasoning & Chain-of-Thought (o1, réflexion, planning)
- Open source (releases, fine-tuning, communauté)
- Recherche (papers, techniques, algorithmes)
- Régulation & Policy (lois, normes, gouvernance)
- Safety & Alignment (sécurité, éthique, red-teaming)
- Industrie & Applications (adoption entreprise, cas d'usage)
- Hardware & Infrastructure (GPUs, TPUs, optimisation)
- France & Europe (initiatives locales, startups, régulation EU)
- Asie (Chine, Japon, Corée - DeepSeek, etc.)

FORMAT JSON STRICT (sans markdown, sans commentaires):
{{
  "articles": [
    {{
      "titre": "Titre exact de l'article",
      "url": "https://source-officielle.com/article-complet",
      "source": "Nom de la source (ex: Anthropic, OpenAI)",
      "date_publication": "YYYY-MM-DD",
      "contenu_brut": "Résumé factuel de 2-3 phrases extrait du contenu réel de l'article",
      "categorie_auto": "Catégorie la plus pertinente parmi celles listées"
    }}
  ],
  "periode": {{
    "debut": "{date_debut.strftime('%Y-%m-%d')}", 
    "fin": "{date_fin.strftime('%Y-%m-%d')}"
  }},
  "nb_articles": 25
}}

EXEMPLE DE RÉSULTAT ATTENDU:
{{
  "titre": "Introducing Claude 3.5 Sonnet with improved coding abilities",
  "url": "https://www.anthropic.com/news/claude-3-5-sonnet",
  "source": "Anthropic",
  "date_publication": "2026-01-28",
  "contenu_brut": "Anthropic annonce une nouvelle version de Claude 3.5 Sonnet avec des capacités de codage améliorées, atteignant 95% sur SWE-bench. Le modèle introduit également de meilleures performances sur les tâches de raisonnement mathématique.",
  "categorie_auto": "Nouveaux modèles LLM"
}}

IMPORTANT:
- Retourner UNIQUEMENT le JSON (pas de texte avant/après)
- 25 articles OBLIGATOIRE (ni plus, ni moins)
- URLs complètes et valides
- Dates au format YYYY-MM-DD
- Contenu factuel (pas d'opinion)"""

    print(f"🌐 Lancement GPT-5.2 + web search LIVE...")
    print(f"📅 Recherche sur 7 jours : {date_debut.strftime('%d/%m')} - {date_fin.strftime('%d/%m')}")
    
    try:
        # Appel OpenAI Responses API (PAS de max_tokens avec GPT-5.2)
        response = client.responses.create(
            model=MODEL_RECHERCHE,
            tools=[{"type": "web_search", "external_web_access": True}],
            input=prompt
        )
        
        tokens_used = response.usage.total_tokens
        print(f"📊 Tokens utilisés : {tokens_used}")
        
        # Nettoyage du JSON
        json_text = response.output_text.strip()
        
        # Retirer les balises markdown si présentes
        if json_text.startswith('```'):
            lines = json_text.split('\n')
            json_text = '\n'.join(lines[1:-1]) if len(lines) > 2 else json_text
            json_text = json_text.replace('```json', '').replace('```', '').strip()
        
        # Parse JSON
        data = json.loads(json_text)
        
        # Validation basique
        if 'articles' not in data or not isinstance(data['articles'], list):
            raise ValueError("Format JSON invalide : clé 'articles' manquante ou invalide")
        
        # Enrichissement métadonnées
        data['date_collecte'] = date_fin.strftime('%Y-%m-%d %H:%M:%S')
        data['model_utilise'] = MODEL_RECHERCHE
        data['tokens_utilises'] = tokens_used
        data['agent'] = "Recherche IA v3"
        data['nb_articles'] = len(data.get('articles', []))
        
        # Génération ID unique pour chaque article
        for article in data.get('articles', []):
            hash_input = f"{article.get('url', '')}{article.get('titre', '')}"
            article['id'] = hashlib.md5(hash_input.encode()).hexdigest()[:12]
        
        print(f"✅ {data['nb_articles']} articles collectés")
        
        # Afficher la répartition par catégorie
        categories = {}
        for art in data['articles']:
            cat = art.get('categorie_auto', 'Non classé')
            categories[cat] = categories.get(cat, 0) + 1
        
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
        print("🤖 AGENT RECHERCHE IA v3 - COLLECTE PURE")
        print("=" * 80)
        print(f"📅 Période : 7 derniers jours")
        print(f"🎯 Objectif : {MAX_ARTICLES} articles EXACTEMENT")
        print(f"🌐 Modèle : {MODEL_RECHERCHE} + web search live")
        print()
        
        data = collecter_actualites_ia()
        
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
