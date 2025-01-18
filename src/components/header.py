
import dash_bootstrap_components as dbc
from dash import html

def create_header():
    """
    Crée l'entête du tableau de bord.
    :return: Un objet Row contenant un Header.
    """
    return dbc.Row(
        dbc.Col(
            html.H1("Tableau de bord des restaurants", className="text-center text-primary mb-4"),
            style={"backgroundColor": "#f8f9fa", "padding": "20px", "borderRadius": "10px"}
        )
    )
