import streamlit as st
import pandas as pd
import plotly.express as px
import json
import dash_leaflet as dl

# Título de la aplicación
st.title("Dashboard de Defunciones - Espaillat 2024")

# Cargar los datos de defunciones
df = pd.read_excel("data/defunciones_2024.xlsx")

# Cargar el archivo GeoJSON
with open("data/esp_municipios.geojson", "r") as f:
    geojson_data = json.load(f)

# Extraer las coordenadas y nombres de los municipios desde el GeoJSON
municipios = []
for feature in geojson_data['features']:
    municipio_name = feature['properties']['NOM_MUNICI']
    coordinates = feature['geometry']['coordinates'][0]  # Coordenadas del polígono
    municipios.append({'municipio': municipio_name, 'coordinates': coordinates})

# Crear un diccionario con las coordenadas por municipio para fácil acceso
municipio_coords = {m['municipio']: m['coordinates'] for m in municipios}

# Limpiar y preparar los datos de defunciones
df["FECHA_DEF"] = pd.to_datetime(df["FECHA_DEF"], errors='coerce')  # Asegurarse que las fechas sean correctas

# Crear pestañas para cada sección del dashboard
tabs = ["Visión General", "Catastróficas", "Traumas", "Temporalidad", "Centros de Salud", "Certificación", "Comparativo Municipal", "Muertes Infantiles", "Edad Fértil", "⚠️ Calidad del Dato"]
tab_selection = st.sidebar.radio("Selecciona una pestaña:", tabs)

# Lógica para cada pestaña del dashboard
if tab_selection == "Visión General":
    st.subheader("Defunciones por Municipio")
    df_grouped = df.groupby("MUNICIPIO_MUERTE")["FECHA_DEF"].count().reset_index()
    df_grouped.columns = ['Municipio', 'Numero_Defunciones']

    # Gráfico de barras
    fig = px.bar(df_grouped, x="Municipio", y="Numero_Defunciones", 
                 labels={"Municipio": "Municipio", "Numero_Defunciones": "Número de Defunciones"},
                 title="Defunciones por Municipio")
    st.plotly_chart(fig)

elif tab_selection == "Catastróficas":
    st.subheader("Defunciones por Causas Catastróficas")
    # Aquí agregaríamos el análisis y gráfico para las enfermedades catastróficas
    # Crear un gráfico de ejemplo
    fig = px.bar(df, x="CIECAUSADEF1", y=df.groupby("CIECAUSADEF1")["FECHA_DEF"].count(), 
                 title="Defunciones por Causas Catastróficas")
    st.plotly_chart(fig)

elif tab_selection == "Traumas":
    st.subheader("Defunciones por Trauma")
    # Similar, crearíamos el análisis de traumas
    fig = px.bar(df, x="LUGAR_OCURRIO_VIOLENCIA", y=df.groupby("LUGAR_OCURRIO_VIOLENCIA")["FECHA_DEF"].count(),
                 title="Defunciones por Trauma")
    st.plotly_chart(fig)

elif tab_selection == "Temporalidad":
    st.subheader("Tendencias de Defunciones en el Tiempo")
    df["Fecha_Mes"] = df["FECHA_DEF"].dt.to_period("M")
    fig = px.line(df, x="Fecha_Mes", y=df.groupby("Fecha_Mes")["FECHA_DEF"].count(), 
                  title="Defunciones a lo largo del Tiempo")
    st.plotly_chart(fig)

elif tab_selection == "Centros de Salud":
    st.subheader("Defunciones por Centros de Salud")
    # Aquí agregamos análisis por centro de salud
    fig = px.bar(df, x="CENTRO_SALUD", y=df.groupby("CENTRO_SALUD")["FECHA_DEF"].count(),
                 title="Defunciones por Centro de Salud")
    st.plotly_chart(fig)

elif tab_selection == "Certificación":
    st.subheader("Tipos de Certificación y Certificantes")
    # Análisis de certificación
    fig = px.bar(df, x="CERTIFICANTE_MUERTE", y=df.groupby("CERTIFICANTE_MUERTE")["FECHA_DEF"].count(),
                 title="Certificación de Muertes")
    st.plotly_chart(fig)

elif tab_selection == "Comparativo Municipal":
    st.subheader("Comparativo Municipal con Mapa")
    markers = []
    for municipio, coords in municipio_coords.items():
        defunciones_municipio = df[df['MUNICIPIO_MUERTE'] == municipio]['FECHA_DEF'].count()
        if defunciones_municipio > 0:
            markers.append(
                dl.Polygon(
                    positions=coords,
                    color="red",
                    fillOpacity=0.4,
                    weight=1,
                    dashArray="5, 5",
                )
            )
    
    map_fig = dl.Map([dl.TileLayer()] + markers, style={"width": "100%", "height": "500px"})
    st.components.v1.html(map_fig.to_html(), height=600)

elif tab_selection == "Muertes Infantiles":
    st.subheader("Muertes Infantiles")
    # Agregar análisis de muertes infantiles
    fig = px.bar(df, x="EDAD_ANO", y=df.groupby("EDAD_ANO")["FECHA_DEF"].count(), 
                 title="Muertes Infantiles por Edad")
    st.plotly_chart(fig)

elif tab_selection == "Edad Fértil":
    st.subheader("Muertes de Mujeres en Edad Fértil")
    # Crear el análisis para mujeres en edad fértil
    fig = px.bar(df, x="SEXO", y=df.groupby("SEXO")["FECHA_DEF"].count(), 
                 title="Muertes de Mujeres en Edad Fértil")
    st.plotly_chart(fig)

elif tab_selection == "⚠️ Calidad del Dato":
    st.subheader("Análisis de Calidad de los Datos")
    missing_data = df.isnull().sum()
    missing_data = missing_data[missing_data > 0]
    fig = px.bar(missing_data, x=missing_data.index, y=missing_data.values, 
                 title="Análisis de Calidad de Datos")
    st.plotly_chart(fig)
