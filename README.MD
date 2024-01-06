
# Dashboard sur les Crimes et Délits en France

Bienvenue dans le projet du **Dashboard sur les Crimes et Délits en France** ! Ce tableau de bord interactif présente une analyse des données sur les crimes et délits en France Métropolitaine entre 1996 et le premier trimestre de 2022.

----------

## User Guide

### Déploiement

1.  Clonez le dépôt depuis GitHub :
    
    
    `git clone https://github.com/Leon-ED/delinqFrance_dashboard` 
    
2.  Accédez au répertoire du projet :
    
    
    `cd delinqFrance_dashboard` 
    
3.  Installez les dépendances nécessaires avec pip :

    
    `pip install -r requirements.txt` 
    
4.  Exécutez le script principal pour lancer le tableau de bord :
    
    
    `python main.py` 
    
5.  Ouvrez votre navigateur web et accédez à l'url qui apparaît dans la console pour accéder au dashboard
    

----------

## Rapport d'Analyse

Le tableau de bord offre une visualisation interactive des données sur les crimes et délits, permettant de tirer les principales conclusions suivantes :

1.  Répartition Géographique : La carte interactive présente la répartition des crimes et délits par département, offrant une vue détaillée de la situation en France.
    
2.  Évolution Temporelle : Le graphique en ligne expose l'évolution du nombre de crimes et délits au fil des années, identifiant les tendances générales et les périodes d'augmentation ou de diminution.
    
3.  Camembert des Faits : Le camembert interactif permet d'explorer les faits les plus et moins communs, en fonction du mois, de l'année et du département sélectionnés.
    
4.  Histogramme par Mois : L'histogramme offre une représentation mensuelle du nombre de crimes, facilitant une analyse détaillée des variations mensuelles.
    
5.  Débits et Crimes par Années : Le graphique présente les délits et crimes par années, permettant une analyse de long terme des variations.
    

----------

## Guide du développeur
Lors du lancement du `main.py`, le script va regarder si des données sont déjà disponibles localement. Si ce n'est pas le cas il va faire appel automatiquement au `get_data.py`. 
Il est quand même possible de faire appel au `get_data.py` manuellement.

> [!NOTE]
> Le traitement des données téléchargées par get_data.py peut prendre entre 10secondes et 1 minute selon la machine

### Architecture du Code

Le code est structuré de manière modulaire pour faciliter la compréhension et l'extension. Voici une brève description des composants principaux :

-   **Main.py :** Le script principal pour lancer l'application Dash, il contient le layout et les différents callbacks
-   **src/Graphs/** : Dossier contenant les scripts pour générer les différents graphiques. Un fichier par type de graphique
-   **get_data.py :** Script pour récupérer et prétraiter les données.
-   **src/Utils.py :** Module contenant des utilitaires divers.
- **data/ :** Contient (ou contiendra) le fichier `output.csv` qui contient les données utilisées par le dashboard.



----------
