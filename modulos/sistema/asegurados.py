from fastapi import APIRouter, Depends, HTTPException, Header
from database.database import *
from utils import response
from auth import verificar_token

router = APIRouter()
con = get_database_connection()

@router.get('/')
def obtener_asegurados(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    usuario_id = verificar_token(token)

    if usuario_id is None:
        raise HTTPException(status_code=401, detail='Acceso denegado')

    cursor = con.cursor()
    cursor.execute('SELECT * FROM fcodgeneral')
    asegurados_rows = cursor.fetchallmap()

    asegurados_list = []  # Lista para almacenar los asegurados en forma de diccionarios

    for asegurado_row in asegurados_rows:
        asegurado_dict = dict(asegurado_row.items())
        asegurados_list.append(asegurado_dict)

    if asegurados_list:
        return response(200, 'Asegurados encontrados', asegurados_list)
    else:
        raise HTTPException(status_code=404, detail='No se encontraron asegurados')


@router.get('/{id}')
def obtener_asegurado(id: str, authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    usuario_id = verificar_token(token)

    if usuario_id is None:
        raise HTTPException(status_code=401, detail='Acceso denegado')

    query = f"SELECT nombre, tipo_documento, ruc, cedula, otro_documento FROM fcodgeneral WHERE codigo = '{id}'"

    cursor = con.cursor()
    cursor.execute(query)
    asegurado_row = cursor.fetchonemap()

    if asegurado_row:
        asegurado_dict = dict(asegurado_row.items())
        return response(200, 'Asegurado encontrado', asegurado_dict)
    else:
        raise HTTPException(status_code=404, detail='Asegurado no encontrado')


@router.get('/documento/{tipo_documento}')
def obtener_asegurado_por_doc(tipo_documento: str, authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    usuario_id = verificar_token(token)

    if usuario_id is None:
        raise HTTPException(status_code=401, detail='Acceso denegado')

    claves = tipo_documento.split('_')
    v_tipo, v_documento = claves

    if v_tipo.strip() == "CI":
        v_where = "cedula"
    elif v_tipo.strip() == "RUC":
        v_where = "ruc"
    else:
        v_where = "otro_documento"

    query = f"SELECT nombre, tipo_documento, ruc, cedula, otro_documento FROM fcodgeneral WHERE tipo_documento = '{v_tipo}' AND {v_where} = '{v_documento}'"

    cursor = con.cursor()
    cursor.execute(query)
    asegurado_row = cursor.fetchonemap()

    if asegurado_row:
        asegurado_dict = dict(asegurado_row.items())
        return response(200, 'Asegurado encontrado', asegurado_dict)
    else:
        raise HTTPException(status_code=404, detail='Asegurado no encontrado')
