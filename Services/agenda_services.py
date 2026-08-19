from flask import current_app
from Models.agenda import Agenda


def servListAgenda():
    sql = "SELECT * FROM T_AGENDA"
    c = current_app.mysql.connection.cursor()
    c.execute(sql)
    data = c.fetchall()
    agendas_l = []
    for u in data:
        agendas_l.append(Agenda(u[0], u[1], u[2], u[3], u[4], u[5]).to_dic())
    c.close()
    return agendas_l


def addAgenda(data):
    sql = "INSERT INTO T_AGENDA (AGE_ID, AGE_UUID, AGE_FECHA, AGE_HORA, AGE_USU_ID, AGE_SER_ID) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (data.get("id"), data.get("uuid"), data.get("fecha"), data.get("hora"), data.get("usu_id"), data.get("ser_id"))
    c = current_app.mysql.connection.cursor()
    c.execute(sql, values)
    current_app.mysql.connection.commit()
    new_id = c.lastrowid
    c.close()
    return servGetAgenda(new_id)


def upAgenda(id, data):
    sql = "UPDATE T_AGENDA SET AGE_UUID = %s, AGE_FECHA = %s, AGE_HORA = %s, AGE_USU_ID = %s, AGE_SER_ID = %s WHERE AGE_ID = %s"
    values = (data.get("uuid"), data.get("fecha"), data.get("hora"), data.get("usu_id"), data.get("ser_id"), id)
    c = current_app.mysql.connection.cursor()
    c.execute(sql, values)
    current_app.mysql.connection.commit()
    affected = c.rowcount
    c.close()
    if affected == 0:
        return None
    return servGetAgenda(id)


def delAgenda(id):
    sql = "DELETE FROM T_AGENDA WHERE AGE_ID = %s"
    c = current_app.mysql.connection.cursor()
    c.execute(sql, (id,))
    current_app.mysql.connection.commit()
    affected = c.rowcount
    c.close()
    return affected > 0


def servGetAgenda(id):
    sql = "SELECT * FROM T_AGENDA WHERE AGE_ID = %s"
    c = current_app.mysql.connection.cursor()
    c.execute(sql, (id,))
    u = c.fetchone()
    c.close()
    if u is None:
        return None
    return Agenda(u[0], u[1], u[2], u[3], u[4], u[5]).to_dic()
