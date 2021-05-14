from models.cryptocurrency.crypto import Crypto

class Cro(Crypto):
    def __init__(self, currency_name):
        super().__init__("!CRO", currency_name)

    def message_price(self):
        self.get_price()
        return f"Le prix du cro est de {self.price} {self.currency} ({self.hours})"
