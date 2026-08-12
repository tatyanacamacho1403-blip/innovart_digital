from flask import current_app
from Models.users import users

def servlist_users():
    sql = "SELECT * FROM users"
    c   = current_app.mysql.connection.cursor() 
    c.execute(sql)                              
    data = c.fetchall()
    print(data)

    users_l =[ ]
    for u in data:
        users_l.append(users(u[0],u[1],u[2],u[3],u[4],u[5],u[6]).to_dict())
    print(users_l)
    c.close()            
    return users_l

def register_user():
    pass

def longin_user():
    pass

def logout_user():
    pass



