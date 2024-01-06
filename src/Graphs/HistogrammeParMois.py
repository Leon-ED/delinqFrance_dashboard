"""
Module HistogrammeParMois.py
--------------------------------
Gère les graphiques et les données pour l'histogramme du nombre de délits par mois et par département.

Auteur
------
Léon E.

Fonctions
---------
- get_histogramme_dataframe(dataframe)
    Obtient un DataFrame adapté pour l'histogramme.

- get_histogramme_dataframe_byParams(dataframe, annee, departements:list, fait)
    Obtient un DataFrame adapté pour l'histogramme avec des paramètres spécifiques.

- get_histogramme_graph(dataframe, annee, departement, fait)
    Obtient le graphique de l'histogramme du nombre de délits par mois et par département.
"""

import plotly.express as px
import pandas as pd

def get_histogramme_dataframe(dataframe):
    """
    Obtient un DataFrame adapté pour l'histogramme.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        Le DataFrame contenant les données.

    Returns
    -------
    pandas.DataFrame
        Un DataFrame adapté pour l'histogramme.
    """
    return dataframe.groupby(["num_departement", "mois"])[["nombre"]].sum().reset_index()

def get_histogramme_dataframe_byParams(dataframe, annee, departements:list, fait):
    """
    Obtient un DataFrame adapté pour l'histogramme avec des paramètres spécifiques.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        Le DataFrame contenant les données.
    annee : str
        L'année à considérer ou "Tout" pour toutes les années.
    departements : list
        La liste des départements à considérer ou "Tout" pour tous les départements.
    fait : str
        Le type de fait à considérer ou "Tout" pour tous les faits.

    Returns
    -------
    pandas.DataFrame
        Un DataFrame adapté pour l'histogramme avec les paramètres spécifiés.
    """
    if annee == "Tout":
        annee_condition = True
    else:
        annee_condition = (dataframe['annee'] == annee)
    if departements == 'Tout':
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
    """
    Obtient le graphique de l'histogramme du nombre de délits par mois et par département.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        Le DataFrame contenant les données.
    annee : str
        L'année à considérer ou "Tout" pour toutes les années.
    departement : str
        Le département à considérer ou "Tout" pour tous les départements.
    fait : str
        Le type de fait à considérer ou "Tout" pour tous les faits.

    Returns
    -------
    plotly.graph_objects.Figure
        Le graphique de l'histogramme.
    """
    if(any(arg != 'Tout' for arg in (annee, fait)) or departement != 'Tout'):
        df = get_histogramme_dataframe_byParams(dataframe, annee, departement, fait)
    else:
        df = get_histogramme_dataframe(dataframe)
    
    graph = px.histogram(
        df,
        x="mois", 
        y="nombre",
        color="num_departement",
        title="Histogramme du nombre de délits par mois et par département",
        labels={"nombre": "Nombre de délits"},
    )

    graph.update_xaxes(title="Mois")
    graph.update_yaxes(title="Nombre de délits")
    graph.update_layout(bargap=0)
    return graph
