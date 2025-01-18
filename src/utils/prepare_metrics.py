# -*- coding: utf-8 -*-

import pandas as pd
import os


def prepare_metrics(data: pd.DataFrame) -> dict:
    """
    Prépare les métriques nécessaires pour le tableau de bord avec des données de restaurants.

    :param data: DataFrame brut ou nettoyé contenant les données des restaurants.
    :return: Dictionnaire contenant les métriques pré-calculées.
    """
    # Nombre de restaurants par type
    restaurants_par_type = data['Type'].value_counts().reset_index()
    restaurants_par_type.columns = ['Type', 'Count']
    restaurants_par_type = restaurants_par_type.to_dict(orient='records')

    # Nombre de restaurants par département
    restaurants_par_departement_type = data.groupby(['Département', 'Type'])['Nom'].count().reset_index(name='Count')
    restaurants_par_departement_type = restaurants_par_departement_type.to_dict(orient='records')

    # Nombre de restaurants par région 
    restaurants_par_region = data.groupby('Région')['Nom'].count().reset_index(name='Count')
    restaurants_par_region = restaurants_par_region.to_dict(orient='records')

    # restaurants en fonction des coordonnées 
    geo_points = data[['Nom', 'latitude', 'longitude']].dropna(subset=['latitude', 'longitude']).to_dict(orient='records')

    # Nombre de restaurants par région 
    restaurants_par_region = data.groupby('Région')['Nom'].count().reset_index(name='Count')
    restaurants_par_region = restaurants_par_region.to_dict(orient='records')

    # Type de restaurants dans un département 
    restaurants_par_type_departement = (data.groupby('Département')['Type'].apply(lambda x: list(x.unique()))).reset_index(name='Type')  
    restaurants_par_type_departement = restaurants_par_type_departement.to_dict(orient='records')

    # Nom de restaurants dans un département pour un type précis
    restaurants_par_type_nom = (data.groupby(['Département','Type'])['Nom'].apply(lambda x: list(x.unique()))).reset_index(name='Nom')  
    restaurants_par_type_nom = restaurants_par_type_nom.to_dict(orient='records')


    return {
        "restaurants_par_type": restaurants_par_type,
        "restaurants_par_departement": restaurants_par_departement_type,
        "restaurants_par_region": restaurants_par_region,
        "geo_points": geo_points,
        "type_departement": restaurants_par_type_departement,
        "nom_type": restaurants_par_type_nom,
  }