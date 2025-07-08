#!/usr/bin/env python3
"""
Test de démarrage de Gunicorn avec wsgi.py
"""

import os
import sys
import subprocess
import time

# Définir les variables d'environnement nécessaires
os.environ['SECRET_KEY'] = 'test_secret_key'
os.environ['JWT_SECRET_KEY'] = 'test_jwt_key'
os.environ['DATABASE_URL'] = 'sqlite:///test.db'

print("=== Test de démarrage de Gunicorn avec wsgi.py ===")

try:
    print("1. Test d'import de wsgi.py...")
    import wsgi
    print("✅ SUCCESS: wsgi.py importé")
    
    print("2. Test de l'application dans wsgi...")
    print(f"   Type: {type(wsgi.app)}")
    print(f"   Nom: {wsgi.app.name}")
    
    print("3. Test de démarrage de Gunicorn...")
    print("   Commande: gunicorn wsgi:app --bind 0.0.0.0:8000 --workers 1 --timeout 30")
    
    # Démarrer Gunicorn en arrière-plan
    process = subprocess.Popen([
        'gunicorn', 'wsgi:app', 
        '--bind', '0.0.0.0:8000', 
        '--workers', '1', 
        '--timeout', '30',
        '--log-level', 'info'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    print("   Gunicorn démarré avec PID:", process.pid)
    
    # Attendre un peu pour voir s'il démarre correctement
    time.sleep(3)
    
    # Vérifier si le processus est toujours en vie
    if process.poll() is None:
        print("✅ SUCCESS: Gunicorn fonctionne correctement")
        
        # Arrêter le processus
        process.terminate()
        process.wait()
        print("   Gunicorn arrêté proprement")
    else:
        stdout, stderr = process.communicate()
        print("❌ ERREUR: Gunicorn s'est arrêté")
        print("   STDOUT:", stdout.decode())
        print("   STDERR:", stderr.decode())
    
    print("\n✅ TOUS LES TESTS PASSÉS!")
    
except Exception as e:
    print(f"❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()

print("=== Test terminé ===") 