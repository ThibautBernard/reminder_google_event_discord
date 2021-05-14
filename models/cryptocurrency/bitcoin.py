from models.cryptocurrency.crypto import Crypto
class Bitcoin(Crypto):
    def __init__(self, currency_name):
        super().__init__("!BTC", currency_name)

    def message_price(self):
        self.get_price()
        return f"Le prix du bitcoin est de {self.price} {self.currency} ({self.hours})"