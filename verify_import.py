import importlib
import sys

# Ensure the project directory is on sys.path (when run from elsewhere)
# (not strictly necessary when running from project dir)
sys.path.insert(0, r"d:\\Syntecx_hub projects\\number_guessing_game")

mod = importlib.import_module('game')
print('OK', hasattr(mod, 'NumberGuessingGame'))
