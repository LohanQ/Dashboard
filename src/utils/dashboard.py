# -*- coding: utf-8 -*-

from dash import dcc, html, Input, Output, State
from threading import Timer
import pandas as pd
import plotly.express as px
import json
import dash
import dash_bootstrap_components as dbc
import webbrowser

from src.components import create_buttons, create_footer, create_header

def create_dashboard(data: pd.DataFrame, metrics):
    """
    Crée un tableau de bord Dash avec des graphiques.
    
    :param data: Données nettoyées utilisées pour générer les graphiques.
    :param metrics: Les métriques calculées à partir des données utilisées dans les graphiques.
    :return: L'application Dash avec l'interface utilisateur et les callbacks configurés.
    """

    with open('data/departements.geojson', 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)

    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

    style_card = {
        "backgroundColor": "#f8f9fa",
        "borderRadius": "10px",  
        "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)", 
        "padding": "20px",
        "transition": "transform 0.3s ease-in-out"
    }

    style_header = {
        "font-family": "Poppins, sans-serif", 
        "font-weight": "600", 
    }

    style_button = {
        "transition": "all 0.3s ease-in-out",
    }


    app.layout = dbc.Container(
    fluid=True,
    children=[
        # Stockage des métriques
        dcc.Store(id="metrics-store", data=metrics), 

        # Appel du header
        create_header(),  # Appel du composant header

        # Appel des boutons
        create_buttons(style_button),  # Appel de la fonction qui retourne les boutons

        # Contenu dynamique qui changera en fonction des clics
        dbc.Row(
            dbc.Col(html.Div(id="content", className="p-4", style=style_card), width=12)
        ),

        # Appel du footer
        create_footer(),  # Appel du composant footer
    ]
)


    @app.callback(
        Output("content", "children"),
        [Input("btn-type", "n_clicks"),
         Input("btn-carte", "n_clicks"),
         Input("btn-region", "n_clicks"),
         Input("btn-departement", "n_clicks"),
         Input("btn-restaurant", "n_clicks")],
        State("metrics-store", "data")
    )
    def display_content(btn_type, btn_carte, btn_region, btn_departement,btn_restaurant, metrics):
        """
        Met à jour le contenu affiché en fonction du bouton cliqué.
        :param btn_type, btn_carte, btn_region, btn_departement,btn_restaurant: Le bouton séléctionné.
        :param metrics: Les métriques qui contiennent les données nécessaires pour afficher les graphiques.
        :return: Un graphique correspondant au bouton cliqué.
        """
        ctx = dash.callback_context
        if not ctx.triggered:
            return html.Div("Sélectionnez un graphique à afficher.", style={"textAlign": "center", "padding": "50px", "fontSize": "18px", "color": "#6c757d"})

        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if button_id == "btn-type":
            return dcc.Graph(
                figure=px.pie(
                    metrics["restaurants_par_type"],
                    names='Type',
                    values='Count',
                    title="Répartition des restaurants par type",
                    template="seaborn",
                ).update_traces(
                    textinfo='percent+label'
                )
            )

        elif button_id == "btn-carte":
            return dcc.Graph(
                figure=px.choropleth(
                    metrics["restaurants_par_departement"],
                    geojson=geojson_data,
                    locations="Département",
                    featureidkey="properties.nom",
                    color="Count",
                    title="Nombre de restaurants par département",
                ).update_geos(
                    visible=False,
                    fitbounds="locations",
                    resolution=50
                ).update_layout(
                    height=700,
                )
            )

        elif button_id == "btn-region":
            return dcc.Graph(
                figure=px.bar(
                    metrics["restaurants_par_region"],
                    x='Région',
                    y='Count',
                    title="Nombre de restaurants par région",
                    text="Count"
                ).update_traces(
                    textposition='auto',
                )
            )

        elif button_id == "btn-departement":
        
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

        elif button_id == "btn-restaurant":
        

            departements = list({item["Département"] for item in metrics["restaurants_par_departement"]})
            departements.sort()  

            dropdown1 = dcc.Dropdown(
                id="restaurant-dropdown1",
                options=[{"label": departement, "value": departement} for departement in departements],
                value=departements[0] if departements else None,  
                placeholder="Sélectionnez un département",
                style={"width": "50%", "margin": "0 auto", "padding": "10px"},
            )

            dropdown2 = dcc.Dropdown(
                id="restaurant-dropdown2",
                options=[],  
                value=None,  
                placeholder="Sélectionnez un type de restaurant",
                style={"width": "50%", "margin": "0 auto", "padding": "10px"},
            )

            dropdown3 = dcc.Dropdown(
                id="restaurant-dropdown3",
                options=[],  
                value=None, 
                placeholder="Sélectionnez un restaurant",
                style={"width": "50%", "margin": "0 auto", "padding": "10px"},
            )

            recherche = dbc.Button(
            "Rechercher sur Google",
            id="restaurant-recherche-boutton",
            color="primary",
            style={"marginTop": "20px", "display": "none", "marginLeft": "auto", "marginRight": "auto", "textAlign": "center"}, 
            href="",  
            target="_blank",  
            )

            return html.Div(
                [
                    dropdown1,
                    dropdown2,
                    dropdown3,
                    html.Div([recherche], style={"textAlign": "center", "marginTop": "20px"}),
                    ])
          



    @app.callback(
        Output("treemap-dynamic", "figure"),
        [Input("departement-dropdown", "value")],
        State("metrics-store", "data"),
    )

    def update_treemap(selected_departement, metrics):
        """
        Met à jour le graphique Treemap.
        :param selected_departement: Le département sélectionné.
        :param metrics: Les métriques utilisées pour filtrer et générer les données.
        :return: Un graphique Treemap.
        """
        if not selected_departement:
            return px.treemap(title="Veuillez sélectionner un département")

        filtered_data = [item for item in metrics["restaurants_par_departement"] 
                        if item['Département'] == selected_departement]

        if not filtered_data:
            return px.treemap(title=f"Aucun restaurant trouvé pour {selected_departement}")

        fig = px.treemap(
            filtered_data,
            path=['Département', 'Type'],
            values='Count',
            title=f"Répartition des restaurants par type dans {selected_departement}"
        )
        
        fig.update_layout(
            height=600,
        )
        
        return fig

    @app.callback(
        Output("restaurant-dropdown2", "options"),
        [Input("restaurant-dropdown1", "value")],
        State("metrics-store", "data")
    )

    def update_type_dropdown(departement, metrics):
        """
        Met à jour le dropdown .
        :param departement: Le département sélectionné.
        :param metrics: Les métriques utilisées pour filtrer les types de restaurants.
        :return: Les options de type de restaurant disponibles pour le département sélectionné.
        """
        if not departement:
            return "aucun type de restaurant disponible";
        

        filtered_data = [
            item for item in metrics["type_departement"]
            if item["Département"] == departement
        ]

        types = []
        for item in filtered_data:
            types.extend(item["Type"]) 

        return [{"label": t, "value": t} for t in sorted(set(types))] 



    @app.callback(
    Output("restaurant-dropdown3", "options"),
    [Input("restaurant-dropdown2", "value"), Input("restaurant-dropdown1", "value")],
    State("metrics-store", "data")
)
    def update_restaurant_dropdown(selected_type, selected_departement, metrics):
        """
        Met à jour les options du dropdown des restaurants en fonction du type et du département sélectionnés.
        :param selected_type: Le type de restaurant sélectionné.
        :param selected_departement: Le département sélectionné.
        :param metrics: Les métriques utilisées pour filtrer les restaurants.
        :return: Les options de restaurants disponibles en fonction des filtres.
        """
        if not selected_type or not selected_departement:
            return [] 

        filtered_data = [
            item for item in metrics["nom_type"]
            if item["Type"] == selected_type and item["Département"] == selected_departement
        ]

        noms = []
        for item in filtered_data:
            if "Nom" in item and item["Nom"]:
                noms.extend(item["Nom"])

        return [{"label": t, "value": t} for t in sorted(set(n for n in noms if n))]



    @app.callback(
    [Output("restaurant-recherche-boutton", "href"),  
     Output("restaurant-recherche-boutton", "style")],  
    [Input("restaurant-dropdown3", "value"),
     Input("restaurant-dropdown2", "value"),
     Input("restaurant-dropdown1", "value")]
    )
    def search_restaurant_on_internet(selected_restaurant,selected_type, selected_departement):
        """
        Met à jour l'URL de recherche Google et rend visible le bouton de recherche si un restaurant, type et département sont sélectionnés.
        :param selected_restaurant: Le restaurant sélectionné.
        :param selected_type: Le type de restaurant sélectionné.
        :param selected_departement: Le département sélectionné.
        :return: L'URL de recherche Google et le bouton de recherche.
        """
        
        if selected_restaurant and selected_departement and selected_type:
            # Effectue une recherche sur Google 
            search_url = f"https://www.google.com/search?q={selected_restaurant}+{selected_type}+{selected_departement}"
            return search_url, {"display": "inline-block"}  
        return "", {"display": "none"}  



    @app.callback(
        Output("restaurant-link", "children"),  
        [Input("restaurant-dropdown3", "value")]
    )
    def update_link_text(selected_restaurant):
        """
        Met à jour le texte du lien pour rechercher un restaurant sélectionné sur Google.
        :param selected_restaurant: Le restaurant sélectionné.
        :return: Le texte du lien pour effectuer la recherche.
        """
        if selected_restaurant:
            return f"Chercher {selected_restaurant} sur Google"  
        return "" 


    def open_browser():
        """
        Ouvre automatiquement l'application Dash dans un navigateur web.
        """
        webbrowser.open_new("http://127.0.0.1:8050/")

    Timer(1, open_browser).start()
    app.run_server()