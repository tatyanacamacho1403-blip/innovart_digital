class service_agenda:
    def __init__(self,uuid, age_id, ser_id):
        self.ser_age_uuid = uuid
        self.ser_age_age_id = age_id
        self.ser_age_ser_id = ser_id

    def to_dict (self):
        return {
            'uuid': self.ser_age_uuid,
            'age_id': self.ser_age_ser_id,
            'documento': self.ser_age_age_id,
        }