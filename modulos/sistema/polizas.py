from fastapi import APIRouter, Depends, HTTPException, Header
from database.database import get_database_connection
from utils import response
from auth import verificar_token

router = APIRouter()
con = get_database_connection()


@router.get('/{id_poliza}')
def obtener_poliza(id_poliza: str, authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    usuario_id = verificar_token(token)

    if usuario_id is None:
        raise HTTPException(status_code=401, detail='Acceso denegado')

    claves = id_poliza.split('_')
    v_emitido, v_seccion, v_poliza, v_endoso = claves

    query = f"SELECT emitido, seccion, poliza, endoso, asegurado FROM fpol WHERE emitido = '{v_emitido}' AND seccion = '{v_seccion}' AND poliza = '{v_poliza}' AND endoso = '{v_endoso}'"

    cursor = con.cursor()
    cursor.execute(query)
    poliza_row = cursor.fetchonemap()

    if poliza_row:
        poliza_dict = dict(poliza_row.items())
        return response(200, 'Poliza encontrada', poliza_dict)
    else:
        raise HTTPException(status_code=404, detail='Poliza no encontrada')


@router.get('/asegurado/{id_asegurado}')
def obtener_polizas_por_asegurado(id_asegurado: str, authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    usuario_id = verificar_token(token)

    if usuario_id is None:
        raise HTTPException(status_code=401, detail='Acceso denegado')

    query = f"SELECT emitido, seccion, poliza, endoso, asegurado FROM fpol WHERE asegurado = '{id_asegurado}'"

    cursor = con.cursor()
    cursor.execute(query)
    poliza_rows = cursor.fetchallmap()

    polizas_list = []  # Lista para almacenar las polizas en forma de diccionarios

    for poliza_row in poliza_rows:
        poliza_dict = dict(poliza_row.items())
        polizas_list.append(poliza_dict)

    if polizas_list:
        return response(200, 'Polizas encontradas', polizas_list)
    else:
        raise HTTPException(status_code=404, detail='Polizas no encontradas')


@router.get('/asegurado/{id_asegurado}/poliza/{id_poliza}')
def obtener_poliza_por_asegurado(id_asegurado: str, id_poliza: str, authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    usuario_id = verificar_token(token)

    if usuario_id is None:
        raise HTTPException(status_code=401, detail='Acceso denegado')

    claves = id_poliza.split('_')
    v_emitido, v_seccion, v_poliza, v_endoso = claves

    query = f"SELECT emitido, seccion, poliza, endoso, asegurado FROM fpol WHERE asegurado = '{id_asegurado}' AND emitido = '{v_emitido}' AND seccion = '{v_seccion}' AND poliza = '{v_poliza}' AND endoso = '{v_endoso}'"

    cursor = con.cursor()
    cursor.execute(query)
    poliza_row = cursor.fetchonemap()

    if poliza_row:
        poliza_dict = dict(poliza_row.items())
        return response(200, 'Poliza encontrada', poliza_dict)
    else:
        raise HTTPException(status_code=404, detail='Poliza no encontrada')
