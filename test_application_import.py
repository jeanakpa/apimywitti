#!/usr/bin/env python3
"""
Test script pour vérifier l'import de application.py
"""

import os
import sys

# Ajouter le répertoire courant au PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Ajouter tous les sous-répertoires au PYTHONPATH
for root, dirs, files in os.walk(current_dir):
    for dir_name in dirs:
        dir_path = os.path.join(root, dir_name)
        if dir_path not in sys.path:
            sys.path.insert(0, dir_path)

print("=== Test d'import de application.py ===")
print(f"PYTHONPATH: {sys.path[:3]}...")  # Afficher les 3 premiers éléments

try:
    print("1. Test d'import de application.py...")
    from application import app
    print("✅ SUCCESS: application.py importé avec succès")
    
    print("2. Test de création de l'application...")
    print(f"   Type de l'app: {type(app)}")
    print(f"   Nom de l'app: {app.name}")
    print(f"   Debug mode: {app.config.get('DEBUG', 'Non défini')}")
    
    print("3. Test des blueprints enregistrés...")
    blueprints = list(app.blueprints.keys())
    print(f"   Blueprints trouvés: {blueprints}")
    
    print("4. Test des routes disponibles...")
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append(f"{rule.endpoint}: {rule.rule}")
    
    print(f"   Nombre total de routes: {len(routes)}")
    print("   Premières routes:")
    for route in routes[:10]:
        print(f"     {route}")
    
    print("\n✅ TOUS LES TESTS PASSÉS - application.py fonctionne correctement!")
    
except ImportError as e:
    print(f"❌ ERREUR D'IMPORT: {e}")
    print(f"   Fichier essayé: application.py")
    print(f"   Répertoire courant: {os.getcwd()}")
    print(f"   Fichiers présents: {[f for f in os.listdir('.') if f.endswith('.py')]}")
    
except Exception as e:
    print(f"❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()

print("\n=== Test terminé ===") 