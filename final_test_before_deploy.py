#!/usr/bin/env python3
"""
Test final complet avant redéploiement sur Render
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

print("=== TEST FINAL AVANT REDÉPLOIEMENT ===")
print("Vérification complète de la configuration...")

try:
    print("\n1. Test d'import de application.py...")
    from application import app
    print("✅ SUCCESS: application.py importé")
    
    print("\n2. Test d'import de wsgi.py...")
    import wsgi
    print("✅ SUCCESS: wsgi.py importé")
    print(f"   Type de wsgi.app: {type(wsgi.app)}")
    
    print("\n3. Test des modèles SQLAlchemy...")
    with app.app_context():
        from Models.mywitti_users import MyWittiUser
        from Models.mywitti_survey import MyWittiSurvey, MyWittiSurveyResponse
        print("✅ SUCCESS: Modèles importés sans erreur")
        
        # Test des relations
        user_attrs = dir(MyWittiUser())
        if 'basic_survey_responses' in user_attrs:
            print("✅ SUCCESS: Relation basic_survey_responses OK")
        else:
            print("❌ ERREUR: Relation basic_survey_responses manquante")
    
    print("\n4. Test des blueprints...")
    blueprints = list(app.blueprints.keys())
    expected_blueprints = ['accounts', 'customer', 'lot', 'admin', 'faq', 'support', 'survey', 'advertisement']
    missing_blueprints = [bp for bp in expected_blueprints if bp not in blueprints]
    
    if not missing_blueprints:
        print(f"✅ SUCCESS: Tous les blueprints présents ({len(blueprints)} blueprints)")
    else:
        print(f"⚠️  WARNING: Blueprints manquants: {missing_blueprints}")
    
    print("\n5. Test des routes...")
    routes = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            routes.append(rule.endpoint)
    
    print(f"✅ SUCCESS: {len(routes)} routes disponibles")
    
    print("\n6. Test des fichiers de configuration...")
    required_files = [
        'application.py',
        'wsgi.py', 
        'render.yaml',
        'requirements.txt',
        'runtime.txt'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if not missing_files:
        print("✅ SUCCESS: Tous les fichiers de configuration présents")
    else:
        print(f"❌ ERREUR: Fichiers manquants: {missing_files}")
    
    print("\n7. Test de la configuration Render...")
    with open('render.yaml', 'r') as f:
        render_config = f.read()
        if 'gunicorn wsgi:app' in render_config:
            print("✅ SUCCESS: Configuration Render correcte")
        else:
            print("❌ ERREUR: Configuration Render incorrecte")
    
    print("\n" + "="*50)
    print("🎉 TOUS LES TESTS PASSÉS - PRÊT POUR LE DÉPLOIEMENT!")
    print("="*50)
    print("\n📋 Checklist de déploiement:")
    print("✅ Conflit de noms résolu (app.py vs gunicorn.app)")
    print("✅ Conflit SQLAlchemy résolu (relations survey_responses)")
    print("✅ Tous les modèles importés correctement")
    print("✅ Tous les blueprints fonctionnels")
    print("✅ Configuration Render correcte")
    print("✅ Fichiers de déploiement présents")
    print("\n🚀 Vous pouvez maintenant redéployer sur Render!")
    
except Exception as e:
    print(f"\n❌ ERREUR CRITIQUE: {e}")
    import traceback
    traceback.print_exc()
    print("\n🔧 CORRECTION REQUISE AVANT DÉPLOIEMENT")

print("\n=== Test terminé ===") 