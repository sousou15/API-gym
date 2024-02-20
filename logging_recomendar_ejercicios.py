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

    # Verificar el código de estado de la response
    if response.status_code == 200:
        try:
            # Convertir la response JSON a un diccionario
            datos_response = response.get_json()
            
            # Obtener los nombres de los ejercicios recomendados y registrarlos
            ejercicios_recomendados = [ejercicio["nombre"] for ejercicio in datos_response]
            logger.info("Ejercicios recomendados: %s", ejercicios_recomendados)
        except json.JSONDecodeError as e:
            logger.error("Error al decodificar JSON: %s", e)
    else:
        logger.error("La solicitud no fue exitosa. Código de estado: %d", response.status_code)

# Ejecutar la prueba con logging
realizar_prueba_con_logging()
