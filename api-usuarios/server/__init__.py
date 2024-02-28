from functools import wraps
from flask import (
    Flask,
    current_app,
    jsonify,
    abort,
    request
)
from flask_cors import CORS
from werkzeug.security import generate_password_hash

from models import setup_db, Usuario

import jwt
from datetime import datetime, timedelta
from server.funciones import *
import os

def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()
        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }
        if len(auth_headers) != 2:
            abort(401, invalid_msg)

        try:
            token = auth_headers[1]
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            user = Usuario.query.filter_by(correo=data['correo']).first()
            if not user:
                abort(401, 'User not found')
        except jwt.ExpiredSignatureError:
            abort(401, expired_msg) # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            abort(401, invalid_msg)
        return f(user, *args, **kwargs) 
    return _verify


def create_app(test_config=None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('POST_PASS')
    setup_db(app)

    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PATCH,DELETE,OPTIONS,UPDATE')
        return response
    
    
    @app.route('/usuario', methods=['GET'])
    def get_usuarios():
        users = Usuario.query.all()
        return jsonify({'success': True,
                        'users':[user.format() for user in users],
                        'count': len(users)
                        })
    
    @app.route('/usuario', methods=['POST'])
    def create_usuario():
        data = request.get_json()   
        if not data:
            abort(400, 'No se recibieron datos')
        dni = data.get('DNI', None)
        if msg:= v_dni(dni):
            abort(400, msg)
        celular = data.get('celular', None)
        if msg:= v_celular(celular):
            abort(400, msg)
        nombres = data.get('nombres', None)
        if msg:= v_nombre(nombres):
            abort(400, msg)
        correo = data.get('correo', None)
        if msg:= v_correo(correo):
            abort(400, msg)
        contrasena = data.get('contrasena', None)
        if msg:= v_contrasena(contrasena):
            abort(400, msg)
        nuevo_usuario = Usuario(dni, celular, nombres, correo, generate_password_hash(contrasena), 'REG')
        nuevo_usuario.insert()
        return jsonify({
            'success': True,
            'user': nuevo_usuario.format()
            }
        )
    
    @app.route('/usuario/<id>', methods=['PATCH'])
    def update_user(id):
        data = request.get_json()
        if not data:
            abort(400, "No se recibieron datos")
        user = Usuario.query.get(id)
        if user is None:
            abort(400, "El usuario no existe")
        celular = data.get('celular', None)
        if msg:= not v_celular(celular):
            user.celular = celular
        nombres = data.get('nombres', None)
        if msg:= not v_nombre(nombres):
            user.nombres = nombres
        user.update()

        return jsonify({
            'success': True,
            'user': user.format()
        })
        
    @app.route('/usuario/<id>', methods=['GET'])
    def get_user(id):
        user = Usuario.query.get(id)
        if user is None:
            abort(400, "El usuario no existe")
        return jsonify({
            'success': True,
            'user': user.format()
        })

    @app.route('/usuario/<id>', methods=['DELETE'])
    def delete_user(id):
        user = Usuario.query.get(id)
        if user is None:
            abort(400, "El usuario no existe")
        user.delete()
        return jsonify({
            'success': True,
            'id': id
        })

    @app.route('/session', methods=['POST'])
    def login():
        datos = request.get_json()
        correo = datos.get('correo', None)
        if msg:= v_correo(correo, True):
            abort(400, msg)
        contrasena = datos.get('contrasena', None)
        if msg:= v_contrasena(contrasena, True):
            abort(400, msg)
            
        informacion = v_login(correo, contrasena)
        if not informacion['success']:
            abort(403, informacion['message'])
        user = informacion['user']
        token = jwt.encode({
            'id': user.idUsuario,
            'correo': user.correo,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, current_app.config['SECRET_KEY'],
        algorithm='HS256')
        
        return jsonify({
            'success': True,
            'user': user.format(),
            'token': token
        })
    
    @app.route('/session', methods=['PATCH'])
    @token_required
    def session_update(user):
        return jsonify({
            'success': True,
            'time': datetime.utcnow(),
            'user': user.format()
        })
    

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request' if not error.description else error.description
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'error': 401,
            'aunthenticated': False,
            'message': 'Unauthorized' if not error.description else error.description
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            'success': False,
            'error': 403,
            'message': 'Forbidden' if not error.description else error.description
        }), 403
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not found' if not error.description else error.description
        }), 404

    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
                'success': False,
                'error': 422,
                'message': 'Unprocessable' if not error.description else error.description
            }), 422

    @app.errorhandler(500)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Server error' if not error.description else error.description
        }), 500
    
    return app