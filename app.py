import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from PIL import Image

# URLs de los archivos y gráficos
url_datos = 'https://github.com/gabogam3r53/PowersRangers/raw/develop/Datos/datos_todas_las_jugadoras_posibles.xlsx'
url_grafica_contrato = 'https://github.com/gabogam3r53/PowersRangers/raw/develop/Analisis_Datos/Graficas/Contratos_contra_estadisticas_interesantes_todos_mas_datos.png'
dir_graficas_individuales = 'https://raw.githubusercontent.com/gabogam3r53/PowersRangers/refs/heads/develop/Analisis_Datos/Graficas/Graficas_datos_individuales/'
dir_graficas_por_ano = 'https://raw.githubusercontent.com/gabogam3r53/PowersRangers/refs/heads/develop/Analisis_Datos/Graficas/Graficas_datos_liga_por_a%C3%B1o/'

# Configuración de la página
st.set_page_config(
    page_title="Estadísticas WNBA",
    layout="wide"
)

st.title("Estadísticas de Jugadoras de la WNBA (2016-2024)")

# Función para cargar datos de Excel con manejo de errores
@st.cache_data
def cargar_datos():
    try:
        st.info("Cargando datos desde el archivo remoto...")
        response = requests.get(url_datos, timeout=10)
        response.raise_for_status()  # Verifica si hubo errores en la solicitud
        data = response.content
        return pd.read_excel(BytesIO(data))
    except requests.exceptions.RequestException as e:
        st.error(f"Error al cargar los datos: {e}")
        return pd.DataFrame()  # Retorna un DataFrame vacío si falla

# Función para mostrar imágenes con manejo de errores
def mostrar_imagen(url):
    try:
        st.info("Cargando imagen...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Verifica si hubo errores en la solicitud
        image = Image.open(BytesIO(response.content))
        st.image(image, use_column_width=True)
    except requests.exceptions.RequestException as e:
        st.error(f"Error al cargar la imagen: {e}")
    except Image.UnidentifiedImageError:
        st.error("No se pudo identificar el archivo de imagen.")

# Cargar datos
datos = cargar_datos()
if not datos.empty:
    # Mostrar tabla de datos
    st.write("## Estadísticas de Jugadoras")
    st.dataframe(datos)

    # Mostrar gráfica de contrato
    st.write("## Gráfica: Contrato contra Estadísticas Interesantes")
    mostrar_imagen(url_grafica_contrato)

    # Selección y gráfica de jugadoras individuales
    st.write("## Gráfica: Jugadoras individuales")
    jugadoras = datos['Nombre']
    jugadora_seleccionada = st.selectbox(
        "Selecciona una jugadora para ver su gráfica individual:", jugadoras
    )

    if jugadora_seleccionada:
        nombre_archivo = jugadora_seleccionada.replace(' ', '_') + '.png'
        grafica_url = dir_graficas_individuales + nombre_archivo
        mostrar_imagen(grafica_url)

    # Selección y gráfica de estadísticas por año
    st.write("## Gráfica: Media de estadísticas a través de los años")
    caracteristica = [
        'RANK', 'AGE', 'GP', 'MIN', 'PTS', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%',
        'FTM', 'FTA', 'FT%', 'OREB', 'DREB', 'AST', 'TOV', 'STL', 'BLK', 'PF', '+-', 'DD2', 'FP', 'TD3'
    ]
    caracteristica_seleccionada = st.selectbox(
        "Selecciona una estadística para ver su gráfica a través de los años:", caracteristica
    )

    if caracteristica_seleccionada:
        nombre_archivo = caracteristica_seleccionada.replace(' ', '_') + '.png'
        grafica_url = dir_graficas_por_ano + nombre_archivo
        mostrar_imagen(grafica_url)
else:
    st.error("No se pudieron cargar los datos. Por favor, revisa la fuente de datos.")

