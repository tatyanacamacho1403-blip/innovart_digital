from flask import current_app
from Models.respuesta import Respuesta


def servListRespuesta():

    sql = "SELECT RES_ID, RES_UUID, RES_HORA, RES_DESCRIPCION, RES_FECHA FROM t_respusta"

    c = current_app.mysql.connection.cursor()
    c.execute(sql)

    data = c.fetchall()

    lista_l = []

    for u in data:

        objeto = Respuesta(
                u[0],
                u[1],
                u[2],
                u[3],
                u[4]
        )

        lista_l.append(objeto.to_dict())

    c.close()

    return lista_l


def servGetRespuesta(id):

    sql = "SELECT RES_ID, RES_UUID, RES_HORA, RES_DESCRIPCION, RES_FECHA FROM t_respusta WHERE RES_ID = %s"

    c = current_app.mysql.connection.cursor()
    c.execute(sql, (id,))

    data = c.fetchone()

    c.close()

    if data is None:
        return None

    objeto = Respuesta(
            data[0],
            data[1],
            data[2],
            data[3],
            data[4]
    )

    return objeto.to_dict()


def addRespuesta(data):

    sql = "INSERT INTO t_respusta (RES_UUID, RES_HORA, RES_DESCRIPCION, RES_FECHA) VALUES (%s, %s, %s, %s)"

    values = (
        data.get('uuid'),
        data.get('hora'),
        data.get('descripcion'),
        data.get('fecha')
    )

    c = current_app.mysql.connection.cursor()
    c.execute(sql, values)
    current_app.mysql.connection.commit()

    new_id = c.lastrowid

    c.close()

    return servGetRespuesta(new_id)


def upRespuesta(id, data):

    sql = "UPDATE t_respusta SET RES_UUID = %s, RES_HORA = %s, RES_DESCRIPCION = %s, RES_FECHA = %s WHERE RES_ID = %s"

    values = (
        data.get('uuid'),
        data.get('hora'),
        data.get('descripcion'),
        data.get('fecha'),
        id
    )

    c = current_app.mysql.connection.cursor()
    c.execute(sql, values)
    current_app.mysql.connection.commit()

    affected = c.rowcount

    c.close()

    if affected == 0:
        return None

    return servGetRespuesta(id)


def delRespuesta(id):

    sql = "DELETE FROM t_respusta WHERE RES_ID = %s"

    c = current_app.mysql.connection.cursor()
    c.execute(sql, (id,))
    current_app.mysql.connection.commit()

    affected = c.rowcount

    c.close()

    return affected > 0
