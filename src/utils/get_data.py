import os
import pandas as pd
import numpy as np


def get_local_data(file_name: str) -> pd.DataFrame:
    """
    Charge un fichier CSV depuis le répertoire spécifié avec possibilité de gestion par morceaux (chunks).

    :param file_name: Nom du fichier à charger (ex: 'rawdata.csv').
    :param chunksize: Taille des morceaux à charger (None pour charger tout le fichier d'un coup).
    :return: DataFrame pandas contenant les données chargées ou un DataFrame combiné si chunksize est utilisé.
    """
    #raw_data_path = os.path.join(r"C:\\Users\\lohan\\Downloads", file_name)
    url = 'https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/osm-france-food-service/exports/csv?lang=fr&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B'

    try:
            # Lis le fichier complet
            data = pd.read_csv(url, on_bad_lines='skip', sep=";")
    except pd.errors.ParserError as e:
        print(f"Erreur lors de la lecture du fichier CSV: {e}")
        raise
    except FileNotFoundError as e:
        print(f"Fichier introuvable: {e}")
        raise
    except Exception as e:
        print(f"Erreur inconnue lors de la lecture du fichier: {e}")
        raise

    return data



