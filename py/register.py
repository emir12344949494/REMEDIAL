from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from pymongo.errors import ConnectionError

app = Flask(__name__)

# Configuración de MongoDB
MONGO_URI = 'mongodb://localhost:27017/'  # Cambia esto según tu configuración
DB_NAME = 'mi_base_de_datos'
COLLECTION_NAME = 'usuarios'

# Conectar a MongoDB
try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    print("Conexión a MongoDB exitosa")
except ConnectionError:
    print("No se pudo conectar a MongoDB")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        fecha_nacimiento = request.form.get('fecha_nacimiento')
        sexo = request.form.get('sexo')
        usuario = request.form.get('usuario')
        correo = request.form.get('correo')
        password = request.form.get('password')

        # Guardar datos en la base de datos
        usuario_data = {
            'nombre': nombre,
            'apellido': apellido,
            'fecha_nacimiento': fecha_nacimiento,
            'sexo': sexo,
            'usuario': usuario,
            'correo': correo,
            'password': password
        }

        collection.insert_one(usuario_data)
        
        return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/')
def index():
    return "Página principal"

if __name__ == '__main__':
    app.run(debug=True)
