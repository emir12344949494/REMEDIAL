import os
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)

# Configuraciones
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['MONGO_URI'] = 'mongodb+srv://dayronemirgaliciacaballero:Rafa1500@cluster0.vuyp3.mongodb.net/REMEDIAL'
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'guardadas')  # Carpeta para guardar las imágenes
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

mongo = PyMongo(app)

# Validar extensiones de archivo
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Ruta principal
@app.route('/')
def home():
    return render_template('home.html')

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

        # Verificar si el usuario ya existe
        existing_user = mongo.db.users.find_one({'correo': correo})
        if existing_user:
            flash('El correo ya está registrado.')
            return redirect(url_for('register'))

        # Encriptar la contraseña
        hashed_password = generate_password_hash(password)

        # Insertar los datos en la colección 'users'
        mongo.db.users.insert_one({
            'nombre': nombre,
            'apellido': apellido,
            'fecha_nacimiento': fecha_nacimiento,
            'sexo': sexo,
            'usuario': usuario,
            'correo': correo,
            'password': hashed_password
        })

        flash('Usuario registrado exitosamente.')
        return redirect(url_for('login'))  # Redirige a una página de login después de registrar

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('correo')
        password = request.form.get('password')

        # Buscar usuario en la colección 'registro' de la base de datos
        user = mongo.db.registro.find_one({'correo': correo})

        # Verificar si se encontró un usuario y si la contraseña es correcta
        if user and check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            session['usuario'] = user['usuario']
            flash('Inicio de sesión exitoso.')
            return redirect(url_for('user'))  # Redirigir a la página del usuario

    return render_template('login.html')



# Ruta para mostrar la página de usuario después de iniciar sesión
@app.route('/user', methods=['GET', 'POST'])
def user():
    if 'user_id' in session:
        if request.method == 'POST':
            texto = request.form.get('texto')
            imagen = request.files.get('imagen')

            # Crear post
            post_data = {
                'usuario_id': session['user_id'],
                'usuario': session['usuario'],
                'texto': texto,
                'fecha': datetime.now()
            }

            # Guardar la imagen si se proporciona
            if imagen and allowed_file(imagen.filename):
                filename = secure_filename(imagen.filename)
                image_id = mongo.db.imagenes.insert_one({
                    'filename': filename,
                    'content_type': imagen.content_type,
                    'data': imagen.read()
                }).inserted_id
                post_data['imagen_id'] = str(image_id)
            elif imagen and not allowed_file(imagen.filename):
                flash('Formato de imagen no permitido. Usa PNG, JPG o JPEG.')
                return redirect(url_for('user'))

            # Guardar post en la base de datos
            mongo.db.imagenes.insert_one(post_data)
            flash('Post creado exitosamente.')

        # Recuperar los posts para mostrarlos en el feed
        imagenes = list(mongo.db.imagenes.find().sort('fecha', -1))  # Ordenar por fecha descendente

        # Imprimir para depuración
        print(imagenes)

        return render_template('user.html', posts=imagenes)

    else:
        flash('Por favor, inicia sesión primero.')
        return redirect(url_for('login'))


# Cerrar sesión
@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada exitosamente.')
    return redirect(url_for('home'))

if __name__ == '__main__':
    # Crear la carpeta de uploads si no existe
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)

    