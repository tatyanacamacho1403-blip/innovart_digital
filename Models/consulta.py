class Consulta:

    def __init__(self, id, uuid, hota, fecha, mensaje):
        self.con_id = id
        self.con_uuid = uuid
        self.con_hota = hota
        self.con_fecha = fecha
        self.con_mensaje = mensaje

    #covertir el objeto en diccionario
    def to_dict(self):
        return {
            'id': self.con_id,
            'uuid': self.con_uuid,
            'hota': self.con_hota,
            'fecha': self.con_fecha,
            'mensaje': self.con_mensaje
        }