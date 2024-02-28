import re
from werkzeug.security import generate_password_hash, check_password_hash
from models import Usuario, db

def isemail(email):
    expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    return re.match(expresion_regular, email)
def v_celular(celular):
    if not celular:
        return "Envie un numero de celular"
    if not celular.isdigit():
        return "El numero de celular debe ser numerico"
    if len(celular) != 9:
        return "El numero de celular debe tener 9 digitos"
    if Usuario.query.filter_by(celular=celular).first() is not None:
        return "El numero de celular ya existe"
    return None

def v_dni(dni):
    if not dni:
        return "Envie un DNI"
    if not dni.isdigit():
        return "El DNI debe ser numerico"
    if len(dni) != 8:
        return "El DNI debe tener 8 digitos"
    if Usuario.query.filter_by(dni=dni).first() is not None:
        return "El DNI ya existe"
    return None

def v_nombre(nombre):
    if not nombre:
        return "Envie un nombre"
    if not nombre.isalpha():
        return "El nombre debe ser solo letras"
    if len(nombre) < 3 or len(nombre) > 50:
        return "El nombre debe tener entre 3 y 50 caracteres"
    return None

def v_correo(correo, get_user=False):
    if not correo:
        return "Envie un correo"
    if not isemail(correo):
        return "El correo debe ser valido"
    if len(correo) < 5 or len(correo) > 50:
        return "El correo debe tener entre 5 y 50 caracteres"
    if not get_user and Usuario.query.filter_by(correo=correo).first() is not None:
        return "El correo ya existe"
    
    return None

def v_login(correo, contrasena):
    user = Usuario.query.filter_by(correo=correo).one_or_none()
    if user is None:
        return {'success': False, 'message': "El correo no existe"}
    if not check_password_hash(user.contrasena, contrasena):
        return {'success': False, 'message': "Contraseña incorrecta"}
    return {'success': True, 'user': user}

def v_contrasena(contrasena, get_user=False):
    if not contrasena:
        return "Envie una contraseña"
    if get_user:
        return None
    if not re.search("[a-z]", contrasena):
        return "No hay minusculas en tu contraseña."
    if not re.search("[A-Z]", contrasena):
        return "No hay mayusculas en tu contraseña."
    if not re.search("[0-9]", contrasena):
        return "No hay numeros en tu contraseña."
    if not re.search("[?=.*[@#$%^&-+=()_]", contrasena):
        return "No hay caracteres especiales en tu contraseña."
    if re.search("\\s", contrasena):
        return "No se permiten espacios en la contraseña."
    if len(contrasena) < 5 or len(contrasena) > 20:
        return "La contraseña debe tener entre 5 y 20 caracteres."
    return None

def crear_persona():
    testPersona=Usuario("75330321", "985013664", "Marco Antonio", "a@a.com", generate_password_hash("1234"), "REG")
    db.session.add(testPersona)
    db.session.commit()
