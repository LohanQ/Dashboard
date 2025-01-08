# src/utils/clean_data.py

import pandas as pd
import os


def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoie et prépare les données.

    :param data: DataFrame brut.
    :return: DataFrame nettoyé.
    """
    # Nettoyer les noms de colonnes
    data.columns = data.columns.str.strip().str.replace('\s+', ' ', regex=True)
    print("Colonnes normalisées :", data.columns)

    # Vérifiez si "Date Décès" ou similaire est présent
    date_deces_col = [col for col in data.columns if "Date" in col and "Déc" in col]
    if not date_deces_col:
        raise KeyError("La colonne 'Date Décès' est introuvable dans le fichier CSV.")
    
    # Utilisez le nom exact trouvé
    data['Date Décès'] = pd.to_datetime(data[date_deces_col[0]], errors='coerce')
    data['Date Naissance'] = pd.to_datetime(data['Date Naissance'], errors='coerce')

    # Calcul de l'âge
    data['Age'] = (data['Date Décès'] - data['Date Naissance']).dt.days // 365
    data['Année Décès'] = data['Date Décès'].dt.year

    # Supprimer les lignes avec des données manquantes
    data = data.dropna(subset=['Age', 'Année Décès', 'Nom Actuel Région Décès'])
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
    Prépare les métriques nécessaires pour le tableau de bord.

    :param data: DataFrame brut ou nettoyé contenant les données.
    :return: Dictionnaire contenant les métriques pré-calculées.
    """
    # Calcul de l'âge moyen par année
    age_moyen_par_an = data.groupby('Année Décès')['Age'].mean().reset_index()
    age_moyen_par_an = age_moyen_par_an.to_dict(orient='records')  # Conversion en liste de dictionnaires

    # Calcul de l'âge moyen par département
    age_moyen_par_departement = data.groupby('Nom Actuel Département Décès')['Age'].mean().reset_index()
    age_moyen_par_departement = age_moyen_par_departement.to_dict(orient='records')  # Conversion en liste de dictionnaires

    # Répartition des sexes
    repartition_sexe = data['Sexe'].value_counts().reset_index()
    repartition_sexe.columns = ['index', 'Sexe']
    repartition_sexe = repartition_sexe.to_dict(orient='records')  # Conversion en liste de dictionnaires

    # Nombre de décès par région et par année
    deces_par_region_annee = data.groupby(['Année Décès', 'Nom Actuel Région Décès']).size().reset_index(name='Count')
    deces_par_region_annee = deces_par_region_annee.to_dict(orient='records')  # Conversion en liste de dictionnaires

    # Distribution des âges
    distribution_ages = data['Age'].tolist()  # Conversion en liste



    return {
        "age_moyen_par_an": age_moyen_par_an,
        "age_moyen_par_departement": age_moyen_par_departement,
        "repartition_sexe": repartition_sexe,
        "deces_par_region_annee": deces_par_region_annee,
        "distribution_ages": distribution_ages,
    }


