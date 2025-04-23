import sys
import os

from env import BASE_DIR

def get_asset(relative_path):
    """Obtiene el path absoluto, para PyInstaller o modo desarrollo"""
    
    if getattr(sys, 'frozen', False):
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    elif __file__:
        base_path = os.path.join(BASE_DIR, "assets")
    
    return os.path.join(base_path, relative_path)
