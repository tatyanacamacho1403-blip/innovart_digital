from flask import current_app
from Models.usuario import Usuario


def servListUsuario():
    sql = "SELECT * FROM T_USUARIO"

    c = current_app.mysql.connection.cursor()
    c.execute(sql)

    data = c.fetchall()

    usuarios_l = []

    for u in data:
        usuarios_l.append(Usuario(u[0], u[1], u[2], u[3]).to_dic())

    c.close()

    return usuarios_l


def servAddUsuario(data):
    sql = "INSERT INTO T_USUARIO (USU_ID, USU_UUID, USU_CONTRASENA, USU_PER_ID) VALUES (%s, %s, %s, %s)"
    values = (data.get("id"), data.get("uuid"), data.get("contrasena"), data.get("per_id"))

    c = current_app.mysql.connection.cursor()
    c.execute(sql, values)
    current_app.mysql.connection.commit()
    new_id = c.lastrowid
    c.close()

    return servGetUsuario(new_id)


def servUpUsuario(id, data):
    sql = "UPDATE T_USUARIO SET USU_UUID = %s, USU_CONTRASENA = %s, USU_PER_ID = %s WHERE USU_ID = %s"
    values = (data.get("uuid"), data.get("contrasena"), data.get("per_id"), id)

    c = current_app.mysql.connection.cursor()
    c.execute(sql, values)
    current_app.mysql.connection.commit()
    affected = c.rowcount
    c.close()

    if affected == 0:
        return None

    return servGetUsuario(id)


def servDelUsuario(id):
    sql = "DELETE FROM T_USUARIO WHERE USU_ID = %s"

    c = current_app.mysql.connection.cursor()
    c.execute(sql, (id,))
    current_app.mysql.connection.commit()
    affected = c.rowcount
    c.close()

    return affected > 0


def servGetUsuario(id):
    sql = "SELECT * FROM T_USUARIO WHERE USU_ID = %s"

    c = current_app.mysql.connection.cursor()
    c.execute(sql, (id,))
    u = c.fetchone()
    c.close()

    if u is None:
        return None

    return Usuario(u[0], u[1], u[2], u[3]).to_dic()