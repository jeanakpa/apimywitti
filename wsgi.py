#!/usr/bin/env python3
"""
WSGI entry point for Render deployment
"""

import os
import sys

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import the Flask app - exactement comme dans app.py
from app import app

# Cette variable 'app' est exactement la même que celle créée dans app.py
# Elle contient toute la configuration, les blueprints, les routes, etc.

if __name__ == "__main__":
    # Pour le développement local
    app.run(debug=app.config.get('DEBUG', False)) 