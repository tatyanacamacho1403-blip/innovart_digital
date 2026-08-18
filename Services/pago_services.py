# Servicio de pago

from flask import current_app
from Models.pago import Pago


def servListPago():
    sql = "SELECT * FROM T_PAGO"

    # la siguiente linea es para ejecutar la consulta sql
    c = current_app.mysql.connection.cursor()
    c.execute(sql)

    # la siguiente linea es para obtener los resultados de la consulta sql
    data = c.fetchall()

    pagos_l = []

    for u in data:
        pagos_l.append(Pago(u[0], u[1], u[2], u[3], u[4], u[5], u[6], u[7], u[8]).to_dic())

    # la siguiente linea es para cerrar la conexion a la base de datos
    c.close()

    return pagos_l


def addPago(data):
    sql = "INSERT INTO T_PAGO (PAG_ID, PAG_UUID, PAG_HORA, PAG_FECHA, PAG_MONTO, PAG_METODO_PAGO, PAG_USU_ID, PAG_AGE_ID, PAG_SER_ID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (data.get("id"), data.get("uuid"), data.get("hora"), data.get("fecha"), data.get("monto"), data.get("metodo_pago"), data.get("usu_id"), data.get("age_id"), data.get("ser_id"))

    c = current_app.mysql.connection.cursor()
    c.execute(sql, values)
    current_app.mysql.connection.commit()
    new_id = c.lastrowid
    c.close()

    return servGetPago(new_id)


def upPago(id, data):
    sql = "UPDATE T_PAGO SET PAG_UUID = %s, PAG_HORA = %s, PAG_FECHA = %s, PAG_MONTO = %s, PAG_METODO_PAGO = %s, PAG_USU_ID = %s, PAG_AGE_ID = %s, PAG_SER_ID = %s WHERE PAG_ID = %s"
    values = (data.get("uuid"), data.get("hora"), data.get("fecha"), data.get("monto"), data.get("metodo_pago"), data.get("usu_id"), data.get("age_id"), data.get("ser_id"), id)

    c = current_app.mysql.connection.cursor()
    c.execute(sql, values)
    current_app.mysql.connection.commit()
    affected = c.rowcount
    c.close()

    if affected == 0:
        return None

    return servGetPago(id)


def delPago(id):
    sql = "DELETE FROM T_PAGO WHERE PAG_ID = %s"

    c = current_app.mysql.connection.cursor()
    c.execute(sql, (id,))
    current_app.mysql.connection.commit()
    affected = c.rowcount
    c.close()

    return affected > 0


def servGetPago(id):
    sql = "SELECT * FROM T_PAGO WHERE PAG_ID = %s"

    c = current_app.mysql.connection.cursor()
    c.execute(sql, (id,))
    u = c.fetchone()
    c.close()

    if u is None:
        return None

    return Pago(u[0], u[1], u[2], u[3], u[4], u[5], u[6], u[7], u[8]).to_dic()


def searchByUuidPago(uuid):
    sql = "SELECT * FROM T_PAGO WHERE PAG_UUID = %s"

    c = current_app.mysql.connection.cursor()
    c.execute(sql, (uuid,))
    u = c.fetchone()
    c.close()

    if u is None:
        return None

    return Pago(u[0], u[1], u[2], u[3], u[4], u[5], u[6], u[7], u[8]).to_dic()
