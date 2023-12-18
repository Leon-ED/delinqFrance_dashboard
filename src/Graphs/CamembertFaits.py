import plotly.express as px


def get_least_common_crimes_pie_graph(dataframe,annee, mois, departement):
    if(any(arg != 'Tout' for arg in (annee, mois, departement))):
        reduced_data_frame = get_crimes_byDate_departement(dataframe,annee, mois, departement, limit=10, ascending = True)
    else:
        reduced_data_frame = get_crimes(dataframe, limit=10, ascending = True)
    
    graph = px.pie(
        reduced_data_frame,
        values="nombre",
        names="fait",
        title="Les 10 faits les moins communs",
        )
    
    return graph



def get_common_crimes_pie_graph(dataframe,annee, mois, departement, limit=10, ascending = False):
    if(any(arg != 'Tout' for arg in (annee, mois, departement))):
        reduced_data_frame = get_crimes_byDate_departement(dataframe,annee, mois, departement, limit=limit, ascending = ascending)
    else:
        reduced_data_frame = get_crimes(dataframe, limit=limit, ascending = ascending)
    

    title = f"Les {limit} faits les { 'moins' if ascending else 'plus'} communs"
    graph = px.pie(
        reduced_data_frame,
        values="nombre",
        names="fait",
        title=title,
        )
    
    
    return graph

def get_crimes(dataframe, limit=10, ascending = False):
    df = dataframe.groupby("fait")[["nombre"]].sum().reset_index()
    df = df.sort_values(by="nombre", ascending=ascending)
    return df.head(limit)

def get_crimes_byDate_departement(dataframe, annee, mois, departement, limit=10, ascending = False):
    if annee == "Tout":
        annee_condition = True
    else:
        annee_condition = (dataframe['annee'] == annee)
    
    if mois == "Tout":
        mois_condition = True
    else:
        mois_condition = (dataframe['mois'] == mois)
    
    if departement == "Tout":
        departement_condition = True
    else:
        departement_condition = (dataframe['num_departement'] == departement)
 
    new_df = dataframe[annee_condition & mois_condition & departement_condition].groupby("fait")[["nombre"]].sum().reset_index()
    new_df = new_df.sort_values(by="nombre", ascending=ascending)
    return new_df.head(limit)

