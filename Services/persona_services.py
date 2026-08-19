# Servicio de persona

from flask import current_app
from Models.persona import Persona


def servListPersona():
    sql = "SELECT * FROM T_PERSONA"

    c = current_app.mysql.connection.cursor()
    c.execute(sql)

    data = c.fetchall()

    personas_l = []

    for u in data:
        personas_l.append(Persona(u[0], u[1], u[2], u[3], u[4], u[5], u[6], u[7], u[8], u[9], u[10], u[11]).to_dic())

    c.close()

    return personas_l


def addPersona(data):
    sql = "INSERT INTO T_PERSONA (PER_ID, PER_UUID, PER_CEDULA, PER_DOCUMENTO, PER_PRIMER_NOMBRE, PER_SEGUNDO_NOMBRE, PER_PRIMER_APELLIDO, PER_SEGUNDO_APELLIDO, PER_FECHA_NACIMIENTO, PER_DIRECCION, PER_TELEFONO, PER_CORREO_ELECTRONICO) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (data.get("id"), data.get("uuid"), data.get("cedula"), data.get("documento"), data.get("primer_nombre"), data.get("segundo_nombre"), data.get("primer_apellido"), data.get("segundo_apellido"), data.get("fecha_nacimiento"), data.get("direccion"), data.get("telefono"), data.get("correo_electronico"))

    c = current_app.mysql.connection.cursor()
    c.execute(sql, values)
    current_app.mysql.connection.commit()
    new_id = c.lastrowid
    c.close()

    return servGetPersona(new_id)

def upPersona(id, data):
    sql = "UPDATE T_PERSONA SET PER_UUID = %s, PER_CEDULA = %s, PER_DOCUMENTO = %s, PER_PRIMER_NOMBRE = %s, PER_SEGUNDO_NOMBRE = %s, PER_PRIMER_APELLIDO = %s, PER_SEGUNDO_APELLIDO = %s, PER_FECHA_NACIMIENTO = %s, PER_DIRECCION = %s, PER_TELEFONO = %s, PER_CORREO_ELECTRONICO = %s WHERE PER_ID = %s"
    values = (data.get("uuid"), data.get("cedula"), data.get("documento"), data.get("primer_nombre"), data.get("segundo_nombre"), data.get("primer_apellido"), data.get("segundo_apellido"), data.get("fecha_nacimiento"), data.get("direccion"), data.get("telefono"), data.get("correo_electronico"), id)

    c = current_app.mysql.connection.cursor()
    c.execute(sql, values)
    current_app.mysql.connection.commit()
    affected = c.rowcount
    c.close()

    if affected == 0:
        return None
    return servGetPersona(id)

def delPersona(id):
    sql = "DELETE FROM T_PERSONA WHERE PER_ID = %s"

    c = current_app.mysql.connection.cursor()
    c.execute(sql, (id,))
    current_app.mysql.connection.commit()
    affected = c.rowcount
    c.close()

    return affected > 0