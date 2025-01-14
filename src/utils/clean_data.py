import pandas as pd
import os

def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoie et prépare les données relatives aux restaurants.

    :param data: DataFrame brut contenant les informations sur les restaurants.
    :return: DataFrame nettoyé.
    """
    # Nettoie les noms de colonnes
    data.columns = data.columns.str.strip().str.replace('\s+', ' ', regex=True)
    print("Colonnes normalisées :", data.columns)

    if 'Nom' not in data.columns or 'Commune' not in data.columns or 'Région' not in data.columns:
        raise KeyError("Certaines colonnes nécessaires sont manquantes : 'Nom', 'Commune', 'Région'.")


    data['nom_complet'] = data['Nom'] + " - " + data['Commune']

    data[['latitude', 'longitude']] = data['OSM Point'].str.split(',', expand=True)
    
    data['latitude'] = pd.to_numeric(data['latitude'], errors='coerce')
    data['longitude'] = pd.to_numeric(data['longitude'], errors='coerce')

    data = data.dropna(subset=['latitude', 'longitude'])

  
    data['Région'] = data['Région'].astype('category')
    data['Département'] = data['Département'].astype('category')

    return data



def save_cleaned_data(data: pd.DataFrame, file_name: str):
    """
    Sauvegarde le DataFrame nettoyé dans un fichier CSV.

    :param data: DataFrame à sauvegarder.
    :param file_name: Nom du fichier de sortie.
    """
    cleaned_data_path = os.path.join(r"C:\\Users\\lohan\\Downloads", file_name)
    data.to_csv(cleaned_data_path, index=False, sep=";")
    print(f"Fichier sauvegardé : {cleaned_data_path}")

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

    # Nombre de restaurants par commune
    restaurants_par_commune = data.groupby('Commune')['Nom'].count().reset_index(name='Count')
    restaurants_par_commune = restaurants_par_commune.to_dict(orient='records')

    return {
        "restaurants_par_type": restaurants_par_type,
        "restaurants_par_departement": restaurants_par_departement_type,
        "restaurants_par_region": restaurants_par_region,
        "geo_points": geo_points,
        "restaurants_par_commune": restaurants_par_commune,
    }
