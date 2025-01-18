import dash_bootstrap_components as dbc
from dash import html

def create_footer():
    """
    Crée le pied de page du tableau de bord.
    :return: Un objet Row contenant un Footer.
    """
    return dbc.Row(
        dbc.Col(
            html.Footer("Données officielles - Projet 2025", className="text-center text-white bg-dark py-3"),
            style={"marginTop": "20px"}
        )
    )
