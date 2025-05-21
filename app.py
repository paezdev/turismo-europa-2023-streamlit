import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import folium
from streamlit_folium import folium_static
import calendar

# Configuración de la página
st.set_page_config(
    page_title="Análisis de Tendencias Turísticas en Europa 2023",
    page_icon="✈️",
    layout="wide"
)

# Función para cargar los datos
@st.cache_data
def load_data():
    df = pd.read_csv("data/DOC03_Datos_U2_IDSD_VIS_TOM_DEC_542_CE.csv")
    df['fecha'] = pd.to_datetime(df['fecha'])
    df['mes'] = df['fecha'].dt.month
    df['mes_nombre'] = df['fecha'].dt.month_name()
    return df

# Cargar los datos
df = load_data()

# Título y descripción
st.title("Análisis de Tendencias Turísticas en Europa 2023")
st.markdown("""
Esta aplicación analiza los patrones de viaje en Europa durante 2023 para identificar tendencias
que puedan mejorar las ofertas y estrategias de marketing de una agencia de turismo.
""")

# Crear dos columnas para los filtros
col1, col2, col3 = st.columns(3)

with col1:
    paises_seleccionados = st.multiselect(
        "Seleccionar países",
        options=df['pais'].unique(),
        default=df['pais'].unique()
    )

with col2:
    alojamientos_seleccionados = st.multiselect(
        "Seleccionar tipos de alojamiento",
        options=df['tipo_alojamiento'].unique(),
        default=df['tipo_alojamiento'].unique()
    )

with col3:
    motivos_seleccionados = st.multiselect(
        "Seleccionar motivos de viaje",
        options=df['motivo_viaje'].unique(),
        default=df['motivo_viaje'].unique()
    )

# Filtrar los datos según las selecciones
df_filtrado = df[
    df['pais'].isin(paises_seleccionados) &
    df['tipo_alojamiento'].isin(alojamientos_seleccionados) &
    df['motivo_viaje'].isin(motivos_seleccionados)
]

# Mostrar número de viajes después de filtrar
st.markdown(f"**Número de viajes analizados:** {len(df_filtrado)}")

# Dividir la pantalla en pestañas
tab1, tab2, tab3 = st.tabs(["Patrones y Destinos", "Alojamiento y Satisfacción", "Duración y Distribución Geográfica"])

with tab1:
    # Crear dos columnas para los gráficos
    col1, col2 = st.columns(2)

    with col1:
        # 1. Patrones estacionales de viaje
        st.subheader("Patrones estacionales de viaje")

        # Ordenar los meses cronológicamente
        meses_orden = {
            'January': 1, 'February': 2, 'March': 3, 'April': 4,
            'May': 5, 'June': 6, 'July': 7, 'August': 8,
            'September': 9, 'October': 10, 'November': 11, 'December': 12
        }

        # Contar viajes por mes y ordenar
        viajes_por_mes = df_filtrado['mes_nombre'].value_counts().reset_index()
        viajes_por_mes.columns = ['Mes', 'Número de viajes']
        viajes_por_mes['orden_mes'] = viajes_por_mes['Mes'].map(meses_orden)
        viajes_por_mes = viajes_por_mes.sort_values('orden_mes')

        # Crear gráfico de barras
        fig_meses = px.bar(
            viajes_por_mes,
            x='Mes',
            y='Número de viajes',
            color='Número de viajes',
            color_continuous_scale='Viridis',
            title='Número de viajes por mes'
        )
        fig_meses.update_layout(xaxis_title='Mes', yaxis_title='Número de viajes')
        st.plotly_chart(fig_meses, use_container_width=True)

        # Análisis de patrones estacionales
        max_mes = viajes_por_mes.loc[viajes_por_mes['Número de viajes'].idxmax()]
        min_mes = viajes_por_mes.loc[viajes_por_mes['Número de viajes'].idxmin()]

        st.markdown(f"""
        **Insights:**
        - La temporada alta es en **{max_mes['Mes']}** con **{max_mes['Número de viajes']}** viajes.
        - La temporada baja es en **{min_mes['Mes']}** con **{min_mes['Número de viajes']}** viajes.
        """)

    with col2:
        # 2. Destinos más populares
        st.subheader("Destinos más populares")

        # Contar viajes por ciudad y obtener top 10
        top_ciudades = df_filtrado['ciudad'].value_counts().nlargest(10).reset_index()
        top_ciudades.columns = ['Ciudad', 'Número de viajes']

        # Crear gráfico de barras horizontales
        fig_ciudades = px.bar(
            top_ciudades,
            y='Ciudad',
            x='Número de viajes',
            color='Número de viajes',
            color_continuous_scale='Viridis',
            orientation='h',
            title='Top 10 ciudades más visitadas'
        )
        fig_ciudades.update_layout(yaxis_title='Ciudad', xaxis_title='Número de viajes')
        st.plotly_chart(fig_ciudades, use_container_width=True)

        # Análisis de destinos populares
        top_ciudad = top_ciudades.iloc[0]

        st.markdown(f"""
        **Insights:**
        - **{top_ciudad['Ciudad']}** es la ciudad más visitada con **{top_ciudad['Número de viajes']}** viajes.
        - Las 3 ciudades más populares representan el **{round(top_ciudades.iloc[:3]['Número de viajes'].sum() / df_filtrado.shape[0] * 100, 1)}%** del total de viajes.
        """)

