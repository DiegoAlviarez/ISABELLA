import pandas as pd
import requests
from PIL import Image
from io import BytesIO


def load_data(url):
    """
    Carga un archivo de datos desde una URL en formato Excel.
    :param url: str, URL del archivo Excel.
    :return: pd.DataFrame con los datos o None si falla.
    """
    try:
        # Descarga el contenido desde la URL
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Lanza un error si el código HTTP no es 200
        
        # Carga el archivo Excel en un DataFrame
        data = pd.read_excel(BytesIO(response.content))
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar el archivo: {e}")
        return None
    except Exception as e:
        print(f"Error al procesar el archivo Excel: {e}")
        return None


def load_image(url):
    """
    Carga una imagen desde una URL.
    :param url: str, URL de la imagen.
    :return: PIL.Image o None si falla.
    """
    try:
        # Descarga el contenido desde la URL
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Lanza un error si el código HTTP no es 200
        
        # Carga la imagen en un objeto PIL.Image
        image = Image.open(BytesIO(response.content))
        return image
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar la imagen: {e}")
        return None
    except Exception as e:
        print(f"Error al procesar la imagen: {e}")
        return None

