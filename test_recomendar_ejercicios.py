import json
import pytest
from app import app

@pytest.fixture
def client():
    # Crea un cliente de prueba para la aplicación Flask
    with app.test_client() as client:
        yield client

def test_recomendar_ejercicios_basico(client):
    # Ejemplo de datos de solicitud JSON
    data = {
        "ejercicios": [
            {"id": 1, "nombre": "Sentadillas", "imagen": "sentadillas.jpg", "video": "sentadillas.mp4", "grupo_muscular": ["Piernas"]},
            {"id": 2, "nombre": "Press de banca", "imagen": "press_de_banca.jpg", "video": "press_de_banca.mp4", "grupo_muscular": ["Pecho"]},
            {"id": 3, "nombre": "Dominadas", "imagen": "dominadas.jpg", "video": "dominadas.mp4", "grupo_muscular": ["Espalda", "Brazos"]}
        ]
    }

     # Envía una solicitud POST al endpoint '/recomendar'
    response = client.post('/recomendar', json=data)

    # Verifica que la respuesta tenga el código de estado esperado (200 para éxito)
    assert response.status_code == 200

    # Verifica que la respuesta sea del tipo JSON
    assert response.content_type == 'application/json'

    # Verifica que la respuesta contenga los ejercicios recomendados
    resp = response.get_json()

    assert len(resp) == 7  #  En este caso

    # Verifica que los grupos musculares de los ejercicios recomendados sean exactamente "Abdomen" y "Hombros"
    for ejercicio in resp:
        assert "Abdomen" in ejercicio["grupo_muscular"] or "Hombros" in ejercicio["grupo_muscular"]
    