import plotly.express as px
import requests
def get_france_geojson():
   return requests.get(
    "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements.geojson"
    ).json()
   
   
   
def get_map_dataframe_byDate(dataframe,annee, mois):
    if(annee == "Tout"):
        annee = True
    if(mois == "Tout"):
        mois = True
    new_df = dataframe[(dataframe['annee'] == annee) & (dataframe['mois'] == mois)].groupby("num_departement")[["nombre"]].sum().reset_index()
    return new_df
    

def get_map_dataframe(dataframe):
    
    df = dataframe.groupby("num_departement")[["nombre"]].sum().reset_index()
    return df

    


def get_map_graph(dataframe,annee, mois):
    if(any(arg != 'Tout' for arg in (annee, mois))):
        reduced_data_frame = get_map_dataframe_byDate(dataframe,annee, mois)
    else:
        reduced_data_frame = get_map_dataframe(dataframe)
    graph = px.choropleth(
        reduced_data_frame,
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
