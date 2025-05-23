import uuid
from flask import Flask, jsonify, render_template, request, abort
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId  # Añade esto al inicio de tu archivo
from dotenv import load_dotenv
import os


load_dotenv()

app = Flask(__name__, 
            static_folder='./crud-vuejs/dist/assets',
            template_folder='./crud-vuejs/dist')

cors = CORS(app, resources={r"/*": {"origins": ['http://localhost:5173']}})


API_KEY = "clave_super_secreta_123"  # cámbiala por una más segura

@app.before_request
def verificar_api_key():
    if request.method != 'OPTIONS':  # Excepción para CORS preflight
        key = request.headers.get("x-api-key")
        if key != API_KEY:
            abort(403)  # Prohibido

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, x-api-key'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    return response

#Ruta Mensaje
@app.route('/mensaje')
def mensaje():
    return jsonify('Nuevo mensaje desde el servidor Flask')

@app.route('/', defaults={'path':''})
@app.route('/<path:path>')
def render_vue(path):
    return render_template('index.html')


# Coneccion a base de datos
url_db = f'mongodb+srv://{os.getenv("MONGO_USER")}:{os.getenv("MONGO_PASS")}@{os.getenv("MONGO_CLUSTER")}/?retryWrites=true&w=majority&appName=Datos-crud'
client = MongoClient(url_db)
db = client['demo']
collection = db['data']


#Ruta Books
BOOKS = [
    # {
    #     'id': uuid.uuid4().hex,
    #     'title' : '100 Anos de soledad',
    #     'author' : 'Gabriel Garcia Marquez',
    #     'read' : True,
    # },
    # {
    #     'id': uuid.uuid4().hex,
    #     'title' : 'La ileada',
    #     'author' : 'Homero',
    #     'read' : False,
    # },
    #     {
    #     'id': uuid.uuid4().hex,
    #     'title' : 'La ciudad y los perros',
    #     'author' : 'Mario Vargas Llosa',
    #     'read' : True
    # },
]

@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = { 'status': 'success'}

    BOOKS.clear()  # Limpiar la lista para evitar duplicados
    for doc in collection.find():
        doc.pop('_id', None)  # Eliminar el campo _id para evitar conflictos
        BOOKS.append(doc)

    if request.method == 'POST':
        post_data = request.get_json()
        data_book ={
            'id': uuid.uuid4().hex,
            'title' : post_data.get('title'),
            'author' : post_data.get('author'),
            'read' : post_data.get('read'),
        }
        BOOKS.append(data_book)
        response_object['message'] = 'Book Add!'
        collection.insert_one({                   # Insertar el nuevo
            '_id': data_book['id'],  # Usamos el nuevo ID como _id
            **data_book
        })
    else:
        response_object['books'] = BOOKS

    return jsonify(response_object)

@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_books(book_id):
    response_object = {'status': 'success'}
    
    if request.method == 'PUT':
        post_data = request.get_json()
        
        remove_book(book_id)
        data_book = {
            'id': uuid.uuid4().hex,  # Generas nuevo ID
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        }
        BOOKS.append(data_book)
        
        # Operaciones en MongoDB
        collection.delete_one({'_id': book_id})  # Eliminar el viejo
        collection.insert_one({                   # Insertar el nuevo
            '_id': data_book['id'],  # Usamos el nuevo ID como _id
            **data_book
        })
        
        response_object['message'] = 'Book updated!'

    elif request.method == 'DELETE':

        remove_book(book_id)
        collection.delete_one({'_id': book_id})
        response_object['message'] = 'Book removed!'
    
    return jsonify(response_object)

def remove_book(book_id):
    # Tu función original sin cambios
    for book in BOOKS:
        if book['id'] == book_id:
            BOOKS.remove(book)
            return True
    return False   


if __name__ == '__main__':
    app.run(debug=True)