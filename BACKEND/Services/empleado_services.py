from flask import current_app
from Models.empleado import Empleado


def servListEmpleado():

    sql = "SELECT EMP_ID, EMP_UUID FROM T_EMPLEADO"

    c = current_app.mysql.connection.cursor()

    c.execute(sql)

    data = c.fetchall()

    empleados_l = []

    for u in data:

        empleado = Empleado(
                u[0],
                u[1]
        )

        empleados_l.append(empleado.to_dict())

    c.close()

    return empleados_l


def servGetEmpleado(id):

    sql = "SELECT EMP_ID, EMP_UUID FROM T_EMPLEADO WHERE EMP_ID = %s"

    c = current_app.mysql.connection.cursor()

    c.execute(sql, (id,))

    data = c.fetchone()

    c.close()

    if data is None:
        return None

    empleado = Empleado(
            data[0],
                data[1]
    )

    return empleado.to_dict()


def addEmpleado(data):
    sql = "INSERT INTO T_EMPLEADO (EMP_ID, EMP_UUID) VALUES (%s, %s)"
    values = (data.get("id"), data.get("uuid"),)

    cursor = current_app.mysql.connection.cursor()
    cursor.execute(sql, values)
    current_app.mysql.connection.commit()
    new_id = cursor.lastrowid
    cursor.close()

    # Si la tabla usa un ID autoincremental, lastrowid será el ID creado.
    # Si el ID se envía manualmente, el valor enviado se utiliza como respaldo.
    if not new_id:
        new_id = data.get("id")

    return servGetEmpleado(new_id)


def upEmpleado(id, data):
    sql = "UPDATE T_EMPLEADO SET EMP_UUID = %s WHERE EMP_ID = %s"
    values = (data.get("uuid"), id)

    cursor = current_app.mysql.connection.cursor()
    cursor.execute(sql, values)
    current_app.mysql.connection.commit()
    affected = cursor.rowcount
    cursor.close()

    if affected == 0:
        return None

    return servGetEmpleado(id)


def delEmpleado(id):
    sql = "DELETE FROM T_EMPLEADO WHERE EMP_ID = %s"

    cursor = current_app.mysql.connection.cursor()
    cursor.execute(sql, (id,))
    current_app.mysql.connection.commit()
    affected = cursor.rowcount
    cursor.close()

    return affected > 0
