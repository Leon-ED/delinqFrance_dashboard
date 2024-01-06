"""
Module CamembertFaits.py
========================
Gère les graphiques et les données des camemberts des faits les plus et moins communs.

Auteur
------
Léon E.

Fonctions
----------
- `get_common_crimes_pie_graph(dataframe, annee, mois, departement, limit=10, ascending=False)`
    Retourne un graphique camembert des faits les plus/moins communs.

- `get_crimes(dataframe, limit=10, ascending=False)`
    Retourne un dataframe des faits les plus/moins communs.

- `get_crimes_byDate_departement(dataframe, annee, mois, departement, limit=10, ascending=False)`
    Retourne un dataframe des faits les plus/moins communs en fonction de la date et du département.
"""


import plotly.express as px


def get_common_crimes_pie_graph(dataframe, annee, mois, departement, limit=10, ascending=False):
    """
    Retourne un graphique camembert des faits les plus/moins communs.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        Le dataframe contenant les données.
    annee : str
        L'année à considérer ou "Tout" pour toutes les années.
    mois : str
        Le mois à considérer ou "Tout" pour tous les mois.
    departement : str
        Le département à considérer ou "Tout" pour tous les départements.
    limit : int, optional
        Le nombre de faits à afficher dans le camembert (par défaut 10).
    ascending : bool, optional
        True pour les faits les moins communs, False pour les plus communs (par défaut False).

    Returns
    -------
    plotly.graph_objects.Figure
        Un graphique camembert de la répartition des faits.
    """
    if any(arg != 'Tout' for arg in (annee, mois, departement)):
        reduced_data_frame = get_crimes_byDate_departement(dataframe, annee, mois, departement, limit=limit,
                                                           ascending=ascending)
    else:
        reduced_data_frame = get_crimes(dataframe, limit=limit, ascending=ascending)

    title = f"Camembert de la répartition des {limit} faits les {'moins' if ascending else 'plus'} communs"
    graph = px.pie(
        reduced_data_frame,
        values="nombre",
        names="fait",
        title=title,
    )

    return graph


def get_crimes(dataframe, limit=10, ascending=False):
    """
    Retourne un dataframe des faits les plus/moins communs.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        Le dataframe contenant les données.
    limit : int, optional
        Le nombre de faits à afficher (par défaut 10).
    ascending : bool, optional
        True pour les faits les moins communs, False pour les plus communs (par défaut False).

    Returns
    -------
    pandas.DataFrame
        Un dataframe avec les faits les plus/moins communs.
    """
    df = dataframe.groupby("fait")[["nombre"]].sum().reset_index()
    df = df.sort_values(by="nombre", ascending=ascending)
    return df.head(limit)


def get_crimes_byDate_departement(dataframe, annee, mois, departement, limit=10, ascending=False):
    """
    Retourne un dataframe des faits les plus/moins communs en fonction de la date et du département.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        Le dataframe contenant les données.
    annee : str
        L'année à considérer ou "Tout" pour toutes les années.
    mois : str
        Le mois à considérer ou "Tout" pour tous les mois.
    departement : str
        Le département à considérer ou "Tout" pour tous les départements.
    limit : int, optional
        Le nombre de faits à afficher (par défaut 10).
    ascending : bool, optional
        True pour les faits les moins communs, False pour les plus communs (par défaut False).

    Returns
    -------
    pandas.DataFrame
        Un dataframe avec les faits les plus/moins communs en fonction de la date et du département.
    """

    annee_condition = True if annee == "Tout" else (dataframe['annee'] == annee)
    mois_condition = True if mois == "Tout" else (dataframe['mois'] == mois)
    departement_condition = True if departement == "Tout" else (dataframe['num_departement'] == departement)

    new_df = dataframe[annee_condition & mois_condition & departement_condition].groupby("fait")[["nombre"]].sum().reset_index()
    new_df = new_df.sort_values(by="nombre", ascending=ascending)
    
    return new_df.head(limit)
