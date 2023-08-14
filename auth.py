import jwt
from fastapi import HTTPException, Depends, FastAPI, Request, Body, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from database import database

SECRET_KEY = "##_patria_fhkjndkjabsjbdlaknlksndlnsd_ccp1912_tomas_kasbdjk"  # Clave secreta

security = HTTPBearer()
router = APIRouter()


class UsuarioCredenciales(BaseModel):
    username: str
    password: str


def generar_token(usuario_id):
    payload = {
        'usuario_id': usuario_id,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token


def verificar_credenciales(username, password):
    con = database.get_database_connection()  # Obtén una conexión a la base de datos
    cursor = con.cursor()

    username = encriptar(username, 1)
    password = encriptar(password, 2)

    query = f"SELECT usuario_desenc FROM fpasword WHERE usuario = ? AND clave = ?"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    con.close()
    return result is not None if result else False

def verificar_credenciales_web(username, password):
    con = database.get_database_connection_web()  # Obtén una conexión a la base de datos
    cursor = con.cursor()

    username = encriptar(username, 1)
    password = encriptar(password, 2)

    query = f"SELECT usuario FROM f_permitidos WHERE usuario = ? AND clave = ?"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    con.close()
    return result is not None if result else False


def verificar_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['usuario_id']
    except jwt.ExpiredSignatureError:
        return None  # Token expirado
    except jwt.InvalidTokenError:
        return None  # Token inválido


def encriptar(pass_str, tipo):
    pass_str = pass_str.upper().strip()
    if tipo == 1:
        go = 25
    elif tipo == 2:
        go = 22
    final = ""
    lon = len(pass_str)
    for i in range(1, lon + 1):
        L = pass_str[i - 1]
        L = chr(ord(L) + go + i)
        final += L
    return final


def desencriptar(pass_str, tipo):
    if tipo == 1:
        go = 25
    elif tipo == 2:
        go = 22
    final = ""
    lon = len(pass_str)
    for i in range(1, lon + 1):
        L = pass_str[i - 1]
        L = chr(ord(L) - go - i)
        final += L
    return final


@router.get('/login')
def login(credentials: UsuarioCredenciales = Body(...)):
    username = credentials.username
    password = credentials.password

    if not username or not password:
        raise HTTPException(status_code=400, detail='Nombre de usuario y contraseña requeridos')

    if verificar_credenciales(username, password):
        token = generar_token(username)  # O utiliza el ID de usuario en su lugar
        return {'token': token}
    else:
        raise HTTPException(status_code=401, detail='Credenciales inválidas')

@router.get('/access')
def login(credentials: UsuarioCredenciales = Body(...)):
    username = credentials.username
    password = credentials.password

    if not username or not password:
        raise HTTPException(status_code=400, detail='Nombre de usuario y contraseña requeridos')

    if verificar_credenciales_web(username, password):
        token = generar_token(username)  # O utiliza el ID de usuario en su lugar
        return {'token': token}
    else:
        raise HTTPException(status_code=401, detail='Credenciales inválidas')


@router.get('/secure')
def secure_route(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    usuario_id = verificar_token(token)
    if usuario_id:
        return {'message': 'Acceso permitido'}
    else:
        raise HTTPException(status_code=401, detail='Acceso denegado')

# Agrega más rutas seguras según sea necesario
