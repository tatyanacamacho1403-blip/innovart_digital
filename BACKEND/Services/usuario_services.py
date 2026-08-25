from flask import current_app
from Models.usuario import Usuario


def servListUsuario():

    sql = "SELECT USU_ID, USU_UUID, USU_CONTRASENA, USU_PER_ID FROM T_USUARIO"

    c = current_app.mysql.connection.cursor()

    c.execute(sql)

    data = c.fetchall()

    usuarios_l = []

    for u in data:

        usuario = Usuario(
                u[0],
                u[1],
                u[2],
                u[3]
        )

        usuarios_l.append(usuario.to_dict())

    c.close()

    return usuarios_l


def servGetUsuario(id):

    sql = "SELECT USU_ID, USU_UUID, USU_CONTRASENA, USU_PER_ID FROM T_USUARIO WHERE USU_ID = %s"

    c = current_app.mysql.connection.cursor()

    c.execute(sql, (id,))

    data = c.fetchone()

    c.close()

    if data is None:
        return None

    usuario = Usuario(
            data[0],
                data[1],
                data[2],
                data[3]
    )

    return usuario.to_dict()


def addUsuario(data):
    sql = "INSERT INTO T_USUARIO (USU_ID, USU_UUID, USU_CONTRASENA, USU_PER_ID) VALUES (%s, %s, %s, %s)"
    values = (data.get("id"), data.get("uuid"), data.get("contrasena"), data.get("per_id"),)

    cursor = current_app.mysql.connection.cursor()
    cursor.execute(sql, values)
    current_app.mysql.connection.commit()
    new_id = cursor.lastrowid
    cursor.close()

    # Si la tabla usa un ID autoincremental, lastrowid será el ID creado.
    # Si el ID se envía manualmente, el valor enviado se utiliza como respaldo.
    if not new_id:
        new_id = data.get("id")

    return servGetUsuario(new_id)


def upUsuario(id, data):
    sql = "UPDATE T_USUARIO SET USU_UUID = %s, USU_CONTRASENA = %s, USU_PER_ID = %s WHERE USU_ID = %s"
    values = (data.get("uuid"), data.get("contrasena"), data.get("per_id"), id)

    cursor = current_app.mysql.connection.cursor()
    cursor.execute(sql, values)
    current_app.mysql.connection.commit()
    affected = cursor.rowcount
    cursor.close()

    if affected == 0:
        return None

    return servGetUsuario(id)


def delUsuario(id):
    sql = "DELETE FROM T_USUARIO WHERE USU_ID = %s"

    cursor = current_app.mysql.connection.cursor()
    cursor.execute(sql, (id,))
    current_app.mysql.connection.commit()
    affected = cursor.rowcount
    cursor.close()

    return affected > 0
