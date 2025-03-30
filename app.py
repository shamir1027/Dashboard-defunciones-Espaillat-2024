
# app.py
# Código principal del dashboard final profesional

import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import dash_leaflet as dl
import json

# Inicializar app con Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Cargar datos
df = pd.read_excel("data/defunciones_2024.xlsx")

# Layout general (ejemplo)
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("Dashboard Provincial de Defunciones - Espaillat 2024"), width=12)
    ]),
    html.Hr(),
    dbc.Tabs([
        dbc.Tab(label="Visión General", tab_id="tab1"),
        dbc.Tab(label="Catastróficas", tab_id="tab2"),
        dbc.Tab(label="Traumas", tab_id="tab3"),
        dbc.Tab(label="Temporalidad", tab_id="tab4"),
        dbc.Tab(label="Centros de Salud", tab_id="tab5"),
        dbc.Tab(label="Certificación", tab_id="tab6"),
        dbc.Tab(label="Comparativo Municipal", tab_id="tab7"),
        dbc.Tab(label="Utilidades", tab_id="tab8"),
        dbc.Tab(label="Muertes Infantiles", tab_id="tab9"),
        dbc.Tab(label="Edad Fértil", tab_id="tab10"),
        dbc.Tab(label="⚠️ Calidad del Dato", tab_id="tab11"),
    ], id="tabs", active_tab="tab1"),
    html.Div(id="tab-content")
], fluid=True)

# Callback para mostrar contenido de cada pestaña
@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "active_tab")
)
def render_tab_content(active_tab):
    if active_tab == "tab1":
        return html.Div("Contenido de visión general con mapa, resumen e indicadores.")
    elif active_tab == "tab2":
        return html.Div("Análisis de enfermedades catastróficas")
    elif active_tab == "tab3":
        return html.Div("Análisis de traumas")
    elif active_tab == "tab4":
        return html.Div("Tendencias temporales")
    elif active_tab == "tab5":
        return html.Div("Centros de salud con más certificaciones")
    elif active_tab == "tab6":
        return html.Div("Tipos de certificación y certificantes")
    elif active_tab == "tab7":
        return html.Div("Comparativo municipal con radar y AVPP")
    elif active_tab == "tab8":
        return html.Div("Botones de descarga, exportación, filtros")
    elif active_tab == "tab9":
        return html.Div("Muertes infantiles por edad y causa")
    elif active_tab == "tab10":
        return html.Div("Mujeres en edad fértil fallecidas")
    elif active_tab == "tab11":
        return html.Div("⚠️ Análisis de calidad del dato por centro de salud")
    else:
        return html.Div("Bienvenido al dashboard de defunciones")

if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0", port=10000)
