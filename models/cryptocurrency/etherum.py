
#import crypto
from models.cryptocurrency.crypto import Crypto

class Etherum(Crypto):
    def __init__(self, currency_name):
        super().__init__("!ETH", currency_name)

    def message_price(self):
        self.get_price()
        return f"Le prix de l'etherum est de {self.price} {self.currency} ({self.hours})"
