from flask import (
    Flask,
    jsonify,
    abort,
    request
)

from models import setup_db, Auto
from flask_cors import CORS
from server.funciones import *
import os


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


    @app.route("/autos/<idUsuario>", methods=['GET'])
    def get_autos(idUsuario):
        autos = [auto.format() for auto in Auto.query.filter_by(idUsuario=idUsuario).order_by("placa").all()]
        return jsonify({
            'success':True,
            'autos': autos,
            'total_autos':len(autos)
        })

    @app.route("/autos", methods=['POST'])
    def create_auto():
        data = request.get_json()
        idUsuario = data.get('idUsuario', None)
        if not idUsuario:
            abort(400, 'No se recibio un usuario')
        if not data:
            abort(400, 'No se recibieron datos')
        placa = data.get('placa',None)
        if msg:= v_placa(placa):
            abort(400, msg)
        marca = data.get('marca',None)
        if msg:= v_marca(marca):
            abort(400, msg)
        modelo = data.get('modelo',None)
        if msg:= v_modelo(modelo):
            abort(400, msg)
        color = data.get('color',None)
        if msg:= v_color(color):
            abort(400, msg)
        try:
            auto = Auto(idUsuario=idUsuario,placa=placa, marca=marca, modelo=modelo, color=color, estado='DIS')
            newAutoPlaca = auto.insert()
            return jsonify({
                'success':True,
                'created': newAutoPlaca,
                'message':'Auto creado'
            })
        except Exception as e:
            print(e)
            abort(500)
        
    @app.route("/autos/<placa>", methods=['DELETE'])
    def delete_auto(placa):
        if not placa:
            abort(400, 'No se recibio un placa')
        auto = Auto.query.filter_by(placa=placa).first()
        if not auto:
            abort(400, 'No se encontro el auto')
        auto.delete()
        return jsonify({
            'success':True,
            'deleted':placa,
            'message':'Auto eliminado'
        })
    
    @app.route("/autos/<placa>", methods=['PATCH'])
    def update_auto(placa):
        data = request.get_json()
        if not data:
            abort(400, 'No se recibieron datos')
        if not placa:
            abort(400, 'No se recibio una placa')
        marca = data.get('marca',None)
    
        modelo = data.get('modelo',None)

        color = data.get('color',None)
        
        estado = data.get('estado',None)
        
        auto = Auto.query.filter_by(placa=placa).first()
        if not auto:
            abort(400, 'No se encontro el auto')
        if marca != None:
            auto.marca = marca
        if modelo != None:
            auto.modelo = modelo
        if color != None:
            auto.color = color
        if estado != None:
            auto.estado = estado
        auto.update()
        return jsonify({
            'success':True,
            'updated':placa,
            'message':'Auto actualizado'
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