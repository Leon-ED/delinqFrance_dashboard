"""
Module main.py
-------------------
Contient le script principal pour le tableau de bord interactif des crimes et délits en France entre 1996 et le premier trimestre 2022.

Auteur
------
Léon E.

Imports
-------
- Utils
- dash.dependencies (Input, Output)
- dash
- dash.dcc
- dash.html
- datetime.datetime
- Graphs.Carte
- get_data
- Graphs.CamembertFaits
- Graphs.HistogrammeParMois
- numpy
- Graphs.DelitsCrimesParAnnees

Fonctions
---------
- layout(annees, mois, departements, faits, default_annee, default_mois, default_departement, default_fait)
    Initialise le layout du tableau de bord avec les paramètres spécifiés.

- main()
    Fonction principale pour exécuter le tableau de bord.

Callback Functions
------------------
- update_map_graph(year, month, fait, display)
    Met à jour le graphique de la carte de la France et de l'Île-de-France en fonction des paramètres sélectionnés.

- update_most_common_crimes_pie_graph(month, year, departement, tri, limit)
    Met à jour le graphique du camembert des faits les plus/moins communs en fonction des paramètres sélectionnés.

- update_histogramme_par_mois_graph(year, departements, fait)
    Met à jour le graphique de l'histogramme par mois en fonction des paramètres sélectionnés.

- update_delits_crimes_par_annees_graph(fait, departement)
    Met à jour le graphique des délits et crimes par années en fonction des paramètres sélectionnés.
"""

# Imports locaux
import src.Utils as Utils
import src.Graphs.Carte as Carte
import get_data
import src.Graphs.CamembertFaits as CamembertFaits
import src.Graphs.HistogrammeParMois as HistogrammeParMois
import src.Graphs.DelitsCrimesParAnnees as DelitsCrimesParAnnees

# Imports standards
from datetime import datetime

# Imports tiers
try:
    from dash.dependencies import Input, Output
    import dash
    from dash import dcc
    from dash import html
    
    import numpy as np
except ModuleNotFoundError as e:
    print(f"{Utils.Colors.HEADER}L'erreur suivante est survenue lors de l'import des modules{Utils.Colors.ENDC}")
    print(f"{Utils.Colors.FAIL}{e}{Utils.Colors.ENDC}")
    print(f"{Utils.Colors.OKCYAN}Veuillez installer les modules requis en exécutant la commande suivante depuis le dossier racine du projet:{Utils.Colors.OKCYAN}")
    print(f"{Utils.Colors.OKGREEN}pip install -r requirements.txt{Utils.Colors.OKGREEN}")
    exit(1)



debug = True
time = datetime.now()
data = get_data.get_global_dataframe()
app = dash.Dash(__name__)


