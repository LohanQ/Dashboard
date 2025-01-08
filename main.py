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
    # Charger le GeoJSON simplifié
    with open('departements.geojson', 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)

    # Initialisation de l'application Dash
    app = dash.Dash(__name__)

    # Mémorisation des métriques
    app.layout = html.Div(
        style={"backgroundColor": "#f7f7f7", "fontFamily": "Arial, sans-serif", "padding": "10px"},
        children=[
            html.Header(
                style={"textAlign": "center", "padding": "20px", "backgroundColor": "#0044cc", "color": "white"},
                children=[
                    html.H1("Tableau de bord des décès en France"),
                    html.P("Explorez les tendances et les données liées aux décès en France.")
                ]
            ),

            # Boutons pour basculer entre les graphes
            html.Div(
                style={"display": "flex", "justifyContent": "center", "margin": "20px 0"},
                children=[
                    html.Button("Courbe d'âge moyen par année", id="btn-courbe", n_clicks=0, style={"margin": "10px"}),
                    html.Button("Carte interactive des départements", id="btn-carte", n_clicks=0, style={"margin": "10px"}),
                    html.Button("Répartition par sexe", id="btn-sexe", n_clicks=0, style={"margin": "10px"}),
                    html.Button("Évolution par région", id="btn-region", n_clicks=0, style={"margin": "10px"}),
                    html.Button("Distribution des âges", id="btn-distribution", n_clicks=0, style={"margin": "10px"}),
                    html.Button("Treemap par région", id="btn-treemap", n_clicks=0, style={"margin": "10px"}),
                    html.Button("Top 10 communes", id="btn-top-communes", n_clicks=0, style={"margin": "10px"})

                ]
            ),

            # Contenu dynamique des graphes
            dcc.Store(id="metrics-store", data=metrics),  # Stocker les métriques sérialisées
            html.Div(id="content", style={"padding": "20px"}),

            html.Footer(
                style={"textAlign": "center", "marginTop": "20px", "padding": "10px", "backgroundColor": "#333", "color": "white"},
                children="Données issues des enregistrements officiels - Projet 2025"
            )
        ]
    )

    # Callback pour basculer entre les visualisations
    @app.callback(


        Output("content", "children"),
        [Input("btn-courbe", "n_clicks"),
         Input("btn-carte", "n_clicks"),
         Input("btn-sexe", "n_clicks"),
         Input("btn-region", "n_clicks"),
         Input("btn-distribution", "n_clicks"),
         Input("btn-treemap", "n_clicks")],
        State("metrics-store", "data")  # Récupérer les métriques sérialisées
    )
    def display_content(btn_courbe, btn_carte, btn_sexe, btn_region, btn_distribution, btn_treemap, metrics):
        ctx = dash.callback_context  # Identifier le bouton cliqué
        if not ctx.triggered:
            return html.Div("Sélectionnez un graphique à afficher.")

        # Identifier le bouton cliqué
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if button_id == "btn-courbe":
            return dcc.Graph(
                id='graph-age-par-annee',
                figure=px.line(
                    metrics["age_moyen_par_an"],
                    x='Année Décès',
                    y='Age',
                    title="Âge moyen de décès par année",
                    labels={"Age": "Âge moyen", "Année Décès": "Année"}
                ).update_layout(template="plotly_white")
            )
        elif button_id == "btn-carte":
            return dcc.Graph(
                id='map-age-par-departement',
                figure=px.choropleth(
                    metrics["age_moyen_par_departement"],
                    geojson=geojson_data,
                    locations="Nom Actuel Département Décès",
                    featureidkey="properties.nom",
                    color="Age",
                    hover_name="Nom Actuel Département Décès",
                    hover_data=["Age"],
                    color_continuous_scale="Viridis",
                    title="Âge moyen de décès par département"
                ).update_geos(visible=False, fitbounds="locations", resolution=50)
            )
        elif button_id == "btn-sexe":
            return dcc.Graph(
                id='graph-repartition-sexe',
                figure=px.pie(
                    metrics["repartition_sexe"],
                    names='index',
                    values='Sexe',
                    title="Répartition des décès par sexe"
                )
            )
        elif button_id == "btn-region":
            return dcc.Graph(
                id='graph-evolution-region',
                figure=px.area(
                    metrics["deces_par_region_annee"],
                    x='Année Décès',
                    y='Count',
                    color='Nom Actuel Région Décès',
                    title="Évolution des décès par région",
                    labels={"Nom Actuel Région Décès": "Région", "Count": "Nombre de décès"}
                ).update_layout(template="plotly_white")
            )
        elif button_id == "btn-distribution":
            return dcc.Graph(
                id='graph-distribution-ages',
                figure=px.histogram(
                    metrics["distribution_ages"],
                    nbins=20,
                    title="Distribution des âges au décès",
                    labels={"value": "Âge", "count": "Nombre de décès"}
                )
            )
        elif button_id == "btn-treemap":
            dropdown = dcc.Dropdown(
                id="year-dropdown",  # ID modifié pour correspondre au callback
                options=[{'label': str(year), 'value': year}
                        for year in sorted(set(item['Année Décès'] for item in metrics["deces_par_region_annee"]))
                        ],
                value=min([item['Année Décès'] for item in metrics["deces_par_region_annee"]]),  # Valeur par défaut
                placeholder="Sélectionnez une année",
                style={"width": "50%", "margin": "0 auto"}
            )
            return html.Div([
                    dropdown,
                    dcc.Graph(id='treemap-dynamic')
    ])


        elif button_id == "btn-top-10-communes":
            top_10_communes = sorted(
                metrics["deces_par_commune"],  # Assurez-vous que cette clé existe
                key=lambda x: x["Count"],
                reverse=True
            )[:10]  # Prenez les 10 premières communes
    
            return dcc.Graph(
                id='graph-top-10-communes',
                figure=px.bar(
                    top_10_communes,
                    x='Commune',
                    y='Count',
                    title="Top 10 des communes avec le plus de décès",
                    labels={"Commune": "Commune", "Count": "Nombre de décès"}
                ).update_layout(template="plotly_white")
    )


    # Callback pour mettre à jour le treemap en fonction du slider
    @app.callback(

        Output("treemap-dynamic", "figure"),
        [Input("year-dropdown", "value")],
        State("metrics-store", "data")
    )
    def update_treemap(selected_year, metrics):
      
    # Filtrer les données pour l'année sélectionnée
      if selected_year is None:  # Si aucune année n'est sélectionnée
        return px.treemap(title="Veuillez sélectionner une année")
    
    # Filtrer les données pour l'année sélectionnée
      filtered_data = [item for item in metrics["deces_par_region_annee"] if item['Année Décès'] == selected_year]
    
    # Générer le graphique Treemap
      return px.treemap(
        filtered_data,
        path=[px.Constant('France'), 'Nom Actuel Région Décès'],  # Chemin hiérarchique
        values='Count',
        color='Count',
        color_continuous_scale="Viridis",
        title=f"Répartition des décès par région en {selected_year}"
    ).update_layout(template="plotly_white")

    # Lancer le tableau de bord
    app.run_server(debug=False)


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
    print("\nDonnées nettoyées sauvegardées dans le dossier Downloads.")

    metrics = prepare_metrics(cleaned_data)

    # Créer et afficher le tableau de bord
    create_dashboard(cleaned_data, metrics)


if __name__ == "__main__":
    main()