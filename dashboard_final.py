import streamlit as st
import pandas as pd
import plotly.express as px

# Función para cargar los datos
@st.cache_data
def load_data():
    df = pd.read_csv("data/Anexo EA4_Tourist_Travel_Europe.csv")
    return df

# Cargar los datos
df = load_data()

st.set_page_config(page_title="Dashboard Turismo Europa", layout="wide")

# Título y descripción
st.title("🌍 Análisis de Viajes Turísticos en Europa")
st.markdown("Dashboard interactivo para explorar patrones de turismo en Europa según país, temporada, propósito y más.")

# Filtros
with st.sidebar:
    st.header("Filtros")
    pais = st.selectbox("País visitado", ["Todos"] + sorted(df['Country_Visited'].unique().tolist()))
    temporada = st.selectbox("Temporada", ["Todas"] + sorted(df['Season_of_Visit'].unique().tolist()))
    proposito = st.selectbox("Propósito", ["Todos"] + sorted(df['Main_Purpose'].unique().tolist()))
    alojamiento = st.selectbox("Tipo de alojamiento", ["Todos"] + sorted(df['Accommodation_Type'].unique().tolist()))

# Filtrar datos
df_filtrado = df.copy()
if pais != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Country_Visited'] == pais]
if temporada != "Todas":
    df_filtrado = df_filtrado[df_filtrado['Season_of_Visit'] == temporada]
if proposito != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Main_Purpose'] == proposito]
if alojamiento != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Accommodation_Type'] == alojamiento]

# KPIs
k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Total de viajes", len(df_filtrado))
k2.metric("Países visitados", df_filtrado['Country_Visited'].nunique())
k3.metric("Ciudades visitadas", df_filtrado['City_Visited'].nunique())
k4.metric("Gasto total", f"€{df_filtrado['Total_Travel_Cost'].sum():,.0f}")
k5.metric("Duración promedio (días)", f"{df_filtrado['Travel_Duration_Days'].mean():.1f}")
k6.metric("Acompañantes promedio", f"{df_filtrado['Number_of_Companions'].mean():.1f}")

st.markdown("---")

# Visualizaciones principales
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌐 Mapa de países visitados")
    mapa = df_filtrado.groupby('Country_Visited').size().reset_index(name='Viajes')
    fig_map = px.choropleth(
        mapa,
        locations="Country_Visited",
        locationmode="country names",
        color="Viajes",
        color_continuous_scale="Blues",
        title="Cantidad de viajes por país"
    )
    st.plotly_chart(fig_map, use_container_width=True)

with col2:
    st.subheader("🏆 Países más visitados")
    top_paises = df_filtrado['Country_Visited'].value_counts().head(10)
    fig_paises = px.bar(
        top_paises,
        x=top_paises.index,
        y=top_paises.values,
        labels={'x': 'País', 'y': 'Cantidad de viajes'},
        color=top_paises.values,
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig_paises, use_container_width=True)

st.markdown("---")

col3, col4 = st.columns(2)

with col3:
    st.subheader("🎯 Propósito del viaje")
    fig_purpose = px.pie(
        df_filtrado,
        names='Main_Purpose',
        title="Distribución de propósitos del viaje",
        color_discrete_sequence=px.colors.sequential.Blues
    )
    st.plotly_chart(fig_purpose, use_container_width=True)

with col4:
    st.subheader("🏙️ Ciudades más visitadas")
    top_ciudades = df_filtrado['City_Visited'].value_counts().head(10)
    fig_ciudades = px.bar(
        top_ciudades,
        x=top_ciudades.index,
        y=top_ciudades.values,
        labels={'x': 'Ciudad', 'y': 'Cantidad de viajes'},
        color=top_ciudades.values,
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig_ciudades, use_container_width=True)

st.markdown("---")

col5, col6, col7 = st.columns(3)

with col5:
    st.subheader("🚗 Medios de transporte")
    fig_transporte = px.bar(
        df_filtrado['Mode_of_Travel'].value_counts(),
        x=df_filtrado['Mode_of_Travel'].value_counts().index,
        y=df_filtrado['Mode_of_Travel'].value_counts().values,
        labels={'x': 'Medio de transporte', 'y': 'Cantidad'},
        color=df_filtrado['Mode_of_Travel'].value_counts().values,
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig_transporte, use_container_width=True)

with col6:
    st.subheader("🏨 Tipo de alojamiento")
    fig_alojamiento = px.pie(
        df_filtrado,
        names='Accommodation_Type',
        title="Distribución de tipos de alojamiento",
        color_discrete_sequence=px.colors.sequential.Blues
    )
    st.plotly_chart(fig_alojamiento, use_container_width=True)

with col7:
    st.subheader("📅 Viajes por temporada")
    fig_temporada = px.bar(
        df_filtrado['Season_of_Visit'].value_counts(),
        x=df_filtrado['Season_of_Visit'].value_counts().index,
        y=df_filtrado['Season_of_Visit'].value_counts().values,
        labels={'x': 'Temporada', 'y': 'Cantidad de viajes'},
        color=df_filtrado['Season_of_Visit'].value_counts().values,
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig_temporada, use_container_width=True)

st.markdown("---")

# Tabla de detalle
st.subheader("🔎 Detalle de viajes")
st.dataframe(df_filtrado)

st.caption("Fuente: Anexo EA4_Tourist_Travel_Europe.csv | Fecha de actualización: 2025-06-10")