def layout(annees, mois, departements, faits, default_annee, default_mois, default_departement, default_fait):
    map_france,map_idf = Carte.get_map_graph(data, default_annee, default_departement,default_fait,-1)

    app.layout = html.Div(children=[
        # Header de la page
        html.Header(children=[
            html.H1(children='Dashboard des crimes et délits en France entre 1996 et le premier trimestre 2022'),
        ]),

        # Contenu principal (Main)
        html.Main(children=[
            # Section de la carte de la France
            html.Section(id="sec_map_france", children=[
                # Options de la carte de la France
                html.Div(id='sec_map_france_options', children=[
                    html.Label('Année'),
                    dcc.Dropdown(
                        id='map_year_dropdown',
                        options=[{'label': year, 'value': year} for year in annees if year != 'Tout'],
                        value='2022'
                    ),
                    html.Label('Mois'),
                    dcc.Dropdown(
                        id='map_month_dropdown',
                        options=[{'label': month, 'value': month} for month in mois],
                        value=default_mois
                    ),
                    html.Label('Fait'),
                    dcc.Dropdown(
                        id='map_fait_dropdown',
                        options=[{'label': fait, 'value': fait} for fait in faits],
                        value=default_mois
                    ),
                    html.Label('Affichage'),
                    dcc.Dropdown(
                        id='map_display_dropdown',
                        options=[{'label': 'Pour mille', 'value': 1_000},
                                {'label': 'Pour cent', 'value': 100},
                                {'label': 'Nombre', 'value': -1}],
                        value=-1
                    )
                ]),
                # Carte de la France et de l'Île-de-France
                html.Div(id='sec_map_france_content', style={'display': 'flex', 'justify-content': 'space-evenly'}, children=[
                    dcc.Loading(
                        id="map_france_loading",
                        type="circle",
                        children=[
                            dcc.Graph(
                                id='map_france',
                                figure=map_france
                            ),
                        ]
                    ),
                    dcc.Loading(
                        id="map_idf_loading",
                        type="circle",
                        children=[
                            dcc.Graph(
                                id='map_idf',
                                figure=map_idf
                            ),
                        ]
                    ),
                ])
            ]),

            # Camembert des faits les plus/moins communs
            html.Section(id='sec_faits_les_plus_communs', children=[
                # Options du camembert des faits les plus/moins communs
                html.Div(id='most_common_crimes_options', children=[
                    html.Label('Mois'),
                    dcc.Dropdown(
                        id='mcc-month-dropdown',
                        options=[{'label': month, 'value': month} for month in mois],
                        value=default_mois
                    ),
                    html.Label('Année'),
                    dcc.Dropdown(
                        id='mcc-year-dropdown',
                        options=[{'label': year, 'value': year} for year in annees],
                        value=default_annee
                    ),
                    html.Label('Département'),
                    dcc.Dropdown(
                        id='mcc-departement-dropdown',
                        options=[{'label': departement, 'value': departement} for departement in departements],
                        value=default_departement
                    ),
                    html.Label('Tri'),
                    dcc.Dropdown(
                        id='mcc-tri-dropdown',
                        options=[{'label': 'Ascendant', 'value': 'Ascendant'},
                                {'label': 'Descendant', 'value': 'Descendant'}],
                        value='Descendant'
                    ),
                    html.Label('Limite'),
                    dcc.Dropdown(
                        id='mcc-limit-dropdown',
                        options=[{'label': nbr, 'value': nbr} for nbr in range(5, 20, 5)],
                        value=5
                    )
                ]),
                # Camembert des faits les plus/moins communs
                html.Div(id='sec_faits_les_plus_communs_content', children=[
                    dcc.Loading(
                        id="most_common_crimes_loading",
                        type="circle",
                        children=[
                            dcc.Graph(
                                id='most_common_crimes',
                                figure=CamembertFaits.get_common_crimes_pie_graph(data, default_annee, default_mois,
                                                                                default_departement, ascending=False),
                            ),
                        ]
                    ),
                ]),
            ]),

            # Section de l'histogramme par mois
            html.Section(id='sec_histogramme_par_mois', children=[
                # Options de l'histogramme par mois
                html.Div(id='histogramme_par_mois_options', children=[
                    html.Label('Année'),
                    dcc.Dropdown(
                        id='hpm-year-dropdown',
                        options=[{'label': year, 'value': year} for year in annees],
                        value=default_annee
                    ),
                    html.Label('Département (plusieurs choix possibles)'),
                    dcc.Dropdown(
                        id='hpm-departement-dropdown',
                        options=[{'label': departement, 'value': departement} for departement in departements],
                        value='93',
                        multi=True
                    ),
                    html.Label('Fait'),
                    dcc.Dropdown(
                        id='hpm-fait-dropdown',
                        options=[{'label': fait, 'value': fait} for fait in faits],
                        value=default_fait
                    )
                ]),
                # Histogramme par mois
                html.Div(id='sec_histogramme_par_mois_content', children=[
                    dcc.Loading(
                        id="histogramme_par_mois_loading",
                        type="circle",
                        children=[
                            dcc.Graph(
                                id='histogramme_par_mois',
                                figure=HistogrammeParMois.get_histogramme_graph(data, default_annee, default_departement,
                                                                                default_fait),
                            ),
                        ]
                    ),
                ]),
            ]),

            # Delits et crimes par années
            html.Section(id='sec_delits_crimes_par_annees', children=[
                # Options des délits et crimes par années
                html.Div(id='delits_crimes_par_annees_options', children=[
                    html.Label('Fait'),
                    dcc.Dropdown(
                        id='dcpa-fait-dropdown',
                        options=[{'label': fait, 'value': fait} for fait in faits],
                        value=default_fait
                    ),
                    html.Label('Département'),
                    dcc.Dropdown(
                        id='dcpa-departement-dropdown',
                        options=[{'label': departement, 'value': departement} for departement in departements],
                        value=default_departement
                    )
                ]),
                # Débits et crimes par années
                html.Div(id='sec_delits_crimes_par_annees_content', children=[
                    dcc.Loading(
                        id="delits_crimes_par_annees_loading",
                        type="circle",
                        children=[
                            dcc.Graph(
                                id='delits_crimes_par_annees',
                                figure=DelitsCrimesParAnnees.get_delits_crimes_annees_graph(data, default_fait,
                                                                                            default_departement),
                            ),
                        ]
                    ),
                ]),
            ]),
        ])
    ])



   
