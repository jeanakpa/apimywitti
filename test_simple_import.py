#!/usr/bin/env python3
"""
Test simple d'import de application.py
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

print("=== Test simple d'import de application.py ===")

try:
    print("1. Import de application.py...")
    from application import app
    print("✅ SUCCESS: application.py importé avec succès")
    
    print("2. Vérification de l'application...")
    print(f"   Type: {type(app)}")
    print(f"   Nom: {app.name}")
    
    print("3. Test des blueprints...")
    blueprints = list(app.blueprints.keys())
    print(f"   Blueprints: {blueprints}")
    
    print("\n✅ TOUS LES TESTS PASSÉS!")
    
except Exception as e:
    print(f"❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()

print("=== Test terminé ===") 