with tab2:
    # Crear dos columnas para los gráficos
    col1, col2 = st.columns(2)

    with col1:
        # 3. Relación entre tipo de alojamiento y gasto diario
        st.subheader("Relación entre tipo de alojamiento y gasto diario")

        # Crear diagrama de caja
        fig_alojamiento = px.box(
            df_filtrado,
            x='tipo_alojamiento',
            y='gasto_diario',
            color='tipo_alojamiento',
            title='Gasto diario por tipo de alojamiento'
        )
        fig_alojamiento.update_layout(xaxis_title='Tipo de alojamiento', yaxis_title='Gasto diario (€)')
        st.plotly_chart(fig_alojamiento, use_container_width=True)

        # Análisis de gasto por tipo de alojamiento
        gasto_promedio = df_filtrado.groupby('tipo_alojamiento')['gasto_diario'].mean().reset_index()
        gasto_promedio = gasto_promedio.sort_values('gasto_diario', ascending=False)

        st.markdown(f"""
        **Insights:**
        - Los alojamientos tipo **{gasto_promedio.iloc[0]['tipo_alojamiento']}** tienen el mayor gasto diario promedio (**{round(gasto_promedio.iloc[0]['gasto_diario'], 2)}€**).
        - Los alojamientos tipo **{gasto_promedio.iloc[-1]['tipo_alojamiento']}** tienen el menor gasto diario promedio (**{round(gasto_promedio.iloc[-1]['gasto_diario'], 2)}€**).
        """)

    with col2:
        # 4. Satisfacción del cliente por país
        st.subheader("Satisfacción del cliente por país")

        # Crear diagrama de caja
        fig_valoracion = px.box(
            df_filtrado,
            x='pais',
            y='valoracion',
            color='pais',
            title='Valoración por país (1-5)'
        )
        fig_valoracion.update_layout(xaxis_title='País', yaxis_title='Valoración')
        st.plotly_chart(fig_valoracion, use_container_width=True)

        # Análisis de valoración por país
        valoracion_promedio = df_filtrado.groupby('pais')['valoracion'].mean().reset_index()
        valoracion_promedio = valoracion_promedio.sort_values('valoracion', ascending=False)

        st.markdown(f"""
        **Insights:**
        - **{valoracion_promedio.iloc[0]['pais']}** tiene la valoración promedio más alta (**{round(valoracion_promedio.iloc[0]['valoracion'], 2)}** de 5).
        - **{valoracion_promedio.iloc[-1]['pais']}** tiene la valoración promedio más baja (**{round(valoracion_promedio.iloc[-1]['valoracion'], 2)}** de 5).
        """)

