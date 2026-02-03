#!/usr/bin/env python3
"""
Script de nettoyage du repository VeilleNLI
Supprime tous les fichiers et dossiers obsolètes pour ne garder que le nécessaire
pour le workflow "Veille OpenAI v3 - Architecture Séparée (Collecte | Synthèse)"

Usage:
    python scripts/cleanup_repository.py                    # Simulation
    python scripts/cleanup_repository.py --execute          # Exécution avec confirmation
    python scripts/cleanup_repository.py --execute --yes    # Exécution sans confirmation (CI/CD)
"""
import os
import sys
from pathlib import Path
from typing import List

# Liste des fichiers à SUPPRIMER
FILES_TO_DELETE: List[str] = [
    # ===== Workflows obsolètes =====
    '.github/workflows/CLEANUP_README.md',
    '.github/workflows/deep-research-daily.yml',
    '.github/workflows/deep-research-daily.yml.disabled',
    '.github/workflows/list-models.yml',
    '.github/workflows/list-models.yml.disabled',
    '.github/workflows/update-data.yml',
    '.github/workflows/update-data.yml.disabled',
    '.github/workflows/veille-openai-complete.yml',
    '.github/workflows/veille-openai-complete.yml.disabled',
    '.github/workflows/veille-quotidienne.yml',
    '.github/workflows/veille-quotidienne.yml.disabled',
    '.github/workflows/veille-quotidienne.yml.disabled2',
    
    # ===== Documentation obsolète =====
    'ARCHITECTURE_4_AGENTS.md',
    'ARCHITECTURE_MEMOIRE.md',
    'CHANGELOG.md',
    'DEEP_RESEARCH_MIGRATION.md',
    'DOCS.md',
    'DOCUMENTATION_TECHNIQUE.md',
    'MIGRATION_4_AGENTS_SUMMARY.md',
    'MIGRATION_COMPLETE.md',
    'README_MIGRATION_V2.md',
    'README_V3.md',
    'RECAP_PHASE1.md',
    'VALIDATION_TESTS.md',
    
    # ===== Agents obsolètes (v1, v2, anciens) =====
    'agents/agent_collecteur_ia.py',
    'agents/agent_collecteur_news.py',
    'agents/agent_formatter.py',
    'agents/agent_recherche_ia.py',
    'agents/agent_recherche_news.py',
    'agents/agent_synthese_ia.py',
    'agents/agent_synthese_ia_v2.py',
    'agents/agent_synthese_news.py',
    'agents/agent_synthese_news_v2.py',
    'agents/deep_research_ia.py',
    'agents/deep_research_news.py',
    
    # ===== Tests obsolètes =====
    'test_agents_ia.py',
]

# Dossiers à supprimer entièrement (récursivement)
FOLDERS_TO_DELETE: List[str] = [
    'archive',
    'config',
]

# Fichiers/dossiers à CONSERVER (référence pour validation)
MUST_KEEP: List[str] = [
    # Workflow actif
    '.github/workflows/veille-openai-v3.yml',
    
    # Agents v3 actifs
    'agents/agent_recherche_ia_v3.py',
    'agents/agent_synthese_ia_v3.py',
    'agents/agent_recherche_news_v3.py',
    'agents/agent_synthese_news_v3.py',
    'agents/agent_validateur_markdown.py',
    'agents/agent_generateur_json.py',
    
    # Scripts
    'scripts/list_openai_models.py',
    
    # Config & Doc
    'requirements.txt',
    'README.md',
    
    # Site web
    'docs/',
]


def delete_files(dry_run: bool = True) -> None:
    """
    Supprime tous les fichiers listés dans FILES_TO_DELETE
    
    Args:
        dry_run: Si True, affiche seulement ce qui serait supprimé (défaut: True)
    """
    deleted_count = 0
    not_found_count = 0
    
    print("=" * 80)
    print(f"{'🔍 SIMULATION' if dry_run else '🗑️  SUPPRESSION'} DES FICHIERS")
    print("=" * 80)
    print()
    
    for file_path in FILES_TO_DELETE:
        full_path = Path(file_path)
        
        if full_path.exists():
            if dry_run:
                print(f"  ❌ [SIMUL] {file_path}")
            else:
                try:
                    full_path.unlink()
                    print(f"  ✅ [SUPPRIMÉ] {file_path}")
                except Exception as e:
                    print(f"  ⚠️  [ERREUR] {file_path}: {e}")
                    continue
            deleted_count += 1
        else:
            print(f"  ⏭️  [ABSENT] {file_path}")
            not_found_count += 1
    
    print()
    print(f"📊 Résumé fichiers:")
    print(f"  • Supprimés/À supprimer: {deleted_count}")
    print(f"  • Déjà absents: {not_found_count}")
    print()


