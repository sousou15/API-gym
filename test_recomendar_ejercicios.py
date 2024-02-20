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

    # Realizar una solicitud POST a la ruta '/recomendar' con datos de prueba
    response = client.post('/recomendar', json=data)

    # Verificar que la respuesta tiene un código de estado 200 (OK)
    assert response.status_code == 200

    # Convertir la respuesta JSON a un diccionario Python
    data = json.loads(response.data)

    # Verificar que la respuesta contiene la clave "grupos_faltantes"
    assert "grupos_faltantes" in data

    # Verificar que la lista de grupos musculares faltantes no esté vacía
    assert len(data["grupos_faltantes"]) > 0


    # Otras aserciones según lo necesario para la aplicación
    # Verificar que los grupos musculares faltantes son los esperados
    # assert set(data["grupos_faltantes"]) == {"Hombros", "Abdomen", ...}
