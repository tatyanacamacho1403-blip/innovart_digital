from flask import current_app
from Models.usuario import Usuario


def servListUsuario():

    sql = "SELECT USU_ID, USU_UUID, USU_CORREO, USU_CONTRASEÑA, USU_PER_ID FROM t_usuario"

    c = current_app.mysql.connection.cursor()
    c.execute(sql)

    data = c.fetchall()

    lista_l = []

    for u in data:

        objeto = Usuario(
                u[0],
                u[1],
                u[2],
                u[3],
                u[4]
        )

        lista_l.append(objeto.to_dict())

    c.close()

    return lista_l


def servGetUsuario(id):

    sql = "SELECT USU_ID, USU_UUID, USU_CORREO, USU_CONTRASEÑA, USU_PER_ID FROM t_usuario WHERE USU_ID = %s"

    c = current_app.mysql.connection.cursor()
    c.execute(sql, (id,))

    data = c.fetchone()

    c.close()

    if data is None:
        return None

    objeto = Usuario(
            data[0],
            data[1],
            data[2],
            data[3],
            data[4]
    )

    return objeto.to_dict()


def addUsuario(data):

    sql = "INSERT INTO t_usuario (USU_UUID, USU_CORREO, USU_CONTRASEÑA, USU_PER_ID) VALUES (%s, %s, %s, %s)"

    values = (data.get('uuid'), data.get('correo'), data.get('contrasena'), data.get('per_id'),)

    c = current_app.mysql.connection.cursor()
    c.execute(sql, values)
    current_app.mysql.connection.commit()

    new_id = c.lastrowid

    c.close()

    return servGetUsuario(new_id)


def upUsuario(id, data):

    sql = "UPDATE t_usuario SET USU_UUID = %s, USU_CORREO = %s, USU_CONTRASEÑA = %s, USU_PER_ID = %s WHERE USU_ID = %s"

    values = (data.get('uuid'), data.get('correo'), data.get('contrasena'), data.get('per_id'), id)

    c = current_app.mysql.connection.cursor()
    c.execute(sql, values)
    current_app.mysql.connection.commit()

    affected = c.rowcount

    c.close()

    if affected == 0:
        return None

    return servGetUsuario(id)


def delUsuario(id):

    sql = "DELETE FROM t_usuario WHERE USU_ID = %s"

    c = current_app.mysql.connection.cursor()
    c.execute(sql, (id,))
    current_app.mysql.connection.commit()

    affected = c.rowcount

    c.close()

    return affected > 0
