import plotly.express as px



def get_most_common_crimes_pie_graph(dataframe,annee, mois, departement):
    if(any(arg != 'Tout' for arg in (annee, mois, departement))):
        print(annee, mois, departement)
        reduced_data_frame = get_most_common_crimes_byDate_departement(dataframe,annee, mois, departement)
    else:
        reduced_data_frame = get_most_common_crimes(dataframe)
    
    graph = px.pie(
        reduced_data_frame,
        values="nombre",
        names="fait",
        title="Les 10 faits les plus communs",
        )
    
    
    return graph

def get_most_common_crimes(dataframe, limit=10):
    df = dataframe.groupby("fait")[["nombre"]].sum().reset_index()
    df = df.sort_values(by="nombre", ascending=False)
    return df.head(limit)

def get_most_common_crimes_byDate_departement(dataframe,annee, mois, departement, limit=10):
    if(annee == "Tout"):
        annee = True
    if(mois == "Tout"):
        mois = True
    if(departement == "Tout"):
        departement = True
 
    new_df = dataframe[(dataframe['annee'] == annee) & (dataframe['mois'] == mois) & (dataframe['num_departement'] == departement)].groupby("fait")[["nombre"]].sum().reset_index()
    new_df = new_df.sort_values(by="nombre", ascending=False)
    return new_df.head(limit)



