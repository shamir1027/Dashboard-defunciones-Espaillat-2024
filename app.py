import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import dash_leaflet as dl
import json
import os

# Inicializar app con Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Cargar datos de defunciones
df = pd.read_excel("data/defunciones_2024.xlsx")

# Cargar datos geográficos desde GeoJSON
geojson_path = 'data/esp_municipios.geojson'
with open(geojson_path, 'r') as f:
    geojson_data = json.load(f)

# Extraer las coordenadas y nombres de los municipios desde el GeoJSON
municipios = []
for feature in geojson_data['features']:
    municipio_name = feature['properties']['NOM_MUNICI']
    coordinates = feature['geometry']['coordinates'][0]  # Coordenadas del polígono
    municipios.append({'municipio': municipio_name, 'coordinates': coordinates})

# Crear un diccionario con las coordenadas por municipio para fácil acceso
municipio_coords = {m['municipio']: m['coordinates'] for m in municipios}

# Verificar que las columnas y datos están correctamente cargados
df["FECHA_DEF"] = pd.to_datetime(df["FECHA_DEF"], errors='coerce')  # Asegurarse que las fechas sean correctas

# Layout general
app.layout = dbc.Container([
    dbc.Row([dbc.Col(html.H2("Dashboard Provincial de Defunciones - Espaillat 2024"), width=12)]),
    html.Hr(),
    dbc.Tabs([
        dbc.Tab(label="Visión General", tab_id="tab1"),
        dbc.Tab(label="Comparativo Municipal", tab_id="tab7"),
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
        df_grouped = df.groupby("MUNICIPIO_MUERTE")["FECHA_DEF"].count().reset_index()
        df_grouped.columns = ['Municipio', 'Numero_Defunciones']
        fig = px.bar(df_grouped, x="Municipio", y="Numero_Defunciones", 
                     labels={"Municipio": "Municipio", "Numero_Defunciones": "Número de Defunciones"},
                     title="Defunciones por Municipio")
        return dcc.Graph(figure=fig)

    elif active_tab == "tab7":
        # Mapa georreferenciado para comparativo municipal
        markers = []
        
        # Crear marcadores para cada municipio con sus coordenadas y defunciones
        for municipio, coords in municipio_coords.items():
            defunciones_municipio = df[df['MUNICIPIO_MUERTE'] == municipio]['FECHA_DEF'].count()
            if defunciones_municipio > 0:
                # Agregar marcador con un tamaño proporcional al número de defunciones
                markers.append(
                    dl.Polygon(
                        positions=coords,
                        color="red",
                        fillOpacity=0.4,
                        weight=1,
                        dashArray="5, 5",
                    )
                )
        
        # Crear el mapa con los marcadores
        fig = dl.Map([dl.TileLayer()] + markers, style={"width": "100%", "height": "500px"})
        return fig

if __name__ == '__main__':
    # Obtener el puerto dinámico asignado por Render o usar 10000 como respaldo
    port = int(os.environ.get("PORT", 10000))
    app.run(debug=True, host="0.0.0.0", port=port)
