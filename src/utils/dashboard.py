# -*- coding: utf-8 -*-

from dash import dcc, html, Input, Output, State
from threading import Timer
import pandas as pd
import plotly.express as px
import json
import dash
import dash_bootstrap_components as dbc
import webbrowser

from src.components.header import create_header
from src.components.footer import create_footer
from src.components.boutons import create_buttons

def create_dashboard(data: pd.DataFrame, metrics):
    """
    Crée un tableau de bord interactif avec Dash avec des optimisations pour le changement de graphes.
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
        if selected_restaurant:
            return f"Chercher {selected_restaurant} sur Google"  
        return "" 


    def open_browser():
        webbrowser.open_new("http://127.0.0.1:8050/")

    Timer(1, open_browser).start()
    app.run_server()