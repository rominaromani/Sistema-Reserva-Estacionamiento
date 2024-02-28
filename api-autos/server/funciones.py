from models import Auto

def v_placa(placa):
    if not placa:
        return "Envie una placa"
    if len(placa) > 6:
        return "La placa no debe exceder los 6 digitos"
    if Auto.query.filter_by(placa=placa).first() is not None:
        return "El vehiculo ya existe"
    return None

def v_marca(marca):
    if not marca:
        return "Envie una marca"
    return None

def v_modelo(modelo):
    if not modelo:
        return "Envie un modelo"
    return None

def v_color(color):
    if not color:
        return "Envie un color"
    return None

def actualizarEstadoAuto(placa):
    auto=Auto.query.filter_by(placa=placa).first()
    if auto.estado != 'DIS' :
        auto.estado='DIS'
    auto.update()