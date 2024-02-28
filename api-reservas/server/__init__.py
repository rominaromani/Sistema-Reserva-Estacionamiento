from flask import (
    Flask,
    jsonify,
    abort,
    request as req,
)
import requests
import threading

from models import setup_db, Reserva
from flask_cors import CORS

from datetime import datetime
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
        response.headers.add('Access-Control-Allow-Origin','*')

        return response


    @app.route("/reservas/<idUsuario>", methods=['GET'])
    def get_reservas(idUsuario):
        reservas = Reserva.query.filter_by(idUsuario=idUsuario).order_by('idReserva').all()
        return jsonify({
            'success':True,
            'reservas': [i.format() for i in reservas],
            'total_reservas':len(reservas)
        })
    
    @app.route("/reservas/<idReserva>", methods=['DELETE'])
    def delete_reserva(idReserva):
        if not idReserva:
            abort(400, 'No se recibio un idReserva')
        reserva = Reserva.query.filter_by(idReserva=idReserva).first()
        if not reserva:
            abort(400 ,'No se encontro la reserva')
        
        response1 = requests.patch('http://localhost:5004/estacionamiento/'+str(reserva.idEstacionamiento),json={'estadoRegistro':'DIS'})
        if not response1.json()["success"]:
            abort(500, 'No se pudo actualizar el estacionamiento')

        response2 = requests.patch('http://localhost:5002/autos/'+str(reserva.placaAuto), json={'estado':'DIS'})
        if not response2.json()["success"]:
            abort(500, 'No se pudo actualizar el auto')

        reserva.delete()

        return jsonify({
            'success':True,
            'deleted':idReserva,
            'message':'Reserva eliminada'
        })

    @app.route("/reserva", methods=['POST'])
    def create_reserva():
        data = req.get_json()
        if not data:
            return abort(400, 'No se recibieron datos')

        idUsuario = data.get('idUsuario', None)

        inicioReserva=data.get('inicioReserva',None)
        finReserva=data.get('finReserva',None)

        datetimeInicioReserva=datetime.strptime(inicioReserva, "%Y-%m-%dT%H:%M")
        datetimeFinReserva=datetime.strptime(finReserva, "%Y-%m-%dT%H:%M")

        inicioReserva=str(datetimeInicioReserva)
        finReserva=str(datetimeFinReserva)

        if msg:= v_fecha(datetimeInicioReserva,datetimeFinReserva):
            return abort(400,msg)

        costoReserva=data.get('costoReserva',None)
        costoTotal=data.get('costoTotal',None)
    
        placa = data.get('placa',None)

        opcion = data.get('opcion', None)
        if opcion:
            marca = data.get('marca',None)
            modelo = data.get('modelo',None)
            color = data.get('color',None)

            response_post = requests.post('http://localhost:5002/autos', json={'idUsuario':idUsuario,'placa':placa,'marca':marca,'modelo':modelo,'color':color})
            if not response_post.json()['success']:
                return abort(400, 'No se pudo crear el auto')
            response_patch = requests.patch('http://localhost:5002/autos/'+str(placa), json={'estado':'NOD'})
            if not response_patch.json()['success']:
                return abort(400, 'No se pudo actualizar el auto')
        else:
            response_patch = requests.patch('http://localhost:5002/autos/'+str(placa), json={'estado':'NOD'})
            if not response_patch.json()['success']:
                return abort(400, 'No se pudo actualizar el auto')

        now = datetime.now()

        delayInicio = (datetimeInicioReserva - now).total_seconds()
        delayFin = (datetimeFinReserva - now).total_seconds()

        
        idEstacionamiento=data.get('idEstacionamiento',None)
        requests.patch('http://localhost:5004/estacionamiento/'+str(idEstacionamiento),json={'estadoRegistro':'RES'}) 

        reserva=Reserva(idUsuario, idEstacionamiento, placa, datetimeInicioReserva, datetimeFinReserva, costoReserva, costoTotal, estadoRegistro='PEN')
        idReserva = reserva.insert()

        threading.Timer(delayFin, actualizarEstadoAuto, args=[placa, idReserva]).start()

        threading.Timer(delayInicio, actualizarEstadoEstacionamiento, args=[idEstacionamiento, idReserva]).start()
        threading.Timer(delayFin, actualizarEstadoEstacionamiento, args=[idEstacionamiento, idReserva]).start()

        threading.Timer(delayInicio, actualizarEstadoReserva, args=[idReserva]).start()
        threading.Timer(delayFin, actualizarEstadoReserva, args=[idReserva]).start()

        return jsonify({
            'success':True,
            'created':idReserva,
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