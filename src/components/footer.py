import dash_bootstrap_components as dbc
from dash import html

def create_footer():
    return dbc.Row(
        dbc.Col(
            html.Footer("Donn�es officielles - Projet 2025", className="text-center text-white bg-dark py-3"),
            style={"marginTop": "20px"}
        )
    )
