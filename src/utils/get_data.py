# src/utils/get_data.py

import pandas as pd
import os

def get_local_data(file_name: str) -> pd.DataFrame:
    """
    Charge un fichier CSV brut depuis le répertoire `data/raw`.

    :param file_name: Nom du fichier à charger (ex: 'rawdata.csv').
    :return: DataFrame pandas contenant les données chargées.
    """
    raw_data_path = os.path.join("data", "raw", file_name)
    
    # Lire le fichier CSV
    data = pd.read_csv(raw_data_path)
    return data