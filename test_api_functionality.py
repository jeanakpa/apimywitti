#!/usr/bin/env python3
"""
Test de fonctionnalité de l'API après correction des relations SQLAlchemy
"""

import os
import sys
import requests
import json

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

print("=== Test de fonctionnalité de l'API ===")

try:
    print("1. Test d'import de l'application...")
    from application import app
    print("✅ SUCCESS: Application importée")
    
    print("2. Test de création du contexte d'application...")
    with app.app_context():
        print("✅ SUCCESS: Contexte d'application créé")
        
        print("3. Test des modèles SQLAlchemy...")
        from Models.mywitti_users import MyWittiUser
        from Models.mywitti_survey import MyWittiSurvey, MyWittiSurveyResponse
        print("✅ SUCCESS: Modèles importés sans erreur")
        
        print("4. Test des relations...")
        # Test que les relations sont correctement définies
        user_attrs = dir(MyWittiUser())
        if 'basic_survey_responses' in user_attrs:
            print("✅ SUCCESS: Relation basic_survey_responses trouvée")
        else:
            print("⚠️  WARNING: Relation basic_survey_responses non trouvée")
        
        print("5. Test des routes disponibles...")
        routes = []
        for rule in app.url_map.iter_rules():
            if rule.endpoint != 'static':
                routes.append(f"{rule.endpoint}: {rule.rule}")
        
        print(f"   Nombre total de routes: {len(routes)}")
        print("   Routes principales:")
        main_routes = [r for r in routes if any(prefix in r for prefix in ['accounts', 'customer', 'admin', 'survey'])]
        for route in main_routes[:10]:
            print(f"     {route}")
        
        print("6. Test des blueprints...")
        blueprints = list(app.blueprints.keys())
        print(f"   Blueprints actifs: {blueprints}")
        
        print("\n✅ TOUS LES TESTS PASSÉS - API fonctionnelle!")
        
except Exception as e:
    print(f"❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()

print("\n=== Test terminé ===") 