with tab3:
    # Crear dos columnas para los gráficos
    col1, col2 = st.columns(2)

    with col1:
        # 5. Duración promedio de estancia por destino
        st.subheader("Duración promedio de estancia por destino")

        # Calcular duración promedio por ciudad
        duracion_promedio = df_filtrado.groupby('ciudad')['duracion_estancia'].mean().reset_index()
        duracion_promedio = duracion_promedio.sort_values('duracion_estancia', ascending=False).head(10)
        duracion_promedio.columns = ['Ciudad', 'Duración promedio (días)']

        # Crear gráfico de barras
        fig_duracion = px.bar(
            duracion_promedio,
            x='Ciudad',
            y='Duración promedio (días)',
            color='Duración promedio (días)',
            color_continuous_scale='Viridis',
            title='Top 10 ciudades con mayor duración de estancia'
        )
        fig_duracion.update_layout(xaxis_title='Ciudad', yaxis_title='Duración promedio (días)')
        st.plotly_chart(fig_duracion, use_container_width=True)

        # Análisis de duración de estancia
        top_duracion = duracion_promedio.iloc[0]

        st.markdown(f"""
        **Insights:**
        - **{top_duracion['Ciudad']}** tiene la estancia promedio más larga (**{round(top_duracion['Duración promedio (días)'], 1)}** días).
        - La duración promedio general de estancia es de **{round(df_filtrado['duracion_estancia'].mean(), 1)}** días.
        """)

    with col2:
        # 6. Distribución geográfica de los viajes
        st.subheader("Distribución geográfica de los viajes")

        # Crear mapa
        m = folium.Map(location=[48.8566, 2.3522], zoom_start=4)

        # Diccionario de colores por país
        colores_paises = {
            'España': 'red',
            'Francia': 'blue',
            'Italia': 'green',
            'Alemania': 'purple',
            'Reino Unido': 'orange'
        }

        # Añadir marcadores al mapa
        for idx, row in df_filtrado.iterrows():
            folium.CircleMarker(
                location=[row['latitud'], row['longitud']],
                radius=row['duracion_estancia'] / 3,  # Tamaño proporcional a la duración
                color=colores_paises.get(row['pais'], 'gray'),
                fill=True,
                fill_color=colores_paises.get(row['pais'], 'gray'),
                fill_opacity=0.7,
                popup=f"""
                <b>{row['ciudad']}, {row['pais']}</b><br>
                Fecha: {row['fecha'].strftime('%d-%m-%Y')}<br>
                Alojamiento: {row['tipo_alojamiento']}<br>
                Duración: {row['duracion_estancia']} días<br>
                Gasto diario: {row['gasto_diario']}€<br>
                Valoración: {row['valoracion']}/5<br>
                Motivo: {row['motivo_viaje']}
                """
            ).add_to(m)

        # Añadir leyenda
        legend_html = """
        <div style="position: fixed; bottom: 50px; left: 50px; z-index: 1000; background-color: white; padding: 10px; border: 1px solid grey; border-radius: 5px;">
        <p><b>Países:</b></p>
        """

        for pais, color in colores_paises.items():
            legend_html += f"""
            <p><i class="fa fa-circle" style="color:{color}"></i> {pais}</p>
            """

        legend_html += """
        <p><b>Tamaño:</b> Duración de la estancia</p>
        </div>
        """

        m.get_root().html.add_child(folium.Element(legend_html))

        # Mostrar mapa
        folium_static(m, width=700, height=500)

        st.markdown("""
        **Insights del mapa:**
        - Los círculos más grandes representan estancias más largas.
        - Cada color representa un país diferente.
        - Haz clic en un punto para ver detalles del viaje.
        """)

# Añadir sección de conclusiones
st.header("Conclusiones generales")

# Calcular algunas métricas para las conclusiones
pais_mas_visitado = df_filtrado['pais'].value_counts().idxmax()
ciudad_mas_visitada = df_filtrado['ciudad'].value_counts().idxmax()
mes_mas_popular = df_filtrado['mes_nombre'].value_counts().idxmax()
alojamiento_mas_comun = df_filtrado['tipo_alojamiento'].value_counts().idxmax()
motivo_principal = df_filtrado['motivo_viaje'].value_counts().idxmax()
gasto_promedio = df_filtrado['gasto_diario'].mean()
duracion_promedio = df_filtrado['duracion_estancia'].mean()

st.markdown(f"""
Este análisis de tendencias turísticas en Europa durante 2023 revela patrones importantes para la estrategia de marketing:

- **Destinos populares:** {pais_mas_visitado} es el país más visitado, con {ciudad_mas_visitada} como la ciudad más popular.
- **Estacionalidad:** {mes_mas_popular} es el mes con mayor actividad turística.
- **Alojamiento:** {alojamiento_mas_comun} es el tipo de alojamiento más utilizado.
- **Economía:** El gasto diario promedio es de {round(gasto_promedio, 2)}€, con una estancia media de {round(duracion_promedio, 1)} días.
- **Motivación:** La mayoría de los viajes son por {motivo_principal.lower()}.

Estos insights pueden ayudar a la agencia de turismo a optimizar sus ofertas, ajustar precios según la temporada y mejorar la experiencia del cliente.
""")

# Añadir pie de página
st.markdown("---")
st.markdown("Desarrollado por Jean Carlos Páez Ramírez | Análisis de Tendencias Turísticas en Europa 2023")