import pandas as pd
import requests
import os
from Model.OutputCSV import OutputCSV

FILE_NAME = 'tableaux-4001-ts.xlsx'
FILE_PATH = os.path.dirname(os.path.abspath(__file__)) + '/../data/' + FILE_NAME
DATA_URL = 'https://www.data.gouv.fr/fr/datasets/r/fdf5afbf-ed3c-4c54-a4f0-3581c8a1eca4'


def get_data() -> bool:
    '''Télécharge le fichier excel et le sauvegarde dans le dossier data'''

    r = requests.get(DATA_URL)
    if r.status_code != 200:
        raise Exception(f'La requête pour télécharger le fichier a échoué \n Code erreur: {r.status_code}')

    with open(FILE_PATH, 'wb') as f:
        f.write(r.content)
    if os.path.isfile(FILE_PATH):
        print(f'Le fichier {FILE_NAME} a été téléchargé avec succès, le chemin est: \n {FILE_PATH}')
        return True
    
    raise Exception('Une erreur a eu lieu et le fichier n\'a pas été téléchargé')



def parse_excel_sheets():
    df = pd.read_excel(FILE_PATH, sheet_name=None)
    output_csv = OutputCSV()

    for sheet_name, sheet_df in df.items():
        output_csv.addDepartement(sheet_df, sheet_name, sheet_df.columns)

parse_excel_sheets()