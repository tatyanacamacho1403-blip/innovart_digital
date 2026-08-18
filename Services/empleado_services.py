# Servicio de empleado

from flask import current_app
from Models.empleado import Empleado


def servListEmpleado():
    sql = "SELECT * FROM T_EMPLEADO"

    # la siguiente linea es para ejecutar la consulta sql
    c = current_app.mysql.connection.cursor()
    c.execute(sql)

    # la siguiente linea es para obtener los resultados de la consulta sql
    data = c.fetchall()

    empleados_l = []

    for u in data:
        empleados_l.append(Empleado(u[0], u[1]).to_dic())

    # la siguiente linea es para cerrar la conexion a la base de datos
    c.close()

    return empleados_l


def addEmpleado(data):
    sql = "INSERT INTO T_EMPLEADO (EMP_ID, EMP_UUID) VALUES (%s, %s)"
    values = (data.get("id"), data.get("uuid"))

    c = current_app.mysql.connection.cursor()
    c.execute(sql, values)
    current_app.mysql.connection.commit()
    new_id = c.lastrowid
    c.close()

    return servGetEmpleado(new_id)


def upEmpleado(id, data):
    sql = "UPDATE T_EMPLEADO SET EMP_UUID = %s WHERE EMP_ID = %s"
    values = (data.get("uuid"), id)

    c = current_app.mysql.connection.cursor()
    c.execute(sql, values)
    current_app.mysql.connection.commit()
    affected = c.rowcount
    c.close()

    if affected == 0:
        return None

    return servGetEmpleado(id)


def delEmpleado(id):
    sql = "DELETE FROM T_EMPLEADO WHERE EMP_ID = %s"

    c = current_app.mysql.connection.cursor()
    c.execute(sql, (id,))
    current_app.mysql.connection.commit()
    affected = c.rowcount
    c.close()

    return affected > 0


def servGetEmpleado(id):
    sql = "SELECT * FROM T_EMPLEADO WHERE EMP_ID = %s"

    c = current_app.mysql.connection.cursor()
    c.execute(sql, (id,))
    u = c.fetchone()
    c.close()

    if u is None:
        return None

    return Empleado(u[0], u[1]).to_dic()


def searchByUuidEmpleado(uuid):
    sql = "SELECT * FROM T_EMPLEADO WHERE EMP_UUID = %s"

    c = current_app.mysql.connection.cursor()
    c.execute(sql, (uuid,))
    u = c.fetchone()
    c.close()

    if u is None:
        return None

    return Empleado(u[0], u[1]).to_dic()
