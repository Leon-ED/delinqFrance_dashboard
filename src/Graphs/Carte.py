import plotly.express as px
import requests
import  OptionsManager as om
def get_france_geojson():
   return requests.get(
    "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements.geojson"
    ).json()
   
   
   
def get_map_dataframe_with_params(dataframe,annee, mois,fait):
    if mois == "Tout":
        mois_condition = True
    else:
        mois_condition = (dataframe['mois'] == mois)
    if annee == "Tout":
        annee_condition = True
    else:
        annee_condition = (dataframe['annee'] == annee)
    if fait == "Tout":
        fait_condition = True
    else:
        fait_condition = (dataframe['fait'] == fait)
    new_df = dataframe[mois_condition & annee_condition & fait_condition].groupby("num_departement")[["nombre"]].sum().reset_index()
    return new_df
    

def get_map_dataframe(dataframe):
    
    df = dataframe.groupby("num_departement")[["nombre"]].sum().reset_index()
    return df

    


def get_map_graph(dataframe,annee, mois,fait):
    if(om.needs_reduced_data_frame(annee, mois,fait)):
        reduced_data_frame = get_map_dataframe_with_params(dataframe,annee, mois,fait)
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
