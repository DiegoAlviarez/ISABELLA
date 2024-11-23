# utils.py
import pandas as pd
import requests
from io import BytesIO

def load_data(url):
    """
    Carga un archivo de datos desde una URL en formato Excel.
    :param url: str, URL del archivo Excel.
    :return: pd.DataFrame con los datos o None si falla.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Lanza error si el código HTTP no es 200
        data = pd.read_excel(BytesIO(response.content))
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error al cargar datos: {e}")
        return None
    except Exception as e:
        print(f"Error procesando el archivo: {e}")
        return None
