import sys
import os

path = '/home/yourusername/stormy-assistant-2'
if path not in sys.path:
    sys.path.append(path)

from web.app import app as application
