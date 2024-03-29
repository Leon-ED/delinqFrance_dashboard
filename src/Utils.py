"""
Module Utils.py
----------
Gère les fonctions et les classes utilitaires.

Auteur
---------
Léon E.

Classes
---------
- Colors
    Différentes couleurs pour les messages dans la console
"""


class Colors:
    """
    Différentes couleurs pour les messages dans la console

    Auteur
    ----------
    https://stackoverflow.com/a/287944
    
    Licence
    ----------
    CC BY-SA 4.0 DEED
    https://creativecommons.org/licenses/by-sa/4.0/
        
    Champs
    -------
    HEADER, 
    OKBLUE, 
    OKCYAN, 
    OKGREEN, 
    WARNING,
    FAIL, 
    ENDC, 
    BOLD, 
    UNDERLINE
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
