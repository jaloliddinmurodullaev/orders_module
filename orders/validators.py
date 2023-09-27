
class Validator:
    def __init__(self, data):
        self.data = data

    def order_creation_request_data_validator(self):
        return True

    def order_update_request_data_validator(self):
        return True

    def passenger_update_request_data_validator(self):
        return True