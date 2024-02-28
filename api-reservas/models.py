from flask_sqlalchemy import SQLAlchemy 
import os

database_path=f"postgresql://postgres:{os.getenv('POST_PASS')}@database-1.cxhxj7mo1oll.us-east-1.rds.amazonaws.com:5432/sre"

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.reflect()
    db.create_all()


class Reserva(db.Model):
    __tablename__ = "reservas"
    idReserva = db.Column(db.Integer, primary_key = True)
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuarios.idUsuario'), nullable=False)
    idEstacionamiento = db.Column(db.Integer, db.ForeignKey('estacionamientos.idEstacionamiento'), nullable=False)
    placaAuto = db.Column(db.String(6), db.ForeignKey('autos.placa'), nullable=False)
    inicioReserva = db.Column(db.DateTime, nullable = False)
    finReserva = db.Column(db.DateTime, nullable = False)
    costoReserva = db.Column(db.Float, nullable=False)
    costoTotal = db.Column(db.Float, nullable=False)
    estadoRegistro = db.Column(db.String(3), nullable=False)

    def __init__(self, idUsuario, idEstacionamiento, placaAuto, inicioReserva, finReserva, costoReserva, costoTotal, estadoRegistro):
        self.idUsuario = idUsuario
        self.idEstacionamiento = idEstacionamiento
        self.placaAuto = placaAuto
        self.inicioReserva = inicioReserva
        self.finReserva = finReserva
        self.costoReserva = costoReserva
        self.costoTotal = costoTotal
        self.estadoRegistro = estadoRegistro

    def insert(self):
        db.session.add(self)
        db.session.commit()
        return self.idReserva

    def update(self):
        try:
            db.session.commit()
            return self.idReserva
        except:
            db.session.rollback()
        finally:
            db.session.close()
            
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()
    
    def format(self):
        return{
            'idReserva':self.idReserva,
            'idUsuario':self.idUsuario,
            'idEstacionamiento':self.idEstacionamiento,
            'placaAuto':self.placaAuto,
            'inicioReserva':self.inicioReserva,
            'finReserva':self.finReserva,
            'costoReserva':self.costoReserva,
            'costoTotal':self.costoTotal,
            'estadoRegistro':self.estadoRegistro
        }
