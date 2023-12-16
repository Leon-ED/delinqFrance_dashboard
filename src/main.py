import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import os
import dash
from dash import dcc
from dash import html
from datetime import datetime
import Graphs.Map as Map
import get_data
import Graphs.MostCommonCrimes as MostCommonCrimes
import numpy as np


debug = True
time = datetime.now()
data = get_data.get_global_dataframe()
app = dash.Dash(__name__)


   
def main():
    debug and print("Lancement du main")

    debug and print("Données récupérées en " + str(datetime.now() - time))
    
    default_annee = 'Tout'
    default_departement = 'Tout'
    default_mois = 'Tout'
    
    departements = np.append(data['num_departement'].unique(), default_departement)
    annees = np.append(data['annee'].unique(), default_annee)
    mois = np.append(data['mois'].unique(), default_mois)

    departements.sort()
    annees.sort()
    mois.sort()
    

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
            figure=Map.get_map_graph(data, default_annee, default_departement),
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
                
            ]),
            dcc.Graph(
                id='most_common_crimes',
                figure=MostCommonCrimes.get_most_common_crimes_pie_graph(data, default_annee, default_mois, default_departement),
            )
        ])
        
    

    app.run_server(debug=True)

@app.callback(
    Output('map_france', 'figure'),
    Input('map_year_dropdown', 'value'),
    Input('map_month_dropdown', 'value'))
def update_map_graph(year, month):
    return Map.get_map_graph(data, year, month)


@app.callback(
    Output('most_common_crimes', 'figure'),
    Input('mcc-month-dropdown', 'value'),
    Input('mcc-year-dropdown', 'value'),
    Input('mcc-departement-dropdown', 'value'))
def update_most_common_crimes_pie_graph(month, year, departement):
    return MostCommonCrimes.get_most_common_crimes_pie_graph(data, year, month, departement)


if __name__ == '__main__':
    main()
