from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    correo = request.form.get('correo')
    password = request.form.get('password')
    
    # Aquí puedes agregar la lógica de autenticación
    # Por ejemplo, comprobar si el correo y la contraseña son correctos

    # Para fines demostrativos, simplemente redirige a la página de inicio
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
