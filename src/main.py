try:
    from dash.dependencies import Input, Output
    import dash
    from dash import dcc
    from dash import html
    from datetime import datetime
    import Graphs.Carte as Carte
    import get_data
    import Graphs.CamembertFaits as CamembertFaits
    import Graphs.HistogrammeParMois as HistogrammeParMois
    import numpy as np
except Exception as e:
    print("Erreur lors de l'importation des modules : " + str(e))
    print("Veuillez installer les modules requis en exécutant la commande suivante dans le dossier racine du projet:")
    print("pip install -r requirements.txt")
    exit(1)



debug = True
time = datetime.now()
data = get_data.get_global_dataframe()
app = dash.Dash(__name__)


def layout(annees, mois, departements, faits, default_annee, default_mois, default_departement, default_fait):
    app.layout = html.Main(children=[
        html.H1(children='Delinquance en France', className='center'),
        
        # Carte de la France
        html.Div(id="div_map_france",children=[
        
        dcc.Dropdown(
            id='map_year_dropdown',
            options=[{'label': year, 'value': year} for year in annees],
            value=default_annee
        ),
        dcc.Dropdown(
            id='map_month_dropdown',
            options=[{'label': month, 'value': month} for month in mois],
            value=default_mois
        ),
        dcc.Graph(
            id='map_france',
            figure=Carte.get_map_graph(data, default_annee, default_departement),
        )
        ]),
        # Camembert des faits les plus communs
        html.Div(id='div_faits_les_plus_communs', children=[
            html.Div(id='most_common_crimes_options', children=[
                dcc.Dropdown(
                    id='mcc-month-dropdown',
                    options=[{'label': month, 'value': month} for month in mois],
                    value=default_mois
                ),
                dcc.Dropdown(
                    id='mcc-year-dropdown',
                    options=[{'label': year, 'value': year} for year in annees],
                    value=default_annee
                ),
                dcc.Dropdown(
                    id='mcc-departement-dropdown',
                    options=[{'label': departement, 'value': departement} for departement in departements],
                    value=default_departement
                )
            ])
            ,
            dcc.Graph(
                id='most_common_crimes',
                figure=CamembertFaits.get_common_crimes_pie_graph(data, default_annee, default_mois, default_departement, ascending=False),
            )]),
            html.Div(id='div_faits_les_moins_communs', children=[
                html.Div(id='least_common_crimes_options', children=[
                    dcc.Dropdown(
                        id='lcc-month-dropdown',
                        options=[{'label': month, 'value': month} for month in mois],
                        value=default_mois
                    ),
                    dcc.Dropdown(
                        id='lcc-year-dropdown',
                        options=[{'label': year, 'value': year} for year in annees],
                        value=default_annee
                    ),
                    dcc.Dropdown(
                        id='lcc-departement-dropdown',
                        options=[{'label': departement, 'value': departement} for departement in departements],
                        value=default_departement
                    )
            ]),
            dcc.Graph(
                id='least_common_crimes',
                figure=CamembertFaits.get_common_crimes_pie_graph(data, default_annee, default_mois, default_departement, ascending=True),
            )]),
            html.Div(id='div_histogramme_par_mois', children=[
                html.Div(id='histogramme_par_mois_options', children=[
                    dcc.Dropdown(
                        id='hpm-year-dropdown',
                        options=[{'label': year, 'value': year} for year in annees],
                        value=default_annee
                    ),
                    dcc.Dropdown(
                        id='hpm-departement-dropdown',
                        options=[{'label': departement, 'value': departement} for departement in departements],
                        value=default_departement,
                        multi=True
                    ),
                    
                    dcc.Dropdown(
                        id='hpm-fait-dropdown',
                        options=[{'label': fait, 'value': fait} for fait in faits],
                        value=default_fait
                    )
                ]),
                dcc.Graph(
                    id='histogramme_par_mois',
                    figure=HistogrammeParMois.get_histogramme_graph(data, default_annee, default_departement, 'Tout'),
                )
            ]),
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


    
    app.run_server(debug=True)

@app.callback(
    Output('map_france', 'figure'),
    Input('map_year_dropdown', 'value'),
    Input('map_month_dropdown', 'value'))
def update_map_graph(year, month):
    return Carte.get_map_graph(data, year, month)


@app.callback(
    Output('most_common_crimes', 'figure'),
    Input('mcc-month-dropdown', 'value'),
    Input('mcc-year-dropdown', 'value'),
    Input('mcc-departement-dropdown', 'value'))
def update_most_common_crimes_pie_graph(month, year, departement):
    return CamembertFaits.get_common_crimes_pie_graph(data, year, month, departement, ascending=False)

@app.callback(
    Output('least_common_crimes', 'figure'),
    Input('lcc-month-dropdown', 'value'),
    Input('lcc-year-dropdown', 'value'),
    Input('lcc-departement-dropdown', 'value'))
def update_least_common_crimes_pie_graph(month, year, departement):
    return CamembertFaits.get_common_crimes_pie_graph(data, year, month, departement, ascending=True)




@app.callback(
    Output('histogramme_par_mois', 'figure'),
    Input('hpm-year-dropdown', 'value'),
    Input('hpm-departement-dropdown', 'value'),
    Input('hpm-fait-dropdown', 'value'))
def update_histogramme_par_mois_graph(year, departements, fait):
    if(departements == [] or departements == ['Tout']):
        departements = 'Tout'  
    return HistogrammeParMois.get_histogramme_graph(data, year, departements, fait)


if __name__ == '__main__':
    main()
