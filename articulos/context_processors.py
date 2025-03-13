import requests

def obtener_imagen_inspiradora():
    """
    Obtiene una imagen inspiradora de Unsplash.
    """
    url = "https://api.unsplash.com/photos/random"
    params = {
        "query": "courage, overcoming fear, resilience",
        "orientation": "landscape",
        "count": 1,
        "client_id": "L11GCTzAPRzL_o8a4jTSPOnD7FUhNDru-6VZYGNwMwU"  # ⚠️ Reemplaza con tu API Key de Unsplash
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data[0]["urls"]["regular"]  # Retorna la URL de la imagen
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener la imagen inspiradora: {e}")
        return None  # Retorna None en caso de error

def agregar_imagen_inspiradora(request):
    """
    Context processor para agregar la imagen inspiradora a todas las plantillas.
    """
    return {'imagen_inspiradora': obtener_imagen_inspiradora()}

