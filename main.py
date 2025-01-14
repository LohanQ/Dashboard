from config import CONFIG
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

    with open('departements.geojson', 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)


    app = dash.Dash(__name__)


    app.layout = html.Div(
        style={"backgroundColor": "#f7f7f7", "fontFamily": "Arial, sans-serif", "padding": "10px", "height": "100vh", "margin": "0"},
        children=[
            html.Header(
                style={"textAlign": "center", "padding": "20px", "backgroundColor": "#0044cc", "color": "white"},
                children=[
                    html.H1("Tableau de bord des restaurants en France"),
                    html.P("Explorez les tendances et les données liées aux restaurants en France.")
                ]
            ),

            html.Div(
                style={"display": "flex", "justifyContent": "center", "margin": "20px 0"},
                children=[
                    html.Button("Répartition par type de restaurant", id="btn-type", n_clicks=0, style={"margin": "10px"}),
                    html.Button("Carte des restaurants", id="btn-carte", n_clicks=0, style={"margin": "10px"}),
                    html.Button("Répartition par région", id="btn-region", n_clicks=0, style={"margin": "10px"}),
                    html.Button("Répartition par commune", id="btn-commune", n_clicks=0, style={"margin": "10px"})
                ]
            ),

            dcc.Store(id="metrics-store", data=metrics),  
            html.Div(id="content", style={"padding": "20px", "flex": 1}),

            html.Footer(
                style={"textAlign": "center", "marginTop": "20px", "padding": "10px", "backgroundColor": "#333", "color": "white"},
                children="Données issues des enregistrements officiels - Projet 2025"
            )
        ]
    )

    @app.callback(
        Output("content", "children"),
        [Input("btn-type", "n_clicks"),
         Input("btn-carte", "n_clicks"),
         Input("btn-region", "n_clicks"),
         Input("btn-commune", "n_clicks")],
        State("metrics-store", "data")  
    )
    def display_content(btn_type, btn_carte, btn_region, btn_commune, metrics):
        ctx = dash.callback_context  
        if not ctx.triggered:
            return html.Div("Sélectionnez un graphique à afficher.")

     
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if button_id == "btn-type":
            return dcc.Graph(
                id='graph-repartition-type',
                figure=px.pie(
                    metrics["restaurants_par_type"],
                    names='Type',
                    values='Count',
                    title="Répartition des restaurants par type"
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
                ).update_layout(template="plotly_white")
            )
               
        elif button_id == "btn-commune":
            s
            departements = list({item["Département"] for item in metrics["restaurants_par_departement"]})
            departements.sort()  

            dropdown = dcc.Dropdown(
                id="departement-dropdown",
                options=[{"label": departement, "value": departement} for departement in departements],
                value=departements[0] if departements else None,
                placeholder="Sélectionnez un département",
                style={"width": "50%", "margin": "0 auto", "padding": "10px"},
            )
            return html.Div(
                [
                    dropdown,
                    dcc.Graph(id="treemap-dynamic"),
                ]
        )


    @app.callback(
    Output("treemap-dynamic", "figure"),
    [Input("departement-dropdown", "value")],
    State("metrics-store", "data"),

    )
    def update_treemap(selected_departement, metrics):

        if selected_departement is None:  
            return px.treemap(title="Veuillez sélectionner un département")


        filtered_data = [item for item in metrics["restaurants_par_departement"] if item['Département'] == selected_departement]
        filtered_data = [item for item in filtered_data if item['Count'] > 0]

        if not filtered_data:
            return px.treemap(title=f"Aucun restaurant trouvé pour le département {selected_departement}")

        
        return px.treemap(
            filtered_data,
            path=['Département', 'Type'], 
            values='Count',  
            color='Count', 
            color_continuous_scale="Viridis", 
            title=f"Répartition des restaurants par type dans le département {selected_departement}"
        ).update_layout(template="plotly_white")

     # Lancer le tableau de bord
    app.run_server(debug=CONFIG['DEBUG'])


def main():
    # Charge les données brutes
    raw_data = get_local_data("osm-france-food-service.csv")
    print("Données brutes chargées :")
    print(raw_data.head())

    # Nettoie les données
    cleaned_data = clean_data(raw_data)
    print("\nDonnées nettoyées :")
    print(cleaned_data.head())

    # Sauvegarde les données nettoyées
    save_cleaned_data(cleaned_data, "cleaneddata.csv")
    print("\nDonnées nettoyées sauvegardées dans le dossier Downloads.")

    metrics = prepare_metrics(cleaned_data)

    # Créer et affiche le tableau de bord
    create_dashboard(cleaned_data, metrics)


if __name__ == "__main__":
    main()