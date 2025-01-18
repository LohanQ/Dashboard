# -*- coding: utf-8 -*-

import pandas as pd
import os


def prepare_metrics(data: pd.DataFrame) -> dict:
    """
    Pr�pare les m�triques n�cessaires pour le tableau de bord avec des donn�es de restaurants.

    :param data: DataFrame brut ou nettoy� contenant les donn�es des restaurants.
    :return: Dictionnaire contenant les m�triques pr�-calcul�es.
    """
    # Nombre de restaurants par type
    restaurants_par_type = data['Type'].value_counts().reset_index()
    restaurants_par_type.columns = ['Type', 'Count']
    restaurants_par_type = restaurants_par_type.to_dict(orient='records')

    # Nombre de restaurants par d�partement
    restaurants_par_departement_type = data.groupby(['D�partement', 'Type'])['Nom'].count().reset_index(name='Count')
    restaurants_par_departement_type = restaurants_par_departement_type.to_dict(orient='records')

    # Nombre de restaurants par r�gion 
    restaurants_par_region = data.groupby('R�gion')['Nom'].count().reset_index(name='Count')
    restaurants_par_region = restaurants_par_region.to_dict(orient='records')

    # restaurants en fonction des coordonn�es 
    geo_points = data[['Nom', 'latitude', 'longitude']].dropna(subset=['latitude', 'longitude']).to_dict(orient='records')

    # Nombre de restaurants par r�gion 
    restaurants_par_region = data.groupby('R�gion')['Nom'].count().reset_index(name='Count')
    restaurants_par_region = restaurants_par_region.to_dict(orient='records')

    # Type de restaurants dans un d�partement 
    restaurants_par_type_departement = (data.groupby('D�partement')['Type'].apply(lambda x: list(x.unique()))).reset_index(name='Type')  
    restaurants_par_type_departement = restaurants_par_type_departement.to_dict(orient='records')

    # Nom de restaurants dans un d�partement pour un type pr�cis
    restaurants_par_type_nom = (data.groupby(['D�partement','Type'])['Nom'].apply(lambda x: list(x.unique()))).reset_index(name='Nom')  
    restaurants_par_type_nom = restaurants_par_type_nom.to_dict(orient='records')


    return {
        "restaurants_par_type": restaurants_par_type,
        "restaurants_par_departement": restaurants_par_departement_type,
        "restaurants_par_region": restaurants_par_region,
        "geo_points": geo_points,
        "type_departement": restaurants_par_type_departement,
        "nom_type": restaurants_par_type_nom,
  }