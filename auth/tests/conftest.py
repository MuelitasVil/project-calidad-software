"""
Configuración de pytest para agregar el directorio raíz al PYTHONPATH
"""
import sys
import os

# Agregar el directorio raíz del proyecto (auth/) al PYTHONPATH
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
