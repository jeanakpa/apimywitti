#!/usr/bin/env python3
"""
Script pour tester le déploiement Render spécifiquement
"""

import os
import sys
import subprocess

def test_render_environment():
    """Teste l'environnement comme sur Render"""
    print("🧪 Test de l'environnement Render...")
    
    # Variables d'environnement comme sur Render
    env_vars = {
        'SECRET_KEY': 'APZENPtcP_RAkxvWL9MNwQBIxOajuKqbNXdynEIXisw',
        'JWT_SECRET_KEY': '4AZvSj-VQzll1zsTxY9dLtLSMn2obqpxVjVrwQwWAPk',
        'DATABASE_URL': 'postgresql://witti_user:YjXncuy3GIeLiiFMov24m2H1yG4iI7j5@dpg-d1i6idbe5dus73a5l5s0-a.oregon-postgres.render.com/mywitti',
        'FLASK_ENV': 'production',
        'PYTHONPATH': os.getcwd()
    }
    
    # Mettre à jour l'environnement
    for key, value in env_vars.items():
        os.environ[key] = value
    
    print("✅ Variables d'environnement configurées")
    
    # Test 1: Import direct de wsgi.py
    print("\n🧪 Test 1: Import de wsgi.py...")
    try:
        from wsgi import app
        print("✅ wsgi.py importé avec succès")
        
        # Vérifier les blueprints
        blueprints = list(app.blueprints.keys())
        print(f"📋 Blueprints trouvés: {blueprints}")
        
        return True
    except Exception as e:
        print(f"❌ Erreur lors de l'import de wsgi.py: {e}")
        return False

def test_gunicorn_command():
    """Teste la commande Gunicorn exactement comme sur Render"""
    print("\n🧪 Test 2: Commande Gunicorn...")
    
    try:
        # Variables d'environnement
        env = os.environ.copy()
        env['SECRET_KEY'] = 'APZENPtcP_RAkxvWL9MNwQBIxOajuKqbNXdynEIXisw'
        env['JWT_SECRET_KEY'] = '4AZvSj-VQzll1zsTxY9dLtLSMn2obqpxVjVrwQwWAPk'
        env['DATABASE_URL'] = 'postgresql://witti_user:YjXncuy3GIeLiiFMov24m2H1yG4iI7j5@dpg-d1i6idbe5dus73a5l5s0-a.oregon-postgres.render.com/mywitti'
        env['FLASK_ENV'] = 'production'
        
        # Commande exacte de Render
        cmd = ['gunicorn', 'wsgi:app', '--bind', '0.0.0.0:8000', '--timeout', '120']
        
        print(f"🚀 Exécution: {' '.join(cmd)}")
        
        # Démarrer Gunicorn
        process = subprocess.Popen(
            cmd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Attendre un peu
        import time
        time.sleep(5)
        
        # Vérifier si le processus est en vie
        if process.poll() is None:
            print("✅ Gunicorn a démarré avec succès")
            process.terminate()
            process.wait()
            return True
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Gunicorn a échoué:")
            print(f"   STDOUT: {stdout}")
            print(f"   STDERR: {stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test Gunicorn: {e}")
        return False

def test_imports_manually():
    """Teste les imports manuellement"""
    print("\n🧪 Test 3: Imports manuels...")
    
    try:
        # Test des imports de base
        print("📦 Test des imports de base...")
        from flask import Flask
        print("✅ Flask importé")
        
        from extensions import db, ma, jwt, migrate
        print("✅ Extensions importées")
        
        # Test des modèles
        print("📦 Test des modèles...")
        from Models.mywitti_survey import MyWittiSurvey, MyWittiSurveyOption, MyWittiSurveyResponse
        print("✅ Modèles survey importés")
        
        from Models.mywitti_users import MyWittiUser
        print("✅ Modèle utilisateur importé")
        
        from Models.mywitti_client import MyWittiClient
        print("✅ Modèle client importé")
        
        from Models.mywitti_advertisement import MyWittiAdvertisement
        print("✅ Modèle publicité importé")
        
        # Test des blueprints
        print("📦 Test des blueprints...")
        from Account.views import accounts_bp
        print("✅ Blueprint Account importé")
        
        from Customer.views import customer_bp
        print("✅ Blueprint Customer importé")
        
        from Lot.views import lot_bp
        print("✅ Blueprint Lot importé")
        
        from Admin.views import admin_bp
        print("✅ Blueprint Admin importé")
        
        from Advertisement.views import advertisement_bp
        print("✅ Blueprint Advertisement importé")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 Test de déploiement Render")
    print("=" * 50)
    
    # Tests
    test1 = test_imports_manually()
    test2 = test_render_environment()
    test3 = test_gunicorn_command()
    
    print("\n" + "=" * 50)
    print("📊 Résultats:")
    print(f"   Imports manuels: {'✅' if test1 else '❌'}")
    print(f"   Environnement Render: {'✅' if test2 else '❌'}")
    print(f"   Commande Gunicorn: {'✅' if test3 else '❌'}")
    
    if test1 and test2 and test3:
        print("\n🎉 SUCCÈS: Tous les tests sont passés !")
        print("✅ L'application est prête pour le déploiement Render")
        return 0
    else:
        print("\n❌ ÉCHEC: Certains tests ont échoué")
        print("🔧 Vérifiez les erreurs ci-dessus")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 