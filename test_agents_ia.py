#!/usr/bin/env python3
"""
Script de test pour les agents OpenAI
Usage: python test_agents_ia.py
"""

import sys
import os
from pathlib import Path

# Ajouter le dossier agents au path
sys.path.insert(0, str(Path(__file__).parent / 'agents'))

def test_agent_1():
    """Test Agent 1 - Collecteur"""
    print("\n" + "="*80)
    print("🧪 TEST AGENT 1 - COLLECTEUR (GPT-4o-mini)")
    print("="*80 + "\n")
    
    try:
        from agent_collecteur_ia import main as agent1_main
        agent1_main()
        
        # Vérifier que le JSON existe
        json_path = "/tmp/articles_filtres_ia.json"
        if os.path.exists(json_path):
            import json
            with open(json_path, 'r') as f:
                data = json.load(f)
            
            print("\n✅ AGENT 1 - TEST RÉUSSI")
            print(f"   Articles filtrés : {len(data['articles'])}")
            print(f"   Thèmes : {list(data.get('themes', {}).keys())}")
            return True
        else:
            print("\n❌ AGENT 1 - ÉCHEC : JSON non créé")
            return False
            
    except Exception as e:
        print(f"\n❌ AGENT 1 - ERREUR : {e}")
        import traceback
        traceback.print_exc()
        return False


def test_agent_2():
    """Test Agent 2 - Synthétiseur"""
    print("\n" + "="*80)
    print("🧪 TEST AGENT 2 - SYNTHÉTISEUR (GPT-4o)")
    print("="*80 + "\n")
    
    # Vérifier que le JSON existe
    json_path = "/tmp/articles_filtres_ia.json"
    if not os.path.exists(json_path):
        print("❌ AGENT 2 - PRÉREQUIS MANQUANT : JSON de l'Agent 1 introuvable")
        print("   Lancer d'abord Agent 1")
        return False
    
    try:
        from agent_synthese_ia import main as agent2_main
        agent2_main()
        
        print("\n✅ AGENT 2 - TEST RÉUSSI")
        print("   Synthèse uploadée sur Google Drive")
        return True
            
    except Exception as e:
        print(f"\n❌ AGENT 2 - ERREUR : {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Lance les tests des 2 agents"""
    
    print("\n" + "="*80)
    print("🚀 TEST COMPLET - SYSTÈME 2 AGENTS OPENAI")
    print("="*80)
    print("\n📋 Vérification des prérequis...")
    
    # Vérifier les variables d'environnement
    required_vars = {
        'OPENAI_API_KEY': '🔑 OpenAI API',
        'TAVILY_API_KEY': '🔍 Tavily Search',
        'GOOGLE_DRIVE_CREDENTIALS': '☁️  Google Drive',
        'GOOGLE_DRIVE_FOLDER_ID': '📁 Folder ID'
    }
    
    missing = []
    for var, name in required_vars.items():
        if os.environ.get(var):
            print(f"   ✅ {name}")
        else:
            print(f"   ❌ {name} - {var} manquante")
            missing.append(var)
    
    if missing:
        print(f"\n❌ Variables manquantes : {', '.join(missing)}")
        print("\n💡 Pour tester localement, créer un fichier .env avec :")
        for var in missing:
            print(f"   {var}=...")
        return
    
    # Test Agent 1
    success_1 = test_agent_1()
    
    if not success_1:
        print("\n⚠️  Agent 1 a échoué, impossible de tester Agent 2")
        return
    
    # Test Agent 2
    success_2 = test_agent_2()
    
    # Résumé final
    print("\n" + "="*80)
    print("📊 RÉSUMÉ DES TESTS")
    print("="*80)
    print(f"   Agent 1 (Collecteur) : {'✅ RÉUSSI' if success_1 else '❌ ÉCHEC'}")
    print(f"   Agent 2 (Synthétiseur) : {'✅ RÉUSSI' if success_2 else '❌ ÉCHEC'}")
    
    if success_1 and success_2:
        print("\n🎉 TOUS LES TESTS PASSÉS AVEC SUCCÈS !")
        print("\n📋 Prochaines étapes :")
        print("   1. Vérifier le fichier VeilleIA.md sur Google Drive")
        print("   2. Valider la qualité de la synthèse")
        print("   3. Créer le workflow GitHub Actions pour automatisation")
    else:
        print("\n⚠️  Certains tests ont échoué")
    
    print()


if __name__ == "__main__":
    main()
