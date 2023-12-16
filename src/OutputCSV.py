import pandas as pd
import os


# Constantes
DATA_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/../data/'
IMPORT_FILE = DATA_FOLDER + 'tableaux-4001-ts.xlsx'
EXPORT_PATH = DATA_FOLDER + 'output.csv'
xls = pd.ExcelFile(IMPORT_FILE)

data_final = []

# Pour chaque feuille ... 
for sheet_name in xls.sheet_names:
    df = pd.read_excel(IMPORT_FILE, sheet_name)

    # On récupère le numéro du département et on garde aussi la France entière
    # pour permettre de consulter les données au niveau national sans avoir à les calculer nous-même

    # Pour l'instant on veut seulement des données par département
    if(sheet_name == 'France_Métro' or sheet_name == 'France_Entière'):
        continue
    
    num_departement = sheet_name

    # Parcourir les lignes du DataFrame
    for index, row in df.iterrows():
        # Extraire le mois et l'année à partir des noms de colonnes
        for col_name in df.columns[2:]:
            _,annee, mois = col_name.split('_') # Le mois et l'année sont sous forme '_mois_annee'
            fait = row['libellé index']
            nombre = row[col_name]
            data_final.append([num_departement, mois, annee, fait, nombre,1_000])

# Champ pour notre DataFrame final
output_data = pd.DataFrame(data_final, columns=['num_departement', 'mois', 'annee', 'fait', 'nombre','population'])

# Sauvegarder le DataFrame dans un fichier CSV
output_data.to_csv(EXPORT_PATH, index=False,sep=";")

print(f"Le fichier CSV a été créé avec succès : {EXPORT_PATH}")