class respuesta :
    def __init__ (self, uuid, hora, descripcion, fecha):
        self.res_uuid = uuid
        self.res_hora = hora
        self.res_descripcion = descripcion
        self.res_fecha = fecha

    def to_dict (self):
        return {
            'uuid': self.res_uuid,
            'hora': self.res_hora,
            'descripcion': self.res_descripcion,
            'fecha': self.res_fecha,
       }