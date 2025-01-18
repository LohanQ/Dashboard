import os
import pandas as pd


def get_data(file_name: str) -> pd.DataFrame:
    """
    Charge un fichier CSV depuis le répertoire spécifié avec possibilité de gestion par morceaux (chunks).
    :param file_name: Nom du fichier à charger (ex: 'rawdata.csv').
    :return: DataFrame pandas contenant les données chargées ou un DataFrame combiné si chunksize est utilisé.
    """
    #raw_data_path = os.path.join(r"C:\\Users\\lohan\\Downloads", file_name)
    url = 'https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/osm-france-food-service/exports/csv?lang=fr&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B'

    try:
            # Lis le fichier complet
            data = pd.read_csv(url, on_bad_lines='skip', sep=";",encoding='utf-8')
            script_dir = os.path.dirname(__file__)
            dashboard_dir = os.path.abspath(os.path.join(script_dir, "..", ".."))
            dashboard_dir = os.path.join(dashboard_dir, "data","raw")
            raw_data_path = os.path.join(dashboard_dir, file_name)
            data.to_csv(raw_data_path, index=False, sep=";")

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



