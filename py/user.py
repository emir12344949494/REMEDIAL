from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
import gridfs
import os
from werkzeug.utils import secure_filename
from bson import ObjectId

app = Flask(__name__)

# Configuración de MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["social_network"]
posts_collection = db["posts"]
fs = gridfs.GridFS(db)

# Configuración de subida de archivos
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    posts = list(posts_collection.find())
    for post in posts:
        if 'image_id' in post:
            post['image_url'] = '/image/{}'.format(post['image_id'])
        else:
            post['image_url'] = None
    return render_template('index.html', posts=posts)

@app.route('/post', methods=['POST'])
def post():
    data = request.form
    text = data.get('texto')

    if not text:
        return jsonify({'error': 'Texto del post no proporcionado'}), 400

    post = {
        'text': text,
        'image_id': None
    }

    # Manejo de imagen
    if 'image' in request.files:
        image = request.files['image']
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            file_id = fs.put(image, filename=filename)
            post['image_id'] = file_id

    post_id = posts_collection.insert_one(post).inserted_id
    return jsonify({'message': 'Post creado', 'post_id': str(post_id)}), 201

@app.route('/image/<file_id>')
def image(file_id):
    file = fs.get(ObjectId(file_id))
    return file.read(), {'Content-Type': file.content_type}

@app.route('/historial', methods=['GET'])
def historial():
    posts = list(posts_collection.find())
    for post in posts:
        if 'image_id' in post:
            post['image_url'] = '/image/{}'.format(post['image_id'])
        else:
            post['image_url'] = None
    return jsonify(posts)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
