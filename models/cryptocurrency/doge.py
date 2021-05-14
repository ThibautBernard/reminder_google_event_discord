from models.cryptocurrency.crypto import Crypto

class Doge(Crypto):
    def __init__(self, currency_name):
        super().__init__("!DOGE", currency_name)

    def message_price(self):
        self.get_price()
        return f"Le prix du DOGE est de {self.price} {self.currency} ({self.hours})"
