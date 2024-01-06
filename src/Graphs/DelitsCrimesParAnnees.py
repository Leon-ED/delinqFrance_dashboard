"""
Module DelitsCrimesParAnnees.py
--------------------------------
Gère les graphiques et les données relatifs à l'évolution du nombre de délits et crimes par années.

Auteur
------
Léon E.

Fonctions
---------
- get_delits_crimes_annees(dataframe, fait, departement)
    Obtient un DataFrame regroupant le nombre de délits et crimes par année
    en fonction du type de fait et du département spécifiés.

- get_delits_crimes_annees_graph(dataframe, fait, departement)
    Obtient un graphique de l'évolution du nombre de délits et crimes par année
    en fonction du type de fait et du département spécifiés.
"""



import plotly.express as px

def get_delits_crimes_annees(dataframe, fait, departement):
    """
    Obtient un DataFrame regroupant le nombre de délits et crimes par année
    en fonction du type de fait et du département spécifiés.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        Le DataFrame contenant les données.
    fait : str
        Le type de fait à considérer ou "Tout" pour tous les faits.
    departement : str
        Le département à considérer ou "Tout" pour tous les départements.

    Returns
    -------
    pandas.DataFrame
        Un DataFrame regroupant le nombre de délits et crimes par année.
    """
    departement_condition = (departement == "Tout") | (dataframe['num_departement'] == departement)
    fait_condition = (fait == "Tout") | (dataframe['fait'] == fait)
    
    new_df = dataframe[fait_condition & departement_condition].groupby("annee")[["nombre"]].sum().reset_index()
    return new_df

def get_delits_crimes_annees_graph(dataframe, fait, departement):
    """
    Obtient un graphique de l'évolution du nombre de délits et crimes par année
    en fonction du type de fait et du département spécifiés.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        Le DataFrame contenant les données.
    fait : str
        Le type de fait à considérer ou "Tout" pour tous les faits.
    departement : str
        Le département à considérer ou "Tout" pour tous les départements.

    Returns
    -------
    plotly.graph_objects.Figure
        Le graphique de l'évolution du nombre de délits et crimes par année.
    """
    new_df = get_delits_crimes_annees(dataframe, fait, departement)
    precision = "dans le " + departement if departement != 'Tout' else 'de tous les départements en fonction des années'
    graph = px.line(
        new_df,
        x="annee",
        y="nombre",
        title=f"Évolution du nombre de délits et crimes {precision}"
    )
    return graph
