"""
Module get_data.py
----------
Gère la récupération des données depuis le site data.gouv.fr

Auteur
---------
Léon E.

Fonctions
---------
- get_data() -> bool
    Télécharge le fichier excel principal et le sauvegarde dans le dossier data.

- get_data2() -> bool
    Télécharge le fichier excel secondaire et le sauvegarde dans le dossier data.
"""


import pandas as pd
import requests
import os
from Parser import parse_excel
FILE_NAME = 'tableaux-4001-ts.xlsx'
FILE_PATH = os.path.dirname(os.path.abspath(__file__)) + '/../data/' + FILE_NAME
DATA_URL = 'https://www.data.gouv.fr/fr/datasets/r/fdf5afbf-ed3c-4c54-a4f0-3581c8a1eca4'
DATA_URL2 = 'https://www.data.gouv.fr/fr/datasets/r/acc332f6-92be-42af-9721-f3609bea8cfc'



def get_data() -> bool:
    """
    get_data() -> bool
    -----
    Télécharge le fichier excel et le sauvegarde dans le dossier data
    
    Returns
    -----
        - True: si le fichier a été téléchargé avec succès.
        
    Raises
    -----
        - IOError: si le fichier n'a pas été téléchargé.
    """

    r = requests.get(DATA_URL)
    if r.status_code != 200:
        raise Exception(f'La requête pour télécharger le fichier a échoué \n Code erreur: {r.status_code}')

    with open(FILE_PATH, 'wb') as f:
        f.write(r.content)
    if os.path.isfile(FILE_PATH):
        print(f'Le fichier {FILE_NAME} a été téléchargé avec succès, le chemin est: \n {FILE_PATH}')
        return True
    
    raise IOError('Une erreur a eu lieu et le fichier n\'a pas été téléchargé')


# def get_data2() -> bool:
#     '''Télécharge le fichier excel et le sauvegarde dans le dossier data'''

#     r = requests.get(DATA_URL2)
#     if r.status_code != 200:
#         raise Exception(f'La requête pour télécharger le fichier a échoué \n Code erreur: {r.status_code}')

#     with open(FILE_PATH, 'wb') as f:
#         f.write(r.content)
#     if os.path.isfile(FILE_PATH):
#         print(f'Le fichier {FILE_NAME} a été téléchargé avec succès, le chemin est: \n {FILE_PATH}')
#         return True
    
#     raise Exception('Une erreur a eu lieu et le fichier n\'a pas été téléchargé')

def get_global_dataframe():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    types = {'num_departement': str, 'mois': str, 'annee': str, 'fait': str, 'nombre': int}
    
    # check if file exists
    if not os.path.isfile(current_dir + '/../data/output.csv'):
        get_data()
        parse_excel(to_csv=True)
    
    df = pd.read_csv(current_dir + '/../data/output.csv', sep=';', dtype=types)
    return df


if __name__ == '__main__':
    get_data()
    # get_data2()
    print("Fin du programme")