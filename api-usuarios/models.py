from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
import os

database_path=f"postgresql://postgres:{os.getenv('POST_PASS')}@database-1.cxhxj7mo1oll.us-east-1.rds.amazonaws.com/sre"

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.reflect()
    db.create_all()


class Usuario(db.Model):
    __tablename__ = "usuarios"
    idUsuario = db.Column(db.Integer, primary_key = True)
    dni = db.Column(db.String(8), nullable = False)
    celular = db.Column(db.String(9), nullable = False)
    nombres = db.Column(db.String(50), nullable = False)
    correo = db.Column(db.String(50), nullable = False)
    contrasena = db.Column(db.String(256), nullable = False)
    estado = db.Column(db.String(3), nullable = False)
    
    def __init__(self, dni, celular, nombres, correo, contrasena, estado):
        self.dni = dni
        self.celular = celular
        self.nombres = nombres
        self.correo = correo
        self.contrasena = contrasena
        self.estado = estado
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        try:
            db.session.commit()
            return self.dni
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
            'dni': self.dni,
            'celular': self.celular,
            'nombres': self.nombres,
            'correo': self.correo,
            'estado': self.estado
        }