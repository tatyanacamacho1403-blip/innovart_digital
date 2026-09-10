from flask import current_app
from Models.servicio import Servicio

#listar servicios
def list_serv():
    sql = "SELECT * FROM T_SERVICIO"

    c = current_app.mysql.connection.cursor()
    c.execute(sql)

    data = c.fetchall()

    servicios_l = []

    for u in data:
        servicios_l.append(Servicio(u[0], u[1], u[2], u[3], u[4], u[5], u[6]).to_dic())

    c.close()

    return servicios_l


#añadir servicios
def add_serv(data):
    sql = "INSERT INTO T_SERVICIO (SER_ID, SER_UUID, SER_NOMBRE, SER_DESCRIPCION, SER_PRECIO, SER_TIPO, SER_ESTADO) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (data.get("id"), data.get("uuid"), data.get("nombre"), data.get("descripcion"), data.get("precio"), data.get("tipo"), data.get("estado"))

    c = current_app.mysql.connection.cursor()
    c.execute(sql, values)
    current_app.mysql.connection.commit()
    new_id = c.lastrowid
    c.close()

    return get_serv(new_id)


#actualizar servicios
def update_serv(id, data):
    sql = "UPDATE T_SERVICIO SET SER_UUID = %s, SER_NOMBRE = %s, SER_DESCRIPCION = %s, SER_PRECIO = %s, SER_TIPO = %s, SER_ESTADO = %s WHERE SER_ID = %s"
    values = (data.get("uuid"), data.get("nombre"), data.get("descripcion"), data.get("precio"), data.get("tipo"), data.get("estado"), id)

    c = current_app.mysql.connection.cursor()
    c.execute(sql, values)
    current_app.mysql.connection.commit()
    affected = c.rowcount
    c.close()

    if affected == 0:
        return None

    return get_serv(id)

#eliminar sevicios
def del_serv(id):
    sql = "DELETE FROM T_SERVICIO WHERE SER_ID = %s"

    c = current_app.mysql.connection.cursor()
    c.execute(sql, (id,))
    current_app.mysql.connection.commit()
    affected = c.rowcount
    c.close()

    return affected > 0

#buscar por id
def get_serv(id):
    sql = "SELECT * FROM T_SERVICIO WHERE SER_ID = %s"

    c = current_app.mysql.connection.cursor()
    c.execute(sql, (id,))
    u = c.fetchone()
    c.close()

    if u is None:
        return None

    return Servicio(u[0], u[1], u[2], u[3], u[4], u[5], u[6]).to_dic()
