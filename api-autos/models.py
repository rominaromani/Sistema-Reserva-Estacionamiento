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

class Auto(db.Model):
    __tablename__ = "autos"
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuarios.idUsuario'), nullable = False)
    placa = db.Column(db.String(6), primary_key = True)
    marca = db.Column(db.String(50), nullable = False)
    modelo = db.Column(db.String(50), nullable = False)
    color = db.Column(db.String(50), nullable = False)
    estado = db.Column(db.String(3), nullable = False)

    def __init__(self, idUsuario, placa, marca, modelo, color, estado):
        self.idUsuario = idUsuario
        self.placa = placa
        self.marca = marca
        self.modelo = modelo
        self.color = color
        self.estado = estado

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.placa
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
            return self.placa
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
        return {
            'idUsuario': self.idUsuario,
            'placa': self.placa,
            'marca': self.marca,
            'modelo': self.modelo,
            'color': self.color,
            'estado': self.estado
        }

