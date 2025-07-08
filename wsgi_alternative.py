#!/usr/bin/env python3
"""
WSGI entry point for Render deployment - Version alternative
"""

import os
import sys

# Configuration du chemin Python
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Ajouter tous les sous-répertoires au PYTHONPATH
for item in os.listdir(current_dir):
    item_path = os.path.join(current_dir, item)
    if os.path.isdir(item_path) and not item.startswith('.'):
        if item_path not in sys.path:
            sys.path.insert(0, item_path)

# Configuration des variables d'environnement par défaut si non définies
if 'SECRET_KEY' not in os.environ:
    os.environ['SECRET_KEY'] = 'default-secret-key-for-development'
if 'JWT_SECRET_KEY' not in os.environ:
    os.environ['JWT_SECRET_KEY'] = 'default-jwt-secret-key-for-development'
if 'DATABASE_URL' not in os.environ:
    os.environ['DATABASE_URL'] = 'sqlite:///app.db'
if 'FLASK_ENV' not in os.environ:
    os.environ['FLASK_ENV'] = 'development'

try:
    # Import de l'application Flask
    from app import app
    print("✅ Application Flask importée avec succès")
    
    # Vérification des blueprints
    blueprints = list(app.blueprints.keys())
    print(f"📋 Blueprints chargés: {blueprints}")
    
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
    print(f"📁 Répertoire courant: {current_dir}")
    print(f"📁 PYTHONPATH: {sys.path}")
    raise
except Exception as e:
    print(f"❌ Erreur inattendue: {e}")
    raise

if __name__ == "__main__":
    # Pour le développement local
    app.run(debug=app.config.get('DEBUG', False)) 