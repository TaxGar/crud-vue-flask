import uuid
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS


app = Flask(__name__, 
            static_folder='./crud-vuejs/dist/assets',
            template_folder='./crud-vuejs/dist')

cors = CORS(app, resources={r"/*": {"origins": "*"}})

#Ruta Mensaje
@app.route('/mensaje')
def mensaje():
    return jsonify('Nuevo mensaje desde el servidor Flask')

@app.route('/', defaults={'path':''})
@app.route('/<path:path>')
def render_vue(path):
    return render_template('index.html')

#Ruta Books
BOOKS = [
    {
        'id': uuid.uuid4().hex,
        'title' : '100 Anos de soledad',
        'author' : 'Gabriel Garcia Marquez',
        'read' : True,
    },
    {
        'id': uuid.uuid4().hex,
        'title' : 'La ileada',
        'author' : 'Homero',
        'read' : False,
    },
        {
        'id': uuid.uuid4().hex,
        'title' : 'La ciudad y los perros',
        'author' : 'Mario Vargas Llosa',
        'read' : True
    },
]

@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = { 'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title' : post_data.get('title'),
            'author' : post_data.get('author'),
            'read' : post_data.get('read'),
        })
        response_object['message'] = 'Book Add!'
    else:
        response_object['books'] = BOOKS
    
    return jsonify(response_object)

@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_books(book_id):
    response_object = { 'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_book(book_id)
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title' : post_data.get('title'),
            'author' : post_data.get('author'),
            'read' : post_data.get('read'),
        })
        response_object['message'] = 'Book updated!'

    if request.method == 'DELETE':
        remove_book(book_id)
        
    return jsonify(response_object)

def remove_book(book_id):
    for book in BOOKS:
        if book['id'] == book_id:
            BOOKS.remove(book)
            return True
    return False    



if __name__ == '__main__':
    app.run(debug=True)