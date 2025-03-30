# app.py
# Código principal del dashboard final profesional

import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import dash_leaflet as dl
import os

# Inicializar app con Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Cargar datos
df = pd.read_excel("data/defunciones_2024.xlsx")

# Verificar las primeras filas para asegurarse de que los datos se cargan bien (esto es para depuración)
print(df.head())  # Esto te ayudará a saber las columnas disponibles

# Layout general
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
        # Gráfico de defunciones por municipio
        fig = px.bar(df,
                     x="MUNICIPIO_MUERTE",  # Asegúrate de que esta columna esté presente
                     y=df.groupby("MUNICIPIO_MUERTE")["FECHA_DEF"].count(),  # Contando las defunciones por municipio
                     labels={"MUNICIPIO_MUERTE": "Municipio", "y": "Número de Defunciones"},
                     title="Defunciones por Municipio")
        return dcc.Graph(figure=fig)

    elif active_tab == "tab2":
        # Gráfico de causas catastróficas
        fig = px.bar(df,
                     x="CIECAUSADEF1",  # Código de causa de muerte
                     y=df.groupby("CIECAUSADEF1")["FECHA_DEF"].count(),
                     labels={"CIECAUSADEF1": "Causa de Muerte", "y": "Número de Defunciones"},
                     title="Defunciones por Causas Catastróficas")
        return dcc.Graph(figure=fig)

    elif active_tab == "tab3":
        # Gráfico de traumas
        fig = px.bar(df,
                     x="LUGAR_OCURRIO_VIOLENCIA",  # Lugar de ocurrencia de los traumas
                     y=df.groupby("LUGAR_OCURRIO_VIOLENCIA")["FECHA_DEF"].count(),
                     labels={"LUGAR_OCURRIO_VIOLENCIA": "Lugar de Trauma", "y": "Número de Defunciones"},
                     title="Defunciones por Traumas")
        return dcc.Graph(figure=fig)

    elif active_tab == "tab4":
        # Gráfico de temporalidad de defunciones
        df["FECHA_DEF"] = pd.to_datetime(df["FECHA_DEF"])  # Asegurarse de que la fecha esté en formato datetime
        fig = px.line(df,
                      x="FECHA_DEF",  # Fecha de defunción
                      y=df.groupby(df["FECHA_DEF"].dt.to_period("M")).size(),  # Defunciones por mes
                      labels={"FECHA_DEF": "Fecha de Defunción", "y": "Número de Defunciones"},
                      title="Tendencias Temporales de Defunciones")
        return dcc.Graph(figure=fig)

    elif active_tab == "tab5":
        # Gráfico de centros de salud
        fig = px.bar(df,
                     x="CENTRO_SALUD",  # Nombre del centro de salud
                     y=df.groupby("CENTRO_SALUD")["FECHA_DEF"].count(),
                     labels={"CENTRO_SALUD": "Centro de Salud", "y": "Número de Defunciones"},
                     title="Defunciones por Centro de Salud")
        return dcc.Graph(figure=fig)

    elif active_tab == "tab6":
        return html.Div("Tipos de certificación y certificantes")

    elif active_tab == "tab7":
        # Mapa georreferenciado para comparativo municipal
        # Asegurarse de que tienes las columnas de latitud y longitud
        if "LATITUD" in df.columns and "LONGITUD" in df.columns:
            markers = [
                dl.CircleMarker(center=[lat, lon], radius=5, color="red") 
                for lat, lon in zip(df["LATITUD"], df["LONGITUD"])
            ]
            fig = dl.Map([dl.TileLayer()] + markers, style={"width": "100%", "height": "500px"})
            return fig
        else:
            return html.Div("No se encontraron coordenadas geográficas en el archivo.")

    elif active_tab == "tab8":
        return html.Div("Botones de descarga, exportación, filtros")

    elif active_tab == "tab9":
        return html.Div("Muertes infantiles por edad y causa")

    elif active_tab == "tab10":
        return html.Div("Mujeres en edad fértil fallecidas")

    elif active_tab == "tab11":
        # Análisis de completitud de datos
        missing_data = df.isnull().sum()  # Contar los valores faltantes por columna
        missing_data = missing_data[missing_data > 0]  # Filtrar solo las columnas con datos faltantes
        fig = px.bar(missing_data, x=missing_data.index, y=missing_data.values,
                     labels={"x": "Variables", "y": "Valores Faltantes"},
                     title="Análisis de Completitud de Datos")
        return dcc.Graph(figure=fig)

    else:
        return html.Div("Bienvenido al dashboard de defunciones")

if __name__ == '__main__':
    # Obtener el puerto dinámico asignado por Render o usar 10000 como respaldo
    port = int(os.environ.get("PORT", 10000))
    app.run(debug=True, host="0.0.0.0", port=port)

