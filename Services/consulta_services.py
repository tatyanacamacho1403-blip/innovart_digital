# Servicio de consulta

from flask import current_app
from Models.consulta import Consulta


def servListConsulta():
    sql = "SELECT * FROM T_CONSULTA"

    c = current_app.mysql.connection.cursor()
    c.execute(sql)

    data = c.fetchall()

    consultas_l = []

    for u in data:
        consultas_l.append(Consulta(u[0], u[1], u[2], u[3], u[4]).to_dic())

    c.close()

    return consultas_l


def addConsulta(data):
    sql = "INSERT INTO T_CONSULTA (CON_ID, CON_UUID, CON_HORA, CON_FECHA, CON_MENSAJE) VALUES (%s, %s, %s, %s, %s)"
    values = (data.get("id"), data.get("uuid"), data.get("hora"), data.get("fecha"), data.get("mensaje"))

    c = current_app.mysql.connection.cursor()
    c.execute(sql, values)
    current_app.mysql.connection.commit()
    new_id = c.lastrowid
    c.close()

    return servGetConsulta(new_id)


def upConsulta(id, data):
    sql = "UPDATE T_CONSULTA SET CON_UUID = %s, CON_HORA = %s, CON_FECHA = %s, CON_MENSAJE = %s WHERE CON_ID = %s"
    values = (data.get("uuid"), data.get("hora"), data.get("fecha"), data.get("mensaje"), id)

    c = current_app.mysql.connection.cursor()
    c.execute(sql, values)
    current_app.mysql.connection.commit()
    affected = c.rowcount
    c.close()

    if affected == 0:
        return None

    return servGetConsulta(id)


def delConsulta(id):
    sql = "DELETE FROM T_CONSULTA WHERE CON_ID = %s"

    c = current_app.mysql.connection.cursor()
    c.execute(sql, (id,))
    current_app.mysql.connection.commit()
    affected = c.rowcount
    c.close()

    return affected > 0


def servGetConsulta(id):
    sql = "SELECT * FROM T_CONSULTA WHERE CON_ID = %s"

    c = current_app.mysql.connection.cursor()
    c.execute(sql, (id,))
    u = c.fetchone()
    c.close()

    if u is None:
        return None

    return Consulta(u[0], u[1], u[2], u[3], u[4]).to_dic()
