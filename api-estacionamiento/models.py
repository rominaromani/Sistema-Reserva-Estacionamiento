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


class Estacionamiento(db.Model):
    __tablename__ = "estacionamientos"
    idEstacionamiento = db.Column(db.Integer, primary_key = True)
    lugar = db.Column(db.String(10), nullable=False)
    estadoRegistro = db.Column(db.String(3), nullable=False)
    def __init__(self,  lugar, estadoRegistro):
        self.lugar = lugar
        self.estadoRegistro = estadoRegistro

    def update(self):
            db.session.commit()

    def format(self):
        return{
            'idEstacionamiento':self.idEstacionamiento,
            'lugar':self.lugar,
            'estadoRegistro':self.estadoRegistro
        }



