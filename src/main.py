# filename = 'main.py'

#
# Imports
#
import os
import plotly_express as px
import dash
from dash import dcc
from dash import html
import pandas as pd
from dash.dependencies import Input, Output

#
# Data
#
current_dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(current_dir + '/../data/donnee-dep-data.gouv-2022-geographie2023-produit-le2023-07-17 2.csv', sep=';')

years = df['annee'].unique()
departements = df['Code.département'].unique()
year = 21
departement = 75
#
# Main
#

data = px.bar(df, x="classe", y="faits", hover_name="faits", title=f'Delinquance en France en 20{year} dans le département {departement}')

if __name__ == '__main__':

    app = dash.Dash(__name__)
    app.layout = html.Nav(children=[
        html.H1(children='Delinquance en France', className='center'),

        dcc.Dropdown(
            id='year-dropdown',  # (4)
            options=[{'label': year, 'value': year} for year in years],
            value=year
        ),
        dcc.Dropdown(
            id='departement-dropdown',  # (4)
            options=[{'label': departement, 'value': departement} for departement in departements],
            value=departements[0]
        ),
        dcc.Graph(
            id='graph1',  # (5)
            figure=data,
        )
    ])

    #
    # RUN APP
    #

    @app.callback(
        Output(component_id='graph1', component_property='figure'),
        [Input(component_id='year-dropdown', component_property='value'), Input(component_id='departement-dropdown', component_property='value')]  # (6)
    )
    def update_figure(input_value, input_value2):  # (7)
        # print in js console
        return px.bar(df[(df['annee'] == input_value) & (df['Code.département'] == input_value2)], x="classe", y="faits", hover_name="faits", title=f'Delinquance en France en 20{input_value} dans le département {input_value2}')

    app.run_server(debug=True)  # (8)
