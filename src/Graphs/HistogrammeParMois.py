import plotly.express as px
import pandas as pd

def get_histogramme_dataframe(dataframe):
    return dataframe.groupby(["num_departement", "mois"])[["nombre"]].sum().reset_index()

def get_histogramme_dataframe_byParams(dataframe, annee, departements:list, fait):
    if annee == "Tout":
        annee_condition = True
    else:
        annee_condition = (dataframe['annee'] == annee)
    if departements == [] or departements == ['Tout']:
        departement_condition = True
    else:
        departement_condition = (dataframe['num_departement'].isin(departements))
    if fait == "Tout":
        fait_condition = True
    else:
        fait_condition = (dataframe['fait'] == fait)
    
    new_df = dataframe[annee_condition & departement_condition & fait_condition].groupby(["num_departement", "mois"])[["nombre"]].sum().reset_index()
    return new_df
 
 
def get_histogramme_graph(dataframe, annee, departement, fait):
    if(any(arg != 'Tout' for arg in (annee, fait)) or departement != 'Tout'):
        df = get_histogramme_dataframe_byParams(dataframe, annee, departement, fait)
    else:
        df = get_histogramme_dataframe(dataframe)
    
    graph = px.histogram(
        df,
        x="mois", 
        y="nombre",
        color="num_departement",
        title="Nombre de délits par mois et par département",
        labels={"nombre": "Nombre de délits"},
    )

    graph.update_xaxes(title="Mois")
    graph.update_yaxes(title="Nombre de délits")
    graph.update_layout(bargap=0)
    return graph



