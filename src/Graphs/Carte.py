"""
Module Carte.py
--------------------------------
Gère les graphiques et les données pour la carte choroplèthe des délits et crimes en France.

Auteur
------
Léon E.

Fonctions
---------
- get_france_geojson()
    Récupère les données GeoJSON pour la carte de la France.

- get_idf_geojson()
    Récupère les données GeoJSON pour la carte de l'Île-de-France.

- get_map_dataframe_with_params(dataframe, annee, mois, fait, display)
    Obtient un DataFrame adapté pour la carte avec des paramètres spécifiques.

- get_map_dataframe(dataframe, display)
    Obtient un DataFrame adapté pour la carte avec des paramètres par défaut.

- get_map_graph(dataframe, annee, mois, fait, display)
    Obtient les graphiques choroplèthes de la carte de la France et de l'Île-de-France.

- get_graph(geojson, dataframe, title, affichage)
    Obtient un graphique choroplèthe basé sur un GeoJSON et un DataFrame.
"""
import plotly.express as px
import requests

def get_france_geojson():
    """
    Récupère les données GeoJSON pour la carte de la France.

    Returns
    -------
    dict
        Les données GeoJSON pour la carte de la France.
    """
    return requests.get(
        "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements.geojson"
    ).json()

def get_idf_geojson():
    """
    Récupère les données GeoJSON pour la carte de l'Île-de-France.

    Returns
    -------
    dict
        Les données GeoJSON pour la carte de l'Île-de-France.
    """
    return requests.get(
        "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions/ile-de-france/departements-ile-de-france.geojson"
    ).json()

def get_map_dataframe_with_params(dataframe, annee, mois, fait, display):
    """
    Obtient un DataFrame adapté pour la carte avec des paramètres spécifiques.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        Le DataFrame contenant les données.
    annee : str
        L'année à considérer ou "Tout" pour toutes les années.
    mois : str
        Le mois à considérer ou "Tout" pour tous les mois.
    fait : str
        Le type de fait à considérer ou "Tout" pour tous les faits.
    display : int
        Le paramètre d'affichage, -1 pour le nombre brut ou un nombre pour l'affichage par habitant.

    Returns
    -------
    pandas.DataFrame
        Un DataFrame adapté pour la carte avec les paramètres spécifiés.
    """
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
    new_df = dataframe[mois_condition & annee_condition & fait_condition].groupby("num_departement").agg(
        nombre=("nombre", "sum"),
        population=("population", "first")
    ).reset_index()
    if display != -1:
        new_df['nombre'] = new_df['nombre'] / new_df['population'] * display

    return new_df

def get_map_dataframe(dataframe, display):
    """
    Obtient un DataFrame adapté pour la carte avec des paramètres par défaut.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        Le DataFrame contenant les données.
    display : int
        Le paramètre d'affichage, -1 pour le nombre brut ou un nombre pour l'affichage par habitant.

    Returns
    -------
    pandas.DataFrame
        Un DataFrame adapté pour la carte avec des paramètres par défaut.
    """
    df = dataframe.groupby("num_departement").agg(
        nombre=("nombre", "sum"),
        population=("population", "first")
    ).reset_index()
    if display != -1:
        df['nombre'] = df['nombre'] / df['population'] * display

    return df

def get_map_graph(dataframe, annee, mois, fait, display):
    """
    Obtient les graphiques choroplèthes de la carte de la France et de l'Île-de-France.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        Le DataFrame contenant les données.
    annee : str
        L'année à considérer ou "Tout" pour toutes les années.
    mois : str
        Le mois à considérer ou "Tout" pour tous les mois.
    fait : str
        Le type de fait à considérer ou "Tout" pour tous les faits.
    display : int
        Le paramètre d'affichage, -1 pour le nombre brut ou un nombre pour l'affichage par habitant.

    Returns
    -------
    tuple of plotly.graph_objects.Figure
        Les graphiques choroplèthes de la carte de la France et de l'Île-de-France.
    """
    if any(arg != 'Tout' for arg in (annee, mois, fait)):
        reduced_data_frame = get_map_dataframe_with_params(dataframe, annee, mois, fait, display)
    else:
        reduced_data_frame = get_map_dataframe(dataframe, display)

    affichage = f"pour {display} habitants" if display != -1 else "(en nombre commis)"

    graph_france = get_graph(get_france_geojson(), reduced_data_frame,
                             "Carte des délits et crimes en France (métropolitaine) par départements ", affichage)
    graph_idf = get_graph(get_idf_geojson(), reduced_data_frame,
                          "Carte des délits et crimes en Île-de-France par départements ", affichage)

    return graph_france, graph_idf

def get_graph(geojson, dataframe, title, affichage):
    """
    Obtient un graphique choroplèthe basé sur un GeoJSON et un DataFrame.

    Parameters
    ----------
    geojson : dict
        Les données GeoJSON.
    dataframe : pandas.DataFrame
        Le DataFrame contenant les données.
    title : str
        Le titre du graphique.
    affichage : str
        Le type d'affichage spécifique au graphique.

    Returns
    -------
    plotly.graph_objects.Figure
        Le graphique choroplèthe.
    """
    return px.choropleth(
        dataframe,
        geojson=geojson,
        locations="num_departement",
        title=title,
        featureidkey="properties.code",
        color="nombre",
        color_continuous_scale="Viridis_r",
        labels={"nombre": "Délits et crimes " + affichage, "nom_departement": "Département",
                "num_departement": "Code département"},
        basemap_visible=False,
        locationmode="geojson-id",
        projection="mercator",
    ).update_layout(margin={"r": 0, "t": 20, "l": 0, "b": 0}).update_geos(fitbounds="locations", visible=False)
