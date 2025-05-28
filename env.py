import os
import sys

# ~ Alternate between frozen (.exe) or script (.py) to get program main path.
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(os.path.abspath(sys.executable))
elif __file__:
    BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

VERSION_PROGRAM="2.62.0"
