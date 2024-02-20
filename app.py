from flask import Flask, jsonify, request
import json
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt_claims

app = Flask(__name__)

# Función para verificar si el usuario es un administrador
def es_admin():
    # Obtener la identidad y los claims del token JWT
    identity = get_jwt_identity()
    claims = get_jwt_claims()

    # Verificar si el claim 'role' existe y tiene el valor 'admin'
    if claims and 'role' in claims and claims['role'] == 'admin':
        return True
    else:
        return False
    
# Generación de token JWT para un usuario administrador
@app.route('/login_admin', methods=['POST'])
def login_admin():
    # En un escenario real, deberías autenticar al usuario y verificar si es un administrador
    username = request.json.get('username')
    password = request.json.get('password')

    # Verificar las credenciales del usuario (ejemplo básico)
    if username == 'admin' and password == 'admin':
        # Generar un token JWT con un claim personalizado 'role' para indicar que el usuario es un administrador
        access_token = create_access_token(identity=username, additional_claims={'role': 'admin'})
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'mensaje': 'Credenciales incorrectas'}), 401
    
# Cargar los ejercicios desde el archivo JSON externo
with open('ejercicios.json', 'r') as f:
    ejercicios = json.load(f)

# Ruta para obtener todos los ejercicios
@app.route('/ejercicios', methods=['GET'])
@jwt_required()  # Requiere que el usuario esté autenticado con un token JWT válido
def obtener_ejercicios():
    return jsonify(ejercicios)

# Ruta para obtener un ejercicio por su ID
@app.route('/ejercicios/<int:id>', methods=['GET'])
@jwt_required()  # Requiere que el usuario esté autenticado con un token JWT válido
def obtener_ejercicio(id):
    ejercicio = next((x for x in ejercicios if x['id'] == id), None)
    if ejercicio:
        return jsonify(ejercicio)
    else:
        return jsonify({'mensaje': 'Ejercicio no encontrado'}), 404

# Ruta para agregar un nuevo ejercicio
@app.route('/ejercicios', methods=['POST'])
def agregar_ejercicio():
    if not es_admin():
        return jsonify({'mensaje': 'No tienes permisos de administrador para realizar esta acción'}), 403
    nuevo_ejercicio = request.json
    if 'nombre' in nuevo_ejercicio and 'imagen' in nuevo_ejercicio and 'video' in nuevo_ejercicio and 'grupo_muscular' in nuevo_ejercicio:
        nuevo_ejercicio['id'] = ejercicios[-1]['id'] + 1
        ejercicios.append(nuevo_ejercicio)
        return jsonify(nuevo_ejercicio), 201
    else:
        return jsonify({'mensaje': 'El ejercicio debe tener un nombre, imagen, video y grupo muscular'}), 400

# Ruta para eliminar un ejercicio por su ID
@app.route('/ejercicios/<int:id>', methods=['DELETE'])
def eliminar_ejercicio(id):
    if not es_admin():
        return jsonify({'mensaje': 'No tienes permisos de administrador para realizar esta acción'}), 403
    ejercicio = next((x for x in ejercicios if x['id'] == id), None)
    if ejercicio:
        ejercicios.remove(ejercicio)
        return jsonify({'mensaje': 'Ejercicio eliminado'})
    else:
        return jsonify({'mensaje': 'Ejercicio no encontrado'}), 404

# Ruta para realizar consultas
@app.route('/consultar', methods=['GET'])
@jwt_required()  # Requiere que el usuario esté autenticado con un token JWT válido
def consultar_ejercicios():
    # Obtener parámetros de consulta de la URL
    nombre = request.args.get('nombre')
    grupo_muscular = request.args.get('grupo_muscular')

    # Filtrar ejercicios según los parámetros de consulta
    resultados = ejercicios.copy()

    if nombre:
        resultados = [ejercicio for ejercicio in resultados if nombre.lower() in ejercicio['nombre'].lower()]
    if grupo_muscular:
        resultados = [ejercicio for ejercicio in resultados if grupo_muscular.lower() in ejercicio['grupo_muscular'].lower()]

    return jsonify(resultados)

# Ruta para obtener recomendaciones de ejercicios similares
@app.route('/recomendar', methods=['POST'])
@jwt_required()  # Requiere que el usuario esté autenticado con un token JWT válido
def recomendar_ejercicios():
    # Lista con todos los grupos musculares
    todos_los_grupos = ["Piernas", "Pecho", "Espalda", "Brazos", "Hombros", "Abdomen"]
    # Obtener los ejercicios recientes del usuario desde la solicitud
    ejercicios_usuario = request.json['ejercicios']
    
    # Recorrer los ejercicios recientes del usuario y extraer los grupos musculares
    grupos_musculares_usuario = []
    for ejercicio in ejercicios_usuario:
        grupos_musculares_usuario.extend(ejercicio.get('grupo_muscular', []))

    # Determinar los grupos musculares que faltan
    grupos_faltantes = [grupo for grupo in todos_los_grupos if grupo not in grupos_musculares_usuario]

    recomendaciones = []

    for ejercicio in ejercicios:
        for grupo in grupos_faltantes:
            if grupo in ejercicio["grupo_muscular"]:
                recomendaciones.append(ejercicio)
                break

    return jsonify(recomendaciones)

if __name__ == '__main__':
    app.run(debug=True)
