#!/usr/bin/env python3
"""
Script pour lister les modèles OpenAI disponibles
Usage temporaire pour vérifier les versions GPT-5.2
"""

import os
from openai import OpenAI

print("="*80)
print("🔍 LISTE DES MODÈLES OPENAI DISPONIBLES")
print("="*80)
print()

# Vérifier la clé API
api_key = os.environ.get('OPENAI_API_KEY')
if not api_key:
    print("❌ ERREUR : OPENAI_API_KEY manquante")
    exit(1)

print("🔑 Clé API trouvée")
print("🤖 Initialisation client OpenAI...")

client = OpenAI(api_key=api_key)

print("📡 Récupération de la liste des modèles...")
print()

try:
    models = client.models.list()
    ids = [m.id for m in models.data]
    
    print("="*80)
    print("📊 TOUS LES MODÈLES DISPONIBLES")
    print("="*80)
    print(f"Total : {len(ids)} modèles\n")
    
    for model_id in sorted(ids):
        print(f"  - {model_id}")
    
    print("\n" + "="*80)
    print("🔬 MODÈLES GPT-5.2")
    print("="*80)
    gpt52_models = [m for m in ids if "gpt-5.2" in m.lower()]
    
    if gpt52_models:
        print(f"Trouvés : {len(gpt52_models)} modèle(s)\n")
        for model in gpt52_models:
            print(f"  ✅ {model}")
    else:
        print("❌ Aucun modèle GPT-5.2 trouvé")
        print("\n💡 Modèles GPT-5 disponibles :")
        gpt5_models = [m for m in ids if "gpt-5" in m.lower()]
        if gpt5_models:
            for model in gpt5_models:
                print(f"  - {model}")
        else:
            print("  Aucun modèle GPT-5.x trouvé")
    
    print("\n" + "="*80)
    print("🤖 MODÈLES GPT-4")
    print("="*80)
    gpt4_models = [m for m in ids if "gpt-4" in m.lower()]
    print(f"Trouvés : {len(gpt4_models)} modèle(s)\n")
    for model in sorted(gpt4_models)[:10]:  # Afficher les 10 premiers
        print(f"  - {model}")
    if len(gpt4_models) > 10:
        print(f"  ... et {len(gpt4_models) - 10} autres modèles GPT-4")
    
    print("\n" + "="*80)
    print("🔬 MODÈLES O1 (REASONING)")
    print("="*80)
    o1_models = [m for m in ids if "o1" in m.lower()]
    if o1_models:
        print(f"Trouvés : {len(o1_models)} modèle(s)\n")
        for model in o1_models:
            print(f"  - {model}")
    else:
        print("❌ Aucun modèle o1 trouvé")
    
    print("\n" + "="*80)
    print("✅ RÉCUPÉRATION TERMINÉE")
    print("="*80)
    
except Exception as e:
    print(f"\n❌ ERREUR lors de la récupération : {e}")
    import traceback
    traceback.print_exc()
    exit(1)
