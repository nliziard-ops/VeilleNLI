"""
Agent 2 - Recherche Web News
Modèle : GPT-4 Turbo (ChatGPT)
Rôle : Collecte factuelle depuis presse nationale/internationale/locale
Sans interprétation ni analyse - Restitution brute : catégorie, titre, résumé, synthèse, source+lien
"""

import os
import sys
import json
import hashlib
import traceback
from datetime import datetime, timedelta
from typing import Dict, Any
from openai import OpenAI


# ================================================================================
# CONFIGURATION
# ================================================================================

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# Modèle ChatGPT-4 Turbo pour recherche web
MODEL_RECHERCHE = "gpt-4-turbo-preview"

# Fichier de sortie
OUTPUT_JSON = "recherche_news_brute.json"

# Sources presse (définies par Nicolas)
SOURCES_NEWS = [
    # INTERNATIONAL
    "https://legrandcontinent.eu/fr/",
    "https://elpais.com/",
    "https://www.bbc.com/news",          # Ajout institutionnel
    "https://www.reuters.com",           # Ajout institutionnel
    
    # NATIONAL FRANCE
    "https://www.lefigaro.fr/",
    "https://www.lemonde.fr/",
    "https://www.monde-diplomatique.fr/",
    
    # LOCAL BRETAGNE/PAYS DE LOIRE
    "https://www.ouest-france.fr/",
    "https://www.letelegramme.fr/"
]


# ================================================================================
# RECHERCHE WEB NEWS AVEC CHATGPT-4 TURBO
# ================================================================================

