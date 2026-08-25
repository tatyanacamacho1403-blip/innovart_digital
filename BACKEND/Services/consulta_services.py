from flask import current_app
from Models.consulta import Consulta


def servListConsulta():

    sql = "SELECT CON_ID, CON_UUID, CON_HORA, CON_FECHA, CON_MENSAJE FROM T_CONSULTA"

    c = current_app.mysql.connection.cursor()

    c.execute(sql)

    data = c.fetchall()

    consultas_l = []

    for u in data:

        consulta = Consulta(
                u[0],
                u[1],
                u[2],
                u[3],
                u[4]
        )

        consultas_l.append(consulta.to_dict())

    c.close()

    return consultas_l


def servGetConsulta(id):

    sql = "SELECT CON_ID, CON_UUID, CON_HORA, CON_FECHA, CON_MENSAJE FROM T_CONSULTA WHERE CON_ID = %s"

    c = current_app.mysql.connection.cursor()

    c.execute(sql, (id,))

    data = c.fetchone()

    c.close()

    if data is None:
        return None

    consulta = Consulta(
            data[0],
                data[1],
                data[2],
                data[3],
                data[4]
    )

    return consulta.to_dict()


def addConsulta(data):
    sql = "INSERT INTO T_CONSULTA (CON_ID, CON_UUID, CON_HORA, CON_FECHA, CON_MENSAJE) VALUES (%s, %s, %s, %s, %s)"
    values = (data.get("id"), data.get("uuid"), data.get("hora"), data.get("fecha"), data.get("mensaje"),)

    cursor = current_app.mysql.connection.cursor()
    cursor.execute(sql, values)
    current_app.mysql.connection.commit()
    new_id = cursor.lastrowid
    cursor.close()

    # Si la tabla usa un ID autoincremental, lastrowid será el ID creado.
    # Si el ID se envía manualmente, el valor enviado se utiliza como respaldo.
    if not new_id:
        new_id = data.get("id")

    return servGetConsulta(new_id)


def upConsulta(id, data):
    sql = "UPDATE T_CONSULTA SET CON_UUID = %s, CON_HORA = %s, CON_FECHA = %s, CON_MENSAJE = %s WHERE CON_ID = %s"
    values = (data.get("uuid"), data.get("hora"), data.get("fecha"), data.get("mensaje"), id)

    cursor = current_app.mysql.connection.cursor()
    cursor.execute(sql, values)
    current_app.mysql.connection.commit()
    affected = cursor.rowcount
    cursor.close()

    if affected == 0:
        return None

    return servGetConsulta(id)


def delConsulta(id):
    sql = "DELETE FROM T_CONSULTA WHERE CON_ID = %s"

    cursor = current_app.mysql.connection.cursor()
    cursor.execute(sql, (id,))
    current_app.mysql.connection.commit()
    affected = cursor.rowcount
    cursor.close()

    return affected > 0
