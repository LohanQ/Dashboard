from src.utils import clean_data, save_cleaned_data, prepare_metrics, get_data, create_dashboard



def main()->None:
    """
    Fonction principal gérant le déroulé du code
    """
    raw_data = get_data("osm-france-food-service.csv")
    print("Données brutes chargées :")
    print(raw_data.head())

    cleaned_data = clean_data(raw_data)
    print("\nDonnées nettoyées :")
    print(cleaned_data.head())

    save_cleaned_data(cleaned_data, "cleaneddata.csv")
    metrics = prepare_metrics(cleaned_data)

    create_dashboard(cleaned_data, metrics)

    

if __name__ == "__main__":
    main()