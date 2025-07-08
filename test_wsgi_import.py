#!/usr/bin/env python3
"""
Test d'import de wsgi.py
"""

import os
import sys

# Définir les variables d'environnement nécessaires
os.environ['SECRET_KEY'] = 'test_secret_key'
os.environ['JWT_SECRET_KEY'] = 'test_jwt_key'
os.environ['DATABASE_URL'] = 'sqlite:///test.db'

# Ajouter le répertoire courant au PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Ajouter tous les sous-répertoires au PYTHONPATH
for root, dirs, files in os.walk(current_dir):
    for dir_name in dirs:
        dir_path = os.path.join(root, dir_name)
        if dir_path not in sys.path:
            sys.path.insert(0, dir_path)

print("=== Test d'import de wsgi.py ===")

try:
    print("1. Import de wsgi.py...")
    import wsgi
    print("✅ SUCCESS: wsgi.py importé avec succès")
    
    print("2. Vérification de l'application dans wsgi...")
    print(f"   Type de wsgi.app: {type(wsgi.app)}")
    print(f"   Nom de l'app: {wsgi.app.name}")
    
    print("3. Test des blueprints...")
    blueprints = list(wsgi.app.blueprints.keys())
    print(f"   Blueprints: {blueprints}")
    
    print("4. Test des routes...")
    routes = []
    for rule in wsgi.app.url_map.iter_rules():
        routes.append(f"{rule.endpoint}: {rule.rule}")
    
    print(f"   Nombre total de routes: {len(routes)}")
    print("   Premières routes:")
    for route in routes[:5]:
        print(f"     {route}")
    
    print("\n✅ TOUS LES TESTS PASSÉS - wsgi.py fonctionne correctement!")
    
except Exception as e:
    print(f"❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()

print("=== Test terminé ===") 