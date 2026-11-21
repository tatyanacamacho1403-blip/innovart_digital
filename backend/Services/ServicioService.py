from flask import current_app
from Models.Servicio import Servicio


class ServicioService:
    def list(self):

        sql = "SELECT SER_ID, SER_UUID, SER_NOMBRE, SER_DESCRIPCION, SER_PRECIO, SER_TIPO, SER_ESTADO FROM T_SERVICIO"

        c = current_app.mysql.connection.cursor()
        c.execute(sql)

        data = c.fetchall()

        lista_l = []

        for u in data:

            objeto = Servicio(
                    u[0],
                    u[1],
                    u[2],
                    u[3],
                    u[4],
                    u[5],
                    u[6]
            )

            lista_l.append(objeto.to_dict())

        c.close()

        return lista_l


    def getById(self, id):

        sql = "SELECT SER_ID, SER_UUID, SER_NOMBRE, SER_DESCRIPCION, SER_PRECIO, SER_TIPO, SER_ESTADO FROM T_SERVICIO WHERE SER_ID = %s"

        c = current_app.mysql.connection.cursor()
        c.execute(sql, (id,))

        data = c.fetchone()

        c.close()

        if data is None:
            return None

        objeto = Servicio(
                data[0],
                data[1],
                data[2],
                data[3],
                data[4],
                data[5],
                data[6]
        )

        return objeto.to_dict()


    def create(self, data):

        sql = "INSERT INTO T_SERVICIO (SER_UUID, SER_NOMBRE, SER_DESCRIPCION, SER_PRECIO, SER_TIPO, SER_ESTADO) VALUES (%s, %s, %s, %s, %s, %s)"

        values = (data.get('uuid'), data.get('nombre'), data.get('descripcion'), data.get('precio'), data.get('tipo'), data.get('estado'),)

        c = current_app.mysql.connection.cursor()
        c.execute(sql, values)
        current_app.mysql.connection.commit()

        new_id = c.lastrowid

        c.close()

        return self.getById(new_id)


    def update(self, id, data):

        sql = "UPDATE T_SERVICIO SET SER_UUID = %s, SER_NOMBRE = %s, SER_DESCRIPCION = %s, SER_PRECIO = %s, SER_TIPO = %s, SER_ESTADO = %s WHERE SER_ID = %s"

        values = (data.get('uuid'), data.get('nombre'), data.get('descripcion'), data.get('precio'), data.get('tipo'), data.get('estado'), id)

        c = current_app.mysql.connection.cursor()
        c.execute(sql, values)
        exists = c.rowcount > 0
        if not exists:
            c.execute("SELECT 1 FROM T_SERVICIO WHERE SER_ID = %s", (id,))
            exists = c.fetchone() is not None
        current_app.mysql.connection.commit()
        c.close()

        if not exists:
            return None

        return self.getById(id)


    def delete(self, id):

        sql = "DELETE FROM T_SERVICIO WHERE SER_ID = %s"

        c = current_app.mysql.connection.cursor()
        c.execute(sql, (id,))
        current_app.mysql.connection.commit()

        affected = c.rowcount

        c.close()

        return affected > 0
