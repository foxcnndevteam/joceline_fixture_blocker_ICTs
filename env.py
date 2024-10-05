import os
import sys

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(os.path.abspath(sys.executable))
elif __file__:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))