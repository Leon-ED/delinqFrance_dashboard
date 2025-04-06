"""
Module get_data.py
----------
Gère la récupération des données depuis le site data.gouv.fr

Auteur
---------
Léon E.

Fonctions
---------
- get_main_data() -> DataFrame
    Télécharge le fichier excel et le retourne sous forme de DataFrame.

- get_data_population() -> bool
    Télécharge le fichier excel de la population 

- parse_datas(to_csv=False)
    Parse le fichier récupéré sur data.gouv.fr et le sauvegarde dans un fichier CSV si to_csv est True.

- get_global_dataframe()
    Retourne le DataFrame global contenant les données de tous les départements.
"""


import pandas as pd
import requests
import os
from alive_progress import alive_bar

# Constantes
DATA_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

DATA_URL = 'https://www.data.gouv.fr/fr/datasets/r/fdf5afbf-ed3c-4c54-a4f0-3581c8a1eca4'
"""
 Url du fichier principal (Délits et crimes constatés par les services de police et de gendarmerie, par département (France entière))
"""

DATA_URL2 = 'https://www.insee.fr/fr/statistiques/fichier/7739582/ensemble.xlsx'
"""
    Url du fichier secondaire (Population par département)
"""
EXPORT_PATH = DATA_FOLDER + 'output.csv'



import io

def get_main_data() -> pd.DataFrame:
    """
    get_main_data() -> DataFrame
    -----
    Télécharge le fichier principal et le retourne sous forme de DataFrame.
    Returns
    -----
        - DataFrame: le fichier principal sous forme de DataFrame.
        
    Raises
    -----
        - IOError: si le fichier n'a pas été téléchargé.
    """

    print('Obtention du fichier principal ...')
    r = requests.get(DATA_URL)
    if r.status_code != 200:
        raise Exception(f'La requête pour télécharger le fichier a échoué \n Code erreur: {r.status_code}')

    content_buffer = io.BytesIO(r.content)
    file = pd.ExcelFile(content_buffer)
    print('Le fichier principal a été obtenu avec succès')
    return file

def get_data_population() -> pd.DataFrame:
    """
    get_data_population() -> DataFrame
    -----
    Télécharge le fichier de la population et le retourne sous forme de DataFrame.
    Returns
    -----
        - DataFrame: le fichier de la population sous forme de DataFrame.
        
    Raises
    -----
        - IOError: si le fichier n'a pas été téléchargé.
    """
    print('Obtention du fichier de la population ...')
    r = requests.get(DATA_URL2)
    if r.status_code != 200:
        raise Exception(f'La requête pour télécharger le fichier a échoué \n Code erreur: {r.status_code}')

    content_buffer = io.BytesIO(r.content)
    file = pd.ExcelFile(content_buffer)
    print('Le fichier de la population a été obtenu avec succès')
    return pd.read_excel(file, 'Départements', skiprows=7, usecols='C,D,I', names=['Code département','Nom du département', 'Population totale'])

def get_global_dataframe() -> pd.DataFrame:
    """
    get_global_dataframe() -> DataFrame
    -----
    Retourne le DataFrame global contenant les données de tous les départements.
    Returns
    -----
        - DataFrame: le fichier principal sous forme de DataFrame.

    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    types = {'num_departement': str, 'mois': str, 'annee': str, 'fait': str, 'nombre': int, 'population': int, 'nom_departement': str}
    
    # check if file exists
    if not os.path.isfile(current_dir + '/data/output.csv'):
        print("Le fichier CSV n'existe pas, il va être créé...")
        parse_datas(to_csv=True)
    
    df = pd.read_csv(current_dir + '/data/output.csv', sep=';', dtype=types)

    return df

def parse_datas(to_csv=False):
    """
    parse_datas(to_csv=False)
    ------
    Parse le fichier récupéré sur data.gouv.fr
    Args:
    ------
    
        - to_csv (bool, optional):
            Si True, sauvegarde le fichier dans un fichier CSV. Sinon, retourne le DataFrame.
        
    Returns:
    ------
        - DataFrame si to_csv est False.
        - None si to_csv est True.
    """
    xls =  get_main_data()
    population_data = get_data_population()
    datas = []
    print("Début du traitement des données...")
    # Pour chaque feuille ... 
    with alive_bar(96) as bar:
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name)

            # On récupère le numéro du département et on garde aussi la France entière
            # pour permettre de consulter les données au niveau national sans avoir à les calculer nous-même

            # Pour l'instant on veut seulement des données par département métropolitains
            if(sheet_name == 'France_Métro' or sheet_name == 'France_Entière' or sheet_name > '95'):
                continue

            bar()    
            num_departement = sheet_name
            population = population_data[population_data['Code département'] == num_departement]['Population totale'].values[0]
            nom_departement = population_data[population_data['Code département'] == num_departement]['Nom du département'].values[0]

            for index, row in df.iterrows():
                # On extrait le mois et l'année à partir des noms de colonnes

                for col_name in df.columns[2:]:
                    _,annee, mois = col_name.split('_') # Le mois et l'année sont sous forme '_mois_annee'
                    fait = row['libellé index']
                    nombre = row[col_name]

                    datas.append([num_departement, mois, annee, fait, nombre, population, nom_departement])
            


    # Champ pour notre DataFrame final
    output_data = pd.DataFrame(datas, columns=['num_departement', 'mois', 'annee', 'fait', 'nombre','population','nom_departement'])

    if to_csv:
    # Sauvegarder le DataFrame dans un fichier CSV
        print("Sauvegarde du fichier CSV...")
        try:
            output_data.to_csv(EXPORT_PATH, index=False,sep=";")
            print(f"Le fichier CSV a été créé avec succès : {EXPORT_PATH}")    
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du fichier CSV : {e}")
            exit(1)
    
    return output_data

if __name__ == '__main__':
    parse_datas(to_csv=True)