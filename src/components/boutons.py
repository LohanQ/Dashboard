import dash_bootstrap_components as dbc
from typing import Dict

def create_buttons(style_button: Dict[str, str])-> dbc.Row:
    """
    Crée les boutons utilisés pour le tableau de bord.
    :param style_button: Style à appliquer aux boutons créés.
    :return: Un objet Row contenant les boutons.
    """
    return dbc.Row([
        dbc.Col(dbc.Button("Répartition par type", id="btn-type", color="primary", className="m-2 w-100", style=style_button), width=3),
        dbc.Col(dbc.Button("Carte des restaurants", id="btn-carte", color="secondary", className="m-2 w-100", style=style_button), width=3),
        dbc.Col(dbc.Button("Répartition par région", id="btn-region", color="success", className="m-2 w-100", style=style_button), width=3),
        dbc.Col(dbc.Button("Répartition par departement", id="btn-departement", color="danger", className="m-2 w-100", style=style_button), width=3),
        dbc.Col(dbc.Button("Trouve ton restaurant", id="btn-restaurant", color="dark", className="m-2 w-100", style=style_button), width=3)  # Pas de virgule ici
    ], justify="center", style={"marginBottom": "20px"})