def rechercher_actualites_news() -> Dict[str, Any]:
    """
    Utilise ChatGPT-4 Turbo avec web_search pour collecter
    actualités depuis presse nationale/internationale/locale.
    
    Returns:
        Dictionnaire JSON avec articles catégorisés
    """
    
    if not OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY manquante")
        return {"articles": []}
    
    print(f"🔍 Création client OpenAI pour recherche web...")
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    # Calculer période (7 derniers jours)
    date_fin = datetime.now()
    date_debut = date_fin - timedelta(days=7)
    
    # Préparer liste sources
    sources_text = "\n".join([f"- {source}" for source in SOURCES_NEWS])
    
    # Construire prompt de recherche factuelle
    prompt = f"""Tu es un collecteur d'informations factuelles d'actualités.

**PÉRIODE** : du {date_debut.strftime('%d/%m/%Y')} au {date_fin.strftime('%d/%m/%Y')}

**SOURCES PRIORITAIRES À CONSULTER** :
{sources_text}

**DISTRIBUTION GÉOGRAPHIQUE CIBLE** :
- 35% International (géopolitique, économie mondiale, crises)
- 35% France (politique, économie, société)
- 30% Local Bretagne/Pays de Loire/Nantes (politique locale, économie régionale, sports maritimes : voile, surf, kitesurf, wingfoil)

**TA MISSION - COLLECTE FACTUELLE UNIQUEMENT** :
1. Recherche les actualités importantes publiées cette semaine sur ces sources
2. Pour chaque actualité trouvée, extrais UNIQUEMENT les faits :
   - Titre exact de l'article
   - Résumé court (2-3 lignes) - FACTS ONLY
   - Contenu factuel complet (qui, quoi, quand, où, pourquoi, comment)
   - Source exacte (nom du média)
   - URL complète
   - Date de publication

3. Catégorise chaque actualité dans l'un de ces thèmes :
   **INTERNATIONAL** :
   - "Géopolitique" (conflits, diplomatie, relations internationales)
   - "Économie mondiale" (marchés, commerce, crises)
   - "Environnement" (climat, biodiversité, catastrophes)
   
   **FRANCE** :
   - "Politique nationale" (gouvernement, lois, élections)
   - "Économie France" (entreprises, emploi, budget)
   - "Société" (mouvement sociaux, justice, éducation)
   
   **LOCAL BRETAGNE/PAYS DE LOIRE** :
   - "Politique locale" (région, département, mairies)
   - "Économie régionale" (entreprises locales, emploi)
   - "Sports maritimes" (voile, surf, kitesurf, wingfoil, compétitions)
   - "Mer & littoral" (ports, pêche, environnement marin)
   - "Culture Bretagne" (événements, patrimoine)

**FORMAT DE SORTIE JSON - STRUCTURE OBLIGATOIRE** :
Réponds UNIQUEMENT avec un JSON valide suivant ce format exact :

Articles sous forme de liste avec pour chaque article :
- categorie (string)
- zone_geo (string : "International", "National" ou "Local")
- titre (string)
- resume_court (string de 2-3 lignes)
- synthese_complete (string factuelle)
- source (string, nom du média)
- url (string, URL complète)
- date_publication (string format YYYY-MM-DD)

Ajoute aussi :
- periode avec debut et fin
- repartition avec international, national, local (nombres)
- sources_consultees (liste)

**CONSIGNES CRITIQUES** :
- Vise 15-20 actualités maximum (limite tokens)
- Respecte la distribution : ~35% international, ~35% national, ~30% local
- UNIQUEMENT des faits vérifiables
- AUCUNE interprétation, analyse, opinion
- Citations exactes quand pertinent
- URLs complètes obligatoires
- Pour le local : focus Nantes, Brest, Belle-Île-en-Mer, Le Palais
- Sports maritimes = priorité (voile, surf, kitesurf, wingfoil)

**IMPORTANT** :
Tu es un COLLECTEUR, pas un ANALYSTE.
Tu retranscris les informations telles qu'elles apparaissent.

Utilise la fonction web_search pour accéder aux sites de presse.
Génère le JSON maintenant, sans préambule."""

    print("🌐 Lancement recherche web ChatGPT-4 Turbo...")
    
    try:
        # Appel API ChatGPT-4 Turbo
        response = client.chat.completions.create(
            model=MODEL_RECHERCHE,
            messages=[
                {
                    "role": "system",
                    "content": "Tu es un collecteur d'informations factuelles. Tu réponds UNIQUEMENT en JSON valide, sans markdown, sans commentaires. Tu utilises web_search pour accéder aux sites."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1,  # Très factuel
            max_tokens=4000   # RÉDUIT : max 4096 pour gpt-4-turbo-preview
        )
        
        print(f"📊 Tokens utilisés : {response.usage.total_tokens} (prompt: {response.usage.prompt_tokens}, completion: {response.usage.completion_tokens})")
        
        # Coût GPT-4 Turbo
        cost_input = (response.usage.prompt_tokens / 1000) * 0.01
        cost_output = (response.usage.completion_tokens / 1000) * 0.03
        cost_total = cost_input + cost_output
        print(f"💰 Coût estimé : ${cost_total:.4f}")
        
        # Extraire JSON
        json_text = response.choices[0].message.content.strip()
        
        # Nettoyer markdown
        if json_text.startswith('```'):
            lines = json_text.split('\n')
            json_text = '\n'.join(lines[1:-1]) if len(lines) > 2 else json_text
            json_text = json_text.replace('```json', '').replace('```', '').strip()
        
        print(f"📝 Parsing JSON ({len(json_text)} caractères)...")
        
        data = json.loads(json_text)
        
        # Ajouter métadonnées
        data['date_collecte'] = date_fin.strftime('%Y-%m-%d')
        data['model_utilise'] = MODEL_RECHERCHE
        data['agent'] = "Recherche News"
        
        # Vérifier structure
        if 'periode' not in data:
            data['periode'] = {
                'debut': date_debut.strftime('%Y-%m-%d'),
                'fin': date_fin.strftime('%Y-%m-%d')
            }
        
        # Calculer répartition géographique
        if 'repartition' not in data:
            data['repartition'] = {'international': 0, 'national': 0, 'local': 0}
        
        for article in data.get('articles', []):
            # Générer ID unique
            hash_input = f"{article.get('url', '')}{article.get('titre', '')}"
            article['id'] = hashlib.md5(hash_input.encode()).hexdigest()[:12]
            
            # Compter répartition
            zone = article.get('zone_geo', 'National')
            if zone == 'International':
                data['repartition']['international'] += 1
            elif zone == 'Local':
                data['repartition']['local'] += 1
            else:
                data['repartition']['national'] += 1
        
        total_articles = len(data.get('articles', []))
        print(f"✅ Recherche terminée : {total_articles} articles")
        if total_articles > 0:
            print(f"🌍 Répartition : International {data['repartition']['international']}, National {data['repartition']['national']}, Local {data['repartition']['local']}")
        
        return data
    
    except json.JSONDecodeError as e:
        print(f"❌ Erreur parsing JSON : {e}")
        print(f"Réponse brute (premiers 500 car) : {json_text[:500]}...")
        raise
    
    except Exception as e:
        print(f"❌ Erreur ChatGPT-4 Turbo : {e}")
        traceback.print_exc()
        raise


# ================================================================================
# SAUVEGARDE JSON
# ================================================================================

def sauvegarder_json(data: Dict[str, Any], filepath: str) -> None:
    """
    Sauvegarde le JSON de recherche brute
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
    """Point d'entrée principal de l'agent recherche News"""
    
    try:
        print("=" * 80)
        print("🤖 AGENT 2 - RECHERCHE WEB NEWS (ChatGPT-4 Turbo)")
        print("=" * 80)
        print(f"⏰ Exécution : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"📂 Répertoire de travail : {os.getcwd()}")
        print()
        
        # Vérifier clé API
        print("🔑 Vérification clé API...")
        if not OPENAI_API_KEY:
            print("❌ ERREUR CRITIQUE : OPENAI_API_KEY manquante")
            sys.exit(1)
        else:
            print(f"✅ OPENAI_API_KEY présente ({OPENAI_API_KEY[:10]}...)")
        
        print()
        
        # Recherche web
        print("📡 RECHERCHE WEB FACTUELLE NEWS")
        print("-" * 80)
        print("Sources presse :")
        for source in SOURCES_NEWS:
            print(f"  • {source}")
        print()
        print("Distribution cible : 35% International, 35% National, 30% Local")
        print()
        
        data = rechercher_actualites_news()
        print()
        
        # Sauvegarde
        print("💾 SAUVEGARDE JSON")
        print("-" * 80)
        sauvegarder_json(data, OUTPUT_JSON)
        print()
        
        # Résumé
        print("=" * 80)
        print("✅ AGENT 2 RECHERCHE NEWS TERMINÉ")
        print("=" * 80)
        print(f"📊 {len(data.get('articles', []))} articles collectés")
        print(f"📂 Fichier JSON : {OUTPUT_JSON}")
        print(f"🔗 Prêt pour Agent 4 (Synthèse News)")
        print()
        
        sys.exit(0)
    
    except KeyboardInterrupt:
        print("\n⚠️  Interruption manuelle (Ctrl+C)")
        sys.exit(130)
    
    except Exception as e:
        print("\n" + "=" * 80)
        print("❌ ERREUR FATALE")
        print("=" * 80)
        print(f"Type : {type(e).__name__}")
        print(f"Message : {e}")
        print("\nTraceback :")
        traceback.print_exc()
        print("=" * 80)
        sys.exit(1)


if __name__ == "__main__":
    main()