def main():
    debug and print("Lancement du main")

    debug and print("Données récupérées en " + str(datetime.now() - time))
    
    # Paramètres par défaut des dropdowns
    default_annee = 'Tout'
    default_departement = 'Tout'
    default_mois = 'Tout'
    default_fait = 'Tout'


    departements = np.append(data['num_departement'].unique(), default_departement)
    annees = np.append(data['annee'].unique(), default_annee)
    mois = np.append(data['mois'].unique(), default_mois)
    faits = np.append(data['fait'].unique(), 'Tout')
    departements.sort()
    annees.sort()
    mois.sort()
    

    layout(annees, mois, departements, faits, default_annee, default_mois, default_departement, default_fait)


    
    app.run_server(host="0.0.0.0", port=8050, debug=False)





@app.callback(
    Output('map_france', 'figure'),
    Output('map_idf', 'figure'),
    Input('map_year_dropdown', 'value'),
    Input('map_month_dropdown', 'value'),
    Input('map_fait_dropdown', 'value'),
    Input('map_display_dropdown', 'value'))
def update_map_graph(year, month,fait,display):


    return Carte.get_map_graph(data, year, month,fait,display)


@app.callback(
    Output('most_common_crimes', 'figure'),
    Input('mcc-month-dropdown', 'value'),
    Input('mcc-year-dropdown', 'value'),
    Input('mcc-departement-dropdown', 'value'),
    Input('mcc-tri-dropdown', 'value'),
    Input('mcc-limit-dropdown', 'value'))
def update_most_common_crimes_pie_graph(month, year, departement, tri, limit):
    return CamembertFaits.get_common_crimes_pie_graph(data, year, month, departement, ascending= (tri == 'Ascendant'),limit=limit)



@app.callback(
    Output('histogramme_par_mois', 'figure'),
    Input('hpm-year-dropdown', 'value'),
    Input('hpm-departement-dropdown', 'value'),
    Input('hpm-fait-dropdown', 'value'))
def update_histogramme_par_mois_graph(year, departements, fait):
    if(departements == [] or departements == ['Tout'] or departements == 'Tout'):
        departements = 'Tout'
    elif(type(departements) == str):
        departements = [departements]
    return HistogrammeParMois.get_histogramme_graph(data, year, departements, fait)


@app.callback(
    Output('delits_crimes_par_annees', 'figure'),
    Input('dcpa-fait-dropdown', 'value'),
    Input('dcpa-departement-dropdown', 'value'))
def update_delits_crimes_par_annees_graph(fait, departement):
    return DelitsCrimesParAnnees.get_delits_crimes_annees_graph(data, fait, departement)




if __name__ == '__main__':
    main()
