from flask import current_app
from Models.pago import Pago


def servListPago():

    sql = "SELECT PAG_ID, PAG_UUID, PAG_HORA, PAG_FECHA, PAG_MONTO, PAG_METODO_PAGO, PAG_USU_ID, PAG_AGE_ID, PAG_SER_ID FROM T_PAGO"

    c = current_app.mysql.connection.cursor()

    c.execute(sql)

    data = c.fetchall()

    pagos_l = []

    for u in data:

        pago = Pago(
                u[0],
                u[1],
                u[2],
                u[3],
                u[4],
                u[5],
                u[6],
                u[7],
                u[8]
        )

        pagos_l.append(pago.to_dict())

    c.close()

    return pagos_l


def servGetPago(id):

    sql = "SELECT PAG_ID, PAG_UUID, PAG_HORA, PAG_FECHA, PAG_MONTO, PAG_METODO_PAGO, PAG_USU_ID, PAG_AGE_ID, PAG_SER_ID FROM T_PAGO WHERE PAG_ID = %s"

    c = current_app.mysql.connection.cursor()

    c.execute(sql, (id,))

    data = c.fetchone()

    c.close()

    if data is None:
        return None

    pago = Pago(
            data[0],
                data[1],
                data[2],
                data[3],
                data[4],
                data[5],
                data[6],
                data[7],
                data[8]
    )

    return pago.to_dict()


def addPago(data):
    sql = "INSERT INTO T_PAGO (PAG_ID, PAG_UUID, PAG_HORA, PAG_FECHA, PAG_MONTO, PAG_METODO_PAGO, PAG_USU_ID, PAG_AGE_ID, PAG_SER_ID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (data.get("id"), data.get("uuid"), data.get("hora"), data.get("fecha"), data.get("monto"), data.get("metodo_pago"), data.get("usu_id"), data.get("age_id"), data.get("ser_id"),)

    cursor = current_app.mysql.connection.cursor()
    cursor.execute(sql, values)
    current_app.mysql.connection.commit()
    new_id = cursor.lastrowid
    cursor.close()

    # Si la tabla usa un ID autoincremental, lastrowid será el ID creado.
    # Si el ID se envía manualmente, el valor enviado se utiliza como respaldo.
    if not new_id:
        new_id = data.get("id")

    return servGetPago(new_id)


def upPago(id, data):
    sql = "UPDATE T_PAGO SET PAG_UUID = %s, PAG_HORA = %s, PAG_FECHA = %s, PAG_MONTO = %s, PAG_METODO_PAGO = %s, PAG_USU_ID = %s, PAG_AGE_ID = %s, PAG_SER_ID = %s WHERE PAG_ID = %s"
    values = (data.get("uuid"), data.get("hora"), data.get("fecha"), data.get("monto"), data.get("metodo_pago"), data.get("usu_id"), data.get("age_id"), data.get("ser_id"), id)

    cursor = current_app.mysql.connection.cursor()
    cursor.execute(sql, values)
    current_app.mysql.connection.commit()
    affected = cursor.rowcount
    cursor.close()

    if affected == 0:
        return None

    return servGetPago(id)


def delPago(id):
    sql = "DELETE FROM T_PAGO WHERE PAG_ID = %s"

    cursor = current_app.mysql.connection.cursor()
    cursor.execute(sql, (id,))
    current_app.mysql.connection.commit()
    affected = cursor.rowcount
    cursor.close()

    return affected > 0
