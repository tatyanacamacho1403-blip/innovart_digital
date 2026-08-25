from flask import current_app
from Models.agenda import Agenda

class agen_servicio:
    
    def servListAgenda():
    
        sql = "SELECT AGE_ID, AGE_UUID, AGE_FECHA, AGE_HORA, AGE_USU_ID, AGE_SER_ID FROM T_AGENDA"
    
        c = current_app.mysql.connection.cursor()
    
        c.execute(sql)
    
        data = c.fetchall()
    
        agendas_l = []
    
        for u in data:
    
            agenda = Agenda(
                    u[0],
                    u[1],
                    u[2],
                    u[3],
                    u[4],
                    u[5]
            )
    
            agendas_l.append(agenda.to_dict())
    
        c.close()
    
        return agendas_l
    
    
    def servGetAgenda(id):
    
        sql = "SELECT AGE_ID, AGE_UUID, AGE_FECHA, AGE_HORA, AGE_USU_ID, AGE_SER_ID FROM T_AGENDA WHERE AGE_ID = %s"
    
        c = current_app.mysql.connection.cursor()
    
        c.execute(sql, (id,))
    
        data = c.fetchone()
    
        c.close()
    
        if data is None:
            return None
    
        agenda = Agenda(
                data[0],
                    data[1],
                    data[2],
                    data[3],
                    data[4],
                    data[5]
        )
    
        return agenda.to_dict()
    
    
    def addAgenda(data):
        sql = "INSERT INTO T_AGENDA (AGE_ID, AGE_UUID, AGE_FECHA, AGE_HORA, AGE_USU_ID, AGE_SER_ID) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (data.get("id"), data.get("uuid"), data.get("fecha"), data.get("hora"), data.get("usu_id"), data.get("ser_id"),)
    
        cursor = current_app.mysql.connection.cursor()
        cursor.execute(sql, values)
        current_app.mysql.connection.commit()
        new_id = cursor.lastrowid
        cursor.close()
    
        # Si la tabla usa un ID autoincremental, lastrowid será el ID creado.
        # Si el ID se envía manualmente, el valor enviado se utiliza como respaldo.
        if not new_id:
            new_id = data.get("id")
    
        return servGetAgenda(new_id)
    
    
    def upAgenda(id, data):
        sql = "UPDATE T_AGENDA SET AGE_UUID = %s, AGE_FECHA = %s, AGE_HORA = %s, AGE_USU_ID = %s, AGE_SER_ID = %s WHERE AGE_ID = %s"
        values = (data.get("uuid"), data.get("fecha"), data.get("hora"), data.get("usu_id"), data.get("ser_id"), id)
    
        cursor = current_app.mysql.connection.cursor()
        cursor.execute(sql, values)
        current_app.mysql.connection.commit()
        affected = cursor.rowcount
        cursor.close()
    
        if affected == 0:
            return None
    
        return servGetAgenda(id)
    
    
    def delAgenda(id):
        sql = "DELETE FROM T_AGENDA WHERE AGE_ID = %s"
    
        cursor = current_app.mysql.connection.cursor()
        cursor.execute(sql, (id,))
        current_app.mysql.connection.commit()
        affected = cursor.rowcount
        cursor.close()
    
        return affected > 0
