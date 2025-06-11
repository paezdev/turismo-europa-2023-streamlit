# Análisis de Tendencias Turísticas en Europa 2023

## 1. Descripción General
Este proyecto analiza las tendencias de viajes turísticos en Europa durante el año 2023, con el objetivo de proporcionar información valiosa a una agencia de turismo para optimizar sus ofertas y estrategias de marketing.

---

## 2. Objetivos del Proyecto
- Identificar patrones estacionales de viaje.
- Analizar los destinos más populares.
- Explorar la relación entre tipo de alojamiento y gasto diario.
- Evaluar la duración promedio de estancia por destino.
- Visualizar la distribución geográfica de los viajes.
- Presentar los resultados en un dashboard interactivo.

---

## 3. Herramientas y Tecnologías Utilizadas
- **Python** (para análisis y visualización de datos)
- **Google Colab** (para desarrollo y ejecución de análisis y gráficas)
- **Pandas** (manipulación de datos)
- **Plotly** y **Folium** (visualización avanzada y mapas)
- **Looker Studio** (dashboard interactivo y visualización ejecutiva)
- **Streamlit** (opcional, para prototipos de dashboard web)

En streamlit cloud hice las siguientes visualizaciones: 

entrega 3: https://turismo-europa-2023.streamlit.app/
entrega 4: https://turismo-europa-2023-entrega4.streamlit.app/

La visualización de la entrega 4 la hice en el siguiente:
Lokker studio: https://lookerstudio.google.com/reporting/643c25df-5ef6-4d1b-828a-4fbbda6b13b9

Y el notebook en colab:
Colab: https://colab.research.google.com/drive/1-HHkuL-RTBmxVrQPN3dyU7qtHz70YiDO?usp=sharing


---

## 4. Análisis Exploratorio y Visualizaciones (Google Colab)
- **Carga y limpieza de datos:**  
  Se utilizó el archivo `Anexo EA4_Tourist_Travel_Europe.csv`.
- **Visualizaciones generadas:**
  - Gráficos de barras de países y ciudades más visitados.
  - Gráficos de pastel para propósito del viaje y tipo de alojamiento.
  - Gráficos de líneas/barras para viajes por temporada.
  - Mapas interactivos de destinos visitados.
  - Análisis de gasto total, duración promedio y acompañantes.
- **Código y resultados:**  
  El análisis completo y los gráficos se encuentran documentados en el notebook de Google Colab.

---

## 5. Visualización Ejecutiva (Looker Studio)
- **Dashboard interactivo:**  
  Se diseñó un dashboard en Looker Studio con:
  - KPIs principales (total de viajes, países y ciudades visitadas, gasto total, duración y acompañantes promedio).
  - Mapa coroplético de países visitados.
  - Gráficos de barras y pastel para los principales indicadores.
  - Tabla de detalle de viajes con filtros interactivos.
- **Ventajas:**  
  Permite explorar los datos de manera dinámica y obtener insights rápidos para la toma de decisiones.

---

## 6. Cómo Ejecutar el Proyecto Localmente (opcional: Streamlit)
1. Clona este repositorio.
2. Instala las dependencias:  
   ```
   pip install -r requirements.txt
   ```
3. Ejecuta la aplicación:  
   ```
   streamlit run app.py
   ```

---

## 7. Autor y Créditos
- **Autor:** Jean Carlos Páez Ramírez
- **Licencia:** Proyecto académico, uso educativo.

---

## 8. Archivos Entregados
- `Anexo EA4_Tourist_Travel_Europe.csv` (dataset)
- Notebook de Google Colab con análisis y visualizaciones
- Enlace al dashboard de Looker Studio
- (Opcional) Código de la app en Streamlit