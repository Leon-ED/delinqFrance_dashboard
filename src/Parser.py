"""
Module Parser.py
----------
Parse les données téléchargées

Auteur
---------
Léon E.

Fonctions
---------
- parse_datas(to_csv=False)
    Parse le fichier récupéré sur data.gouv.fr et le sauvegarde dans un fichier CSV si to_csv est True.
"""


import pandas as pd
import os
import get_data
from alive_progress import alive_bar


# Constantes
DATA_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/../data/'
EXPORT_PATH = DATA_FOLDER + 'output.csv'

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
    xls =  get_data.get_main_data()
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
            # Parcourir les lignes du DataFrame
            for index, row in df.iterrows():
                # Extraire le mois et l'année à partir des noms de colonnes

                for col_name in df.columns[2:]:
                    _,annee, mois = col_name.split('_') # Le mois et l'année sont sous forme '_mois_annee'
                    fait = row['libellé index']
                    nombre = row[col_name]
                    datas.append([num_departement, mois, annee, fait, nombre,1_000])
            


    # Champ pour notre DataFrame final
    output_data = pd.DataFrame(datas, columns=['num_departement', 'mois', 'annee', 'fait', 'nombre','population'])

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
    parse_excel(to_csv=True)
    print("Fin du programme")