from flask import current_app
from Models.persona import Persona


def servListPersona():

    sql = "SELECT PER_ID, PER_UUID, PER_CEDULA, PER_DOCUMENTO, PER_PRIMER_NOMBRE, PER_SEGUNDO_NOMBRE, PER_PRIMER_APELLIDO, PER_SEGUNDO_APELLIDO, PER_FECHA_NACIMIENTO, PER_DIRECCION, PER_TELEFONO, PER_CORREO_ELECTRONICO FROM T_PERSONA"

    c = current_app.mysql.connection.cursor()

    c.execute(sql)

    data = c.fetchall()

    personas_l = []

    for u in data:

        persona = Persona(
                u[0],
                u[1],
                u[2],
                u[3],
                u[4],
                u[5],
                u[6],
                u[7],
                u[8],
                u[9],
                u[10],
                u[11]
        )

        personas_l.append(persona.to_dict())

    c.close()

    return personas_l


def servGetPersona(id):

    sql = "SELECT PER_ID, PER_UUID, PER_CEDULA, PER_DOCUMENTO, PER_PRIMER_NOMBRE, PER_SEGUNDO_NOMBRE, PER_PRIMER_APELLIDO, PER_SEGUNDO_APELLIDO, PER_FECHA_NACIMIENTO, PER_DIRECCION, PER_TELEFONO, PER_CORREO_ELECTRONICO FROM T_PERSONA WHERE PER_ID = %s"

    c = current_app.mysql.connection.cursor()

    c.execute(sql, (id,))

    data = c.fetchone()

    c.close()

    if data is None:
        return None

    persona = Persona(
            data[0],
                data[1],
                data[2],
                data[3],
                data[4],
                data[5],
                data[6],
                data[7],
                data[8],
                data[9],
                data[10],
                data[11]
    )

    return persona.to_dict()


def addPersona(data):
    sql = "INSERT INTO T_PERSONA (PER_ID, PER_UUID, PER_CEDULA, PER_DOCUMENTO, PER_PRIMER_NOMBRE, PER_SEGUNDO_NOMBRE, PER_PRIMER_APELLIDO, PER_SEGUNDO_APELLIDO, PER_FECHA_NACIMIENTO, PER_DIRECCION, PER_TELEFONO, PER_CORREO_ELECTRONICO) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (data.get("id"), data.get("uuid"), data.get("cedula"), data.get("documento"), data.get("primer_nombre"), data.get("segundo_nombre"), data.get("primer_apellido"), data.get("segundo_apellido"), data.get("fecha_nacimiento"), data.get("direccion"), data.get("telefono"), data.get("correo_electronico"),)

    cursor = current_app.mysql.connection.cursor()
    cursor.execute(sql, values)
    current_app.mysql.connection.commit()
    new_id = cursor.lastrowid
    cursor.close()

    # Si la tabla usa un ID autoincremental, lastrowid será el ID creado.
    # Si el ID se envía manualmente, el valor enviado se utiliza como respaldo.
    if not new_id:
        new_id = data.get("id")

    return servGetPersona(new_id)


def upPersona(id, data):
    sql = "UPDATE T_PERSONA SET PER_UUID = %s, PER_CEDULA = %s, PER_DOCUMENTO = %s, PER_PRIMER_NOMBRE = %s, PER_SEGUNDO_NOMBRE = %s, PER_PRIMER_APELLIDO = %s, PER_SEGUNDO_APELLIDO = %s, PER_FECHA_NACIMIENTO = %s, PER_DIRECCION = %s, PER_TELEFONO = %s, PER_CORREO_ELECTRONICO = %s WHERE PER_ID = %s"
    values = (data.get("uuid"), data.get("cedula"), data.get("documento"), data.get("primer_nombre"), data.get("segundo_nombre"), data.get("primer_apellido"), data.get("segundo_apellido"), data.get("fecha_nacimiento"), data.get("direccion"), data.get("telefono"), data.get("correo_electronico"), id)

    cursor = current_app.mysql.connection.cursor()
    cursor.execute(sql, values)
    current_app.mysql.connection.commit()
    affected = cursor.rowcount
    cursor.close()

    if affected == 0:
        return None

    return servGetPersona(id)


def delPersona(id):
    sql = "DELETE FROM T_PERSONA WHERE PER_ID = %s"

    cursor = current_app.mysql.connection.cursor()
    cursor.execute(sql, (id,))
    current_app.mysql.connection.commit()
    affected = cursor.rowcount
    cursor.close()

    return affected > 0
