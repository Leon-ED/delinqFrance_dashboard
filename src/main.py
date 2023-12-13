import requests
import pandas as pd
import plotly.express as px
import os
import dash
from dash import dcc
from dash import html

def get_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return pd.read_csv(current_dir + '/../data/output.csv', sep=';')


def get_map_dataframe_byDate(dataframe,annee, mois):
    mask = (dataframe["annee"].astype(str).str.match(annee.replace('*', '.*')) &
            dataframe["mois"].astype(str).str.match(mois.replace('*', '.*')))
    filtered_df = dataframe[mask]
    new_df = filtered_df.groupby("num_departement").sum().reset_index()
    return new_df
    

def get_map_dataframe(dataframe):
    return dataframe.groupby("num_departement")[["nombre"]].sum().reset_index()

    


def get_map_graph(dataframe,annee, mois):
    graph = px.choropleth(
        get_map_dataframe(dataframe),
        geojson=get_france_geojson(),
        locations="num_departement",
        featureidkey="properties.code",
        color="nombre",
        color_continuous_scale="Viridis_r",
        labels={"nombre": "Nombre de délits et crimes", "num_departement": "Département"},
        basemap_visible=False,
        locationmode="geojson-id",
        projection="mercator",
        )
    graph.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    graph.update_geos(fitbounds="locations", visible=False)
    return graph

def get_france_geojson():
   return requests.get(
    "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements.geojson"
    ).json()
   
def main():
    data = get_data()

    departements = data['num_departement'].unique()
    annees = data['annee'].unique()

    default_annee = 2021
    default_departement = departements[0]

    app = dash.Dash(__name__)
    app.layout = html.Nav(children=[
        html.H1(children='Delinquance en France', className='center'),

        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': year, 'value': year} for year in annees],
            value=default_annee
        ),
        dcc.Dropdown(
            id='departement-dropdown',
            options=[{'label': departement, 'value': departement} for departement in departements],
            value=default_departement
        ),
        dcc.Graph(
            id='map_france',
            figure=get_map_graph(data,'*','*'),
        )
    ])

    app.run_server(debug=True)

if __name__ == '__main__':
    main()
