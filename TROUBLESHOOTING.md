# Guide de Dépannage - Erreur ModuleNotFoundError

## 🚨 Problème : ModuleNotFoundError: No module named 'Models.mywitti_survey'

### 🔍 Diagnostic

Cette erreur indique que Python ne peut pas trouver le module `Models.mywitti_survey` lors du déploiement sur Render.

### 🛠️ Solutions

#### Solution 1: Vérification des fichiers __init__.py

Assurez-vous que tous les dossiers ont un fichier `__init__.py` :

```bash
# Vérifiez que ces fichiers existent :
Models/__init__.py
Account/__init__.py
Customer/__init__.py
Lot/__init__.py
Admin/__init__.py
Faq/__init__.py
Support/__init__.py
Survey/__init__.py
Advertisement/__init__.py
Resultat/__init__.py
Category/__init__.py
```

#### Solution 2: Test local avant déploiement

```bash
# Testez localement avec les mêmes variables d'environnement
export SECRET_KEY="APZENPtcP_RAkxvWL9MNwQBIxOajuKqbNXdynEIXisw"
export JWT_SECRET_KEY="4AZvSj-VQzll1zsTxY9dLtLSMn2obqpxVjVrwQwWAPk"
export DATABASE_URL="postgresql://witti_user:YjXncuy3GIeLiiFMov24m2H1yG4iI7j5@dpg-d1i6idbe5dus73a5l5s0-a.oregon-postgres.render.com/mywitti"
export FLASK_ENV="production"

# Testez l'import
python3 -c "from Models.mywitti_survey import MyWittiSurvey; print('OK')"

# Testez wsgi.py
python3 wsgi.py

# Testez Gunicorn
gunicorn wsgi:app --bind 0.0.0.0:8000 --timeout 120
```

#### Solution 3: Configuration Render

Dans votre service Render, configurez :

**Build Command :**
```bash
pip install -r requirements.txt
```

**Start Command :**
```bash
gunicorn wsgi:app --bind 0.0.0.0:$PORT --timeout 120
```

**Variables d'environnement :**
```
PYTHON_VERSION=3.13.0
FLASK_ENV=production
PYTHONPATH=.
SECRET_KEY=votre_secret_key
JWT_SECRET_KEY=votre_jwt_secret_key
DATABASE_URL=votre_database_url
```

#### Solution 4: Alternative - Utiliser app.py directement

Si le problème persiste, modifiez la commande de démarrage :

**Start Command :**
```bash
gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120
```

#### Solution 5: Vérification de la structure

Assurez-vous que votre structure de fichiers est correcte :

```
Witti_Witti/
├── app.py
├── wsgi.py
├── requirements.txt
├── runtime.txt
├── Models/
│   ├── __init__.py
│   ├── mywitti_survey.py
│   └── ...
├── Account/
│   ├── __init__.py
│   └── views.py
└── ...
```

### 🔧 Tests de diagnostic

#### Test 1: Vérification des imports
```bash
python3 test_render_deployment.py
```

#### Test 2: Test de l'environnement
```bash
python3 -c "
import sys
print('Python path:', sys.path)
import os
print('Current directory:', os.getcwd())
print('Files in current directory:', os.listdir('.'))
"
```

#### Test 3: Test des modèles
```bash
python3 -c "
import sys
sys.path.insert(0, '.')
try:
    from Models.mywitti_survey import MyWittiSurvey
    print('✅ Import réussi')
except Exception as e:
    print(f'❌ Erreur: {e}')
"
```

### 📋 Checklist de déploiement

- [ ] Tous les fichiers `__init__.py` sont présents
- [ ] Les variables d'environnement sont configurées sur Render
- [ ] Le test local fonctionne
- [ ] La commande Gunicorn fonctionne localement
- [ ] Le fichier `wsgi.py` importe correctement `app.py`

### 🆘 En cas d'échec persistant

1. **Vérifiez les logs Render** dans l'interface web
2. **Testez avec `app.py`** au lieu de `wsgi.py`
3. **Vérifiez la version Python** (3.13.0)
4. **Contactez le support** si le problème persiste

### 📞 Support

Si aucune solution ne fonctionne :
1. Vérifiez les logs complets sur Render
2. Testez localement avec `python3 test_render_deployment.py`
3. Partagez les erreurs exactes pour un diagnostic plus précis 