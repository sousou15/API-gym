import json
import logging
from app import app

# Configuración básica de logging
logging.basicConfig(filename='test.log', level=logging.INFO)
logger = logging.getLogger(__name__)

def realizar_prueba_con_logging():
    # Ejemplo de datos de solicitud JSON
    data = {
        "ejercicios": [
            {"id": 1, "nombre": "Sentadillas", "imagen": "sentadillas.jpg", "video": "sentadillas.mp4", "grupo_muscular": ["Piernas"]},
            {"id": 2, "nombre": "Press de banca", "imagen": "press_de_banca.jpg", "video": "press_de_banca.mp4", "grupo_muscular": ["Pecho"]},
            {"id": 3, "nombre": "Dominadas", "imagen": "dominadas.jpg", "video": "dominadas.mp4", "grupo_muscular": ["Espalda", "Brazos"]}
        ]
    }

    # Realizar una solicitud POST a la ruta '/recomendar' con datos de prueba
    with app.test_client() as client:
        response = client.post('/recomendar', json=data)

    # Convertir la respuesta JSON a un diccionario Python
    data = json.loads(response.data)

    # Obtener los grupos musculares faltantes e imprimirlos en el registro
    grupos_faltantes = data["grupos_faltantes"]
    logger.info("Grupos musculares faltantes: %s", grupos_faltantes)

# Ejecutar la prueba con logging
realizar_prueba_con_logging()
