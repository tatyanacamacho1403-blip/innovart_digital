from flask import current_app
from Models.Rol import Rol


class RolService:
    def list(self):

        sql = "SELECT ROL_ID, ROL_UUID, ROL_TIPO FROM T_ROL"

        c = current_app.mysql.connection.cursor()
        c.execute(sql)

        data = c.fetchall()

        lista_l = []

        for u in data:

            objeto = Rol(
                    u[0],
                    u[1],
                    u[2]
            )

            lista_l.append(objeto.to_dict())

        c.close()

        return lista_l


    def getById(self, id):

        sql = "SELECT ROL_ID, ROL_UUID, ROL_TIPO FROM T_ROL WHERE ROL_ID = %s"

        c = current_app.mysql.connection.cursor()
        c.execute(sql, (id,))

        data = c.fetchone()

        c.close()

        if data is None:
            return None

        objeto = Rol(
                data[0],
                data[1],
                data[2]
        )

        return objeto.to_dict()


    def create(self, data):

        sql = "INSERT INTO T_ROL (ROL_UUID, ROL_TIPO) VALUES (%s, %s)"

        values = (data.get('uuid'), data.get('tipo'),)

        c = current_app.mysql.connection.cursor()
        c.execute(sql, values)
        current_app.mysql.connection.commit()

        new_id = c.lastrowid

        c.close()

        return self.getById(new_id)


    def update(self, id, data):

        sql = "UPDATE T_ROL SET ROL_UUID = %s, ROL_TIPO = %s WHERE ROL_ID = %s"

        values = (data.get('uuid'), data.get('tipo'), id)

        c = current_app.mysql.connection.cursor()
        c.execute(sql, values)
        exists = c.rowcount > 0
        if not exists:
            c.execute("SELECT 1 FROM T_ROL WHERE ROL_ID = %s", (id,))
            exists = c.fetchone() is not None
        current_app.mysql.connection.commit()
        c.close()

        if not exists:
            return None

        return self.getById(id)


    def delete(self, id):

        sql = "DELETE FROM T_ROL WHERE ROL_ID = %s"

        c = current_app.mysql.connection.cursor()
        c.execute(sql, (id,))
        current_app.mysql.connection.commit()

        affected = c.rowcount

        c.close()

        return affected > 0
