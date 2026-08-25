from flask import current_app
from Models.servicio import Servicio


def servListServicio():

    sql = "SELECT SER_ID, SER_UUID, SER_NOMBRE, SER_DESCRIPCION, SER_PRECIO, SER_TIPO, SER_ESTADO FROM T_SERVICIO"

    c = current_app.mysql.connection.cursor()

    c.execute(sql)

    data = c.fetchall()

    servicios_l = []

    for u in data:

        servicio = Servicio(
                u[0],
                u[1],
                u[2],
                u[3],
                u[4],
                u[5],
                u[6]
        )

        servicios_l.append(servicio.to_dict())

    c.close()

    return servicios_l


def servGetServicio(id):

    sql = "SELECT SER_ID, SER_UUID, SER_NOMBRE, SER_DESCRIPCION, SER_PRECIO, SER_TIPO, SER_ESTADO FROM T_SERVICIO WHERE SER_ID = %s"

    c = current_app.mysql.connection.cursor()

    c.execute(sql, (id,))

    data = c.fetchone()

    c.close()

    if data is None:
        return None

    servicio = Servicio(
            data[0],
                data[1],
                data[2],
                data[3],
                data[4],
                data[5],
                data[6]
    )

    return servicio.to_dict()


def addServicio(data):
    sql = "INSERT INTO T_SERVICIO (SER_ID, SER_UUID, SER_NOMBRE, SER_DESCRIPCION, SER_PRECIO, SER_TIPO, SER_ESTADO) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (data.get("id"), data.get("uuid"), data.get("nombre"), data.get("descripcion"), data.get("precio"), data.get("tipo"), data.get("estado"),)

    cursor = current_app.mysql.connection.cursor()
    cursor.execute(sql, values)
    current_app.mysql.connection.commit()
    new_id = cursor.lastrowid
    cursor.close()

    # Si la tabla usa un ID autoincremental, lastrowid será el ID creado.
    # Si el ID se envía manualmente, el valor enviado se utiliza como respaldo.
    if not new_id:
        new_id = data.get("id")

    return servGetServicio(new_id)


def upServicio(id, data):
    sql = "UPDATE T_SERVICIO SET SER_UUID = %s, SER_NOMBRE = %s, SER_DESCRIPCION = %s, SER_PRECIO = %s, SER_TIPO = %s, SER_ESTADO = %s WHERE SER_ID = %s"
    values = (data.get("uuid"), data.get("nombre"), data.get("descripcion"), data.get("precio"), data.get("tipo"), data.get("estado"), id)

    cursor = current_app.mysql.connection.cursor()
    cursor.execute(sql, values)
    current_app.mysql.connection.commit()
    affected = cursor.rowcount
    cursor.close()

    if affected == 0:
        return None

    return servGetServicio(id)


def delServicio(id):
    sql = "DELETE FROM T_SERVICIO WHERE SER_ID = %s"

    cursor = current_app.mysql.connection.cursor()
    cursor.execute(sql, (id,))
    current_app.mysql.connection.commit()
    affected = cursor.rowcount
    cursor.close()

    return affected > 0
