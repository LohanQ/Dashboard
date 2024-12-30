
from src.utils.get_data import get_local_data
from src.utils.clean_data import clean_data, save_cleaned_data

def main():
    # Charger les données brutes
    raw_data = get_local_data("decees_en_france_raw.csv")
    print("Données brutes chargées :")
    print(raw_data.head())

    # Nettoyer les données
    cleaned_data = clean_data(raw_data)
    print("\nDonnées nettoyées :")
    print(cleaned_data.head())

    # Sauvegarder les données nettoyées
    save_cleaned_data(cleaned_data, "cleaneddata.csv")
    print("\nDonnées nettoyées sauvegardées dans data/cleaned/")

if __name__ == "__main__":
    main()