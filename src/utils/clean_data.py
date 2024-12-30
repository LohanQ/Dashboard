# src/utils/clean_data.py

import pandas as pd
import os

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoie les données brutes.

    :param df: DataFrame brut à nettoyer.
    :return: DataFrame nettoyé.
    """
    # Exemple : Supprimer les valeurs nulles
    cleaned_df = df.dropna()

    # Exemple : Renommer des colonnes
    cleaned_df.rename(columns=lambda col: col.strip().lower(), inplace=True)

    return cleaned_df


def save_cleaned_data(df: pd.DataFrame, file_name: str):
    """
    Enregistre un DataFrame nettoyé dans le répertoire `data/cleaned`.

    :param df: DataFrame nettoyé à sauvegarder.
    :param file_name: Nom du fichier de sortie (ex: 'cleaneddata.csv').
    """
    cleaned_data_path = os.path.join("data", "cleaned", 'cleandata')
    os.makedirs(os.path.dirname(cleaned_data_path), exist_ok=True)
    df.to_csv(cleaned_data_path, index=False)