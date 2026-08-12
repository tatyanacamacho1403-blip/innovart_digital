from flask import current_app
from Models.pers import persona

def servlist_persona():
    sql = "SELCT * FROM persona"
    c   = current_app.mysql.connection.cursor() #esta linea linea es para ejecutar la consulta sql
    c.execute(sql)                              #esta es  para obtener los resultados de la consulta sql
    data = c.fetchall()
    print(data)

    persona_l =[ ]
    for u in data:
        persona_l.append(persona(u[0],u[1],u[2],u[3],u[4],u[5],u[6]).to_dict())
    print(persona_l)
    c.close()              #es para cerrar la conexion a la base de datos
    return persona_l

def addpersona():
    pass

def uppersona():
    pass

def delpersona():
    pass

def searchByDoc(documento):
    pass