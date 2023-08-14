from fastapi import APIRouter, HTTPException, Header
from database.database import *
from utils import response
from auth import verificar_token
import json

router = APIRouter()
con_web = get_database_connection_web()


@router.get('/datos/{parametros}')
def obtener_datos_asegurado(parametros: str, authorization: str = Header(...)):
    """
    ## Obtener legajo de un asegurado por documento.

    ### Parametros
    - `parametros:` Parametros para obtener los datos. Se divide en cuatro (Ej.: CID_5134154_0):
     -- tipo_documento (CID, RUC, ODO),
     -- documento,
     -- tarea (0 - obtiene las polizas vigentes y no vigentes, opcion filtro seccion
           1 - obtene las denuncias, opcion filtro seccion
           2 - obtiene todas las polizas agrupadas
           3 - obtiene todas las DENUNCIAS agrupadas),
     -- seccion (opcional)
    - `authorization:` Token de autorización (Bearer token).
    """

    token = authorization.replace("Bearer ", "")
    usuario_id = verificar_token(token)

    if usuario_id is None:
        raise HTTPException(status_code=401, detail='Acceso denegado')

    claves = parametros.split('_')
    v_tipo, v_documento, v_tarea, v_seccion = claves

    query = f"SELECT * FROM WS_GET_LEGAJOS_ASEGURADO('{v_tipo}', '{v_documento}', '{v_tarea}','{v_seccion}')"

    cursor = con_web.cursor()
    cursor.execute(query)
    datos_asegurado_rows = cursor.fetchallmap()

    datos_asegurados_list = []  # Lista para almacenar los asegurados en forma de diccionarios

    for datos_asegurado_row in datos_asegurado_rows:
        datos_asegurado_dict = dict(datos_asegurado_row.items())

        # Deserializar el valor en "O_DATA" como JSON
        o_data = datos_asegurado_dict.get("O_DATA")
        if o_data:
            datos_asegurado_dict["O_DATA"] = json.loads(o_data)

        datos_asegurados_list.append(datos_asegurado_dict)

    if datos_asegurados_list:
        return response(200, 'Datos del asegurado encontrados', datos_asegurados_list)
    else:
        raise HTTPException(status_code=404, detail='No se encontraron datos del asegurado')
