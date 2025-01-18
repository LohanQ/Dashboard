import pandas as pd
import os

def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoie et prépare les données relatives aux restaurants.
    :param data: DataFrame brut contenant les informations sur les restaurants.
    :return: DataFrame nettoyé.
    """
    # Nettoie les noms de colonnes
    data.columns = data.columns.str.strip().str.replace('\\s+', ' ', regex=True)
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



def save_cleaned_data(data: pd.DataFrame, file_name: str)-> None:
    """
    Sauvegarde le DataFrame nettoyé dans un fichier CSV.

    :param data: DataFrame à sauvegarder.
    :param file_name: Nom du fichier de sortie.
    """
    script_dir = os.path.dirname(__file__)
    dashboard_dir = os.path.abspath(os.path.join(script_dir, "..", ".."))
    dashboard_dir = os.path.join(dashboard_dir, "data","cleaned")
    cleaned_data_path = os.path.join(dashboard_dir, file_name)
    data.to_csv(cleaned_data_path, index=False, sep=";")
    print(f"Fichier sauvegardé : {cleaned_data_path}")