def delete_folders(dry_run: bool = True) -> None:
    """
    Supprime tous les dossiers listés dans FOLDERS_TO_DELETE
    
    Args:
        dry_run: Si True, affiche seulement ce qui serait supprimé (défaut: True)
    """
    deleted_count = 0
    not_found_count = 0
    
    print("=" * 80)
    print(f"{'🔍 SIMULATION' if dry_run else '🗑️  SUPPRESSION'} DES DOSSIERS")
    print("=" * 80)
    print()
    
    for folder_path in FOLDERS_TO_DELETE:
        full_path = Path(folder_path)
        
        if full_path.exists() and full_path.is_dir():
            if dry_run:
                # Compter les fichiers pour info
                file_count = sum(1 for _ in full_path.rglob('*') if _.is_file())
                print(f"  📁❌ [SIMUL] {folder_path}/ ({file_count} fichiers)")
            else:
                try:
                    import shutil
                    shutil.rmtree(full_path)
                    print(f"  ✅ [SUPPRIMÉ] {folder_path}/")
                except Exception as e:
                    print(f"  ⚠️  [ERREUR] {folder_path}/: {e}")
                    continue
            deleted_count += 1
        else:
            print(f"  ⏭️  [ABSENT] {folder_path}/")
            not_found_count += 1
    
    print()
    print(f"📊 Résumé dossiers:")
    print(f"  • Supprimés/À supprimer: {deleted_count}")
    print(f"  • Déjà absents: {not_found_count}")
    print()


def verify_must_keep() -> bool:
    """
    Vérifie que tous les fichiers critiques sont bien présents
    
    Returns:
        True si tous les fichiers critiques existent, False sinon
    """
    print("=" * 80)
    print("🔍 VÉRIFICATION DES FICHIERS CRITIQUES")
    print("=" * 80)
    print()
    
    all_ok = True
    
    for item in MUST_KEEP:
        path = Path(item)
        exists = path.exists()
        
        if exists:
            print(f"  ✅ {item}")
        else:
            print(f"  ❌ MANQUANT: {item}")
            all_ok = False
    
    print()
    if all_ok:
        print("✅ Tous les fichiers critiques sont présents")
    else:
        print("⚠️  ATTENTION: Des fichiers critiques sont manquants!")
    print()
    
    return all_ok


def main():
    """Point d'entrée principal"""
    print()
    print("🧹 NETTOYAGE DU REPOSITORY VeilleNLI")
    print("=" * 80)
    print()
    print("Ce script supprime tous les fichiers et dossiers obsolètes")
    print("pour ne garder que le nécessaire pour le workflow v3.")
    print()
    print(f"📋 Fichiers à supprimer: {len(FILES_TO_DELETE)}")
    print(f"📁 Dossiers à supprimer: {len(FOLDERS_TO_DELETE)}")
    print()
    
    # Mode d'exécution
    execute_mode = '--execute' in sys.argv or '-x' in sys.argv
    skip_confirmation = '--yes' in sys.argv or '-y' in sys.argv
    
    if execute_mode:
        dry_run = False
        print("⚠️  MODE EXÉCUTION: Les fichiers seront réellement supprimés!")
        print()
        
        # Demander confirmation seulement si --yes n'est pas présent
        if not skip_confirmation:
            confirm = input("Taper 'OUI' pour confirmer: ")
            if confirm != 'OUI':
                print("❌ Opération annulée")
                sys.exit(1)
        else:
            print("✅ Confirmation automatique (--yes)")
    else:
        dry_run = True
        print("🔍 MODE SIMULATION (utilisez --execute pour supprimer réellement)")
    
    print()
    
    # Vérifier les fichiers critiques AVANT suppression
    if not verify_must_keep():
        print("❌ Abandon: fichiers critiques manquants")
        sys.exit(1)
    
    # Supprimer les fichiers
    delete_files(dry_run=dry_run)
    
    # Supprimer les dossiers
    delete_folders(dry_run=dry_run)
    
    # Résumé final
    print("=" * 80)
    if dry_run:
        print("✅ SIMULATION TERMINÉE")
        print()
        print("Pour effectuer le nettoyage réel, exécutez:")
        print("  python scripts/cleanup_repository.py --execute")
        print()
        print("Pour skip la confirmation (CI/CD):")
        print("  python scripts/cleanup_repository.py --execute --yes")
    else:
        print("✅ NETTOYAGE TERMINÉ")
        print()
        print("Prochaine étape: Commit et push des modifications")
        print("  git add -A")
        print("  git commit -m '🧹 Nettoyage du repository (suppression fichiers obsolètes)'")
        print("  git push origin main")
    print("=" * 80)
    print()


if __name__ == '__main__':
    main()
