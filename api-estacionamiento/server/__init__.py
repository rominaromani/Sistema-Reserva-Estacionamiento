from flask import (
    Flask,
    jsonify,
    abort,
    request
)
from flask_cors import CORS
from models import setup_db, Estacionamiento
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


    @app.route("/estacionamiento", methods=['GET'])
    def get_estacionamientos():
        lugaresEstacionamiento=[estacionamiento.format() for estacionamiento in Estacionamiento.query.order_by('idEstacionamiento').all()]

        if len(lugaresEstacionamiento) == 0:
                abort(404,'No hay estacionamientos')
        return jsonify({
                'success':True,
                'estacionamientos':lugaresEstacionamiento,
                'total_estacionamientos':len(lugaresEstacionamiento)
        })

    @app.route("/estacionamiento/<id>", methods=['PATCH'])
    def update_estacionamiento(id):
        estacionamiento = Estacionamiento.query.filter(Estacionamiento.idEstacionamiento==id).one_or_none()
        if estacionamiento is None:
            abort(404)
        data = request.get_json()
        estacionamiento.estadoRegistro = data.get('estadoRegistro', estacionamiento.estadoRegistro)
        estacionamiento.update()
        return jsonify({
            'success':True,
            'estacionamiento':estacionamiento.format()
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