from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    # Aquí podrías redirigir a una página de registro real o mostrar una página de registro.
    return "Página de registro"

@app.route('/login')
def login():
    # Aquí podrías redirigir a una página de inicio de sesión real o mostrar una página de inicio de sesión.
    return "Página de inicio de sesión"

if __name__ == '__main__':
    app.run(debug=True)
