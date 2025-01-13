from src.utils.get_data import get_local_data
from src.utils.clean_data import clean_data, save_cleaned_data, prepare_metrics

import pandas as pd
import plotly.express as px
import json
from dash import dcc, html, Input, Output, State
import dash

def create_dashboard(data: pd.DataFrame, metrics):
    """
    Crée un tableau de bord interactif avec Dash avec des optimisations pour le changement de graphes.
    """
    # Charger le GeoJSON des départements
    with open('departements.geojson', 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)

    # Initialisation de l'application Dash
    app = dash.Dash(__name__)

    # Mémorisation des métriques
    app.layout = html.Div(
        style={
            "background": "linear-gradient(45deg, #f7f7f7, #e6e6e6)",  # Dégradé de fond
            "fontFamily": "Arial, sans-serif",
            "height": "100vh", 
            "margin": "0", 
            "display": "flex", 
            "flexDirection": "row"
        },
        children=[

            # Barre latérale à gauche pour choisir le graphique
            html.Div(
                style={
                    "width": "20%", 
                    "backgroundColor": "#0044cc", 
                    "color": "white", 
                    "padding": "20px", 
                    "display": "flex", 
                    "flexDirection": "column", 
                    "alignItems": "center", 
                    "height": "100vh"
                },
                children=[
                    html.H2("Tableau de bord", style={"textAlign": "center", "marginBottom": "30px"}),
                    html.Button("Répartition par type de restaurant", id="btn-type", n_clicks=0, style={"margin": "10px", "width": "100%"}),
                    html.Button("Carte des restaurants", id="btn-carte", n_clicks=0, style={"margin": "10px", "width": "100%"}),
                    html.Button("Répartition par région", id="btn-region", n_clicks=0, style={"margin": "10px", "width": "100%"}),
                    html.Button("Répartition par commune", id="btn-commune", n_clicks=0, style={"margin": "10px", "width": "100%"})
                ]
            ),

            # Contenu principal avec un fond dégradé, qui affiche les graphes
            html.Div(
                id="content", 
                style={
                    "flex": "1", 
                    "padding": "20px", 
                    "display": "flex", 
                    "flexDirection": "column", 
                    "alignItems": "center", 
                    "height": "100vh"
                },
                children=[
                    # Affichage par défaut de tous les graphes
                    dcc.Graph(
                        id='graph-repartition-type',
                        figure=px.pie(
                            metrics["restaurants_par_type"],
                            names='Type',
                            values='Count',
                            title="Répartition des restaurants par type"
                        ).update_layout(
                            template="plotly_white", height=600, width=1200, margin={"r":0, "t":0, "l":0, "b":0}
                        )
                    ),
                    dcc.Graph(
                        id='map-restaurant-par-departement',
                        figure=px.choropleth(
                            metrics["restaurants_par_departement"],
                            geojson=geojson_data,
                            locations="Département",
                            featureidkey="properties.nom",
                            color="Count",
                            hover_name="Département",
                            hover_data=["Count"],
                            color_continuous_scale="Turbo",  
                            title="Nombre de restaurants par département",
                            range_color=[0, 5000]
                        ).update_geos(
                            visible=False, 
                            fitbounds="locations", 
                            resolution=50
                        ).update_layout(
                            height=600, 
                            width = 1200,  
                            margin={"r":0, "t":0, "l":0, "b":0}, 
                            title="Nombre de restaurants par département"
                        )
                    ),
                    dcc.Graph(
                        id='graph-repartition-region',
                        figure=px.bar(
                            metrics["restaurants_par_region"],
                            x='Région',
                            y='Count',
                            title="Nombre de restaurants par région",
                            labels={"Région": "Région", "Count": "Nombre de restaurants"}
                        ).update_layout(
                            template="plotly_white", height=600, width=1200, margin={"r":0, "t":0, "l":0, "b":0}
                        )
                    ),
                    dcc.Graph(
                        id='graph-repartition-commune',
                        figure=px.bar(
                            metrics["restaurants_par_commune"],
                            x='Commune',
                            y='Count',
                            title="Nombre de restaurants par commune",
                            labels={"Commune": "Commune", "Count": "Nombre de restaurants"}
                        ).update_layout(
                            template="plotly_white", height=600, width=1200, margin={"r":0, "t":0, "l":0, "b":0}
                        )
                    )
                ]
            )
        ]
    )

    # Callback pour basculer entre les visualisations
    @app.callback(
        Output("content", "children"),
        [Input("btn-type", "n_clicks"),
         Input("btn-carte", "n_clicks"),
         Input("btn-region", "n_clicks"),
         Input("btn-commune", "n_clicks")],
        State("metrics-store", "data")  # Récupérer les métriques sérialisées
    )
    def display_content(btn_type, btn_carte, btn_region, btn_commune, metrics):
        ctx = dash.callback_context  # Identifier le bouton cliqué
        if not ctx.triggered:
            return html.Div("Sélectionnez un graphique à afficher.")

        # Identifier le bouton cliqué
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if button_id == "btn-type":
            return dcc.Graph(
                id='graph-repartition-type',
                figure=px.pie(
                    metrics["restaurants_par_type"],
                    names='Type',
                    values='Count',
                    title="Répartition des restaurants par type"
                ).update_layout(
                    template="plotly_white", height=600, width=1200, margin={"r":0, "t":0, "l":0, "b":0}
                )
            )
        elif button_id == "btn-carte":
            return dcc.Graph(
                id='map-restaurant-par-departement',
                figure=px.choropleth(
                    metrics["restaurants_par_departement"],
                    geojson=geojson_data,
                    locations="Département",
                    featureidkey="properties.nom",
                    color="Count",
                    hover_name="Département",
                    hover_data=["Count"],
                    color_continuous_scale="Turbo",  
                    title="Nombre de restaurants par département",
                    range_color=[0, 5000]
                ).update_geos(
                    visible=False, 
                    fitbounds="locations", 
                    resolution=50
                ).update_layout(
                    height=600, 
                    width = 1200,  
                    margin={"r":0, "t":0, "l":0, "b":0}, 
                    title="Nombre de restaurants par département"
                )
            )

        elif button_id == "btn-region":
            return dcc.Graph(
                id='graph-repartition-region',
                figure=px.bar(
                    metrics["restaurants_par_region"],
                    x='Région',
                    y='Count',
                    title="Nombre de restaurants par région",
                    labels={"Région": "Région", "Count": "Nombre de restaurants"}
                ).update_layout(
                    template="plotly_white", height=600, width=1200, margin={"r":0, "t":0, "l":0, "b":0}
                )
            )
        elif button_id == "btn-commune":
            return dcc.Graph(
                id='graph-repartition-commune',
                figure=px.bar(
                    metrics["restaurants_par_commune"],
                    x='Commune',
                    y='Count',
                    title="Nombre de restaurants par commune",
                    labels={"Commune": "Commune", "Count": "Nombre de restaurants"}
                ).update_layout(
                    template="plotly_white", height=600, width=1200, margin={"r":0, "t":0, "l":0, "b":0}
                )
            )

    # Lancer le tableau de bord
    app.run_server(debug=False)


def main():
    # Charger les données brutes
    raw_data = get_local_data("osm-france-food-service.csv")
    print("Données brutes chargées :")
    print(raw_data.head())

    # Nettoyer les données
    cleaned_data = clean_data(raw_data)
    print("\nDonnées nettoyées :")
    print(cleaned_data.head())

    # Sauvegarder les données nettoyées
    save_cleaned_data(cleaned_data, "cleaneddata.csv")
    print("\nDonnées nettoyées sauvegardées dans le dossier Downloads.")

    metrics = prepare_metrics(cleaned_data)

    # Créer et afficher le tableau de bord
    create_dashboard(cleaned_data, metrics)


if __name__ == "__main__":
    main()
