from datetime import datetime
from models import Reserva
import requests



def v_fecha(inicio,fin):
    if datetime.now()>inicio:
        return "Fecha ingresada no valida"
    if datetime.now()>fin:
        return "Fecha ingresada no valida"
    if fin<inicio:
        return "Fecha ingresada no valida"
    return None


def actualizarEstadoReserva(idReserva):
    reserva=Reserva.query.filter_by(idReserva=idReserva).first()
    if reserva:
        if reserva.estadoRegistro != 'CER':
            if (reserva.estadoRegistro == 'PEN'):
                reserva.estadoRegistro  = 'OCU'
            elif(reserva.estadoRegistro == 'OCU'):
                reserva.estadoRegistro = 'CER'
        reserva.update()

def actualizarEstadoAuto(placa, idReserva):
    response = requests.get('http://localhost:5002/autos/'+placa)
    auto = response.json()
    reserva=Reserva.query.filter_by(idReserva=idReserva).first()
    if auto.estado != 'DIS' and reserva:
        requests.patch('http://localhost:5002/autos/'+placa, json={'estado': 'DIS'})

def actualizarEstadoEstacionamiento(idEstacionamiento, idReserva):
    response = requests.get('http://localhost:5004/estacionamiento/'+str(idEstacionamiento))
    estacionamiento = response.json()
    reserva=Reserva.query.filter_by(idReserva=idReserva).first()
    if estacionamiento.estadoRegistro != 'DIS' and reserva:
        if (estacionamiento.estadoRegistro == 'RES'):
            requests.patch('http://localhost:5004/estacionamiento/'+idEstacionamiento, json={'estadoRegistro': 'OCU'})
        elif(estacionamiento.estadoRegistro == 'OCU'):
            requests.patch('http://localhost:5004/estacionamiento/'+idEstacionamiento, json={'estadoRegistro': 'DIS'}) 