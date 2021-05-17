#!/usr/bin/python3
"""
    Main class to all cryptocurrencies
"""
import os
import requests
import json
from dotenv import load_dotenv
load_dotenv(dotenv_path="../../config")
class Crypto:
    """
    Parent class to all crypto
    """
    api_key = "api_key"
    def __init__(self, crypto_n, currency):
        """
        crypto_n: name of the crypto wanted
        currency: the exchange of the price 
        """
        self.currency = currency
        self.crypto_name = crypto_n
        self.content = requests.get(f"https://api.nomics.com/v1/currencies/ticker?key={self.api_key}&ids={self.__crypto_name}&interval=1d,30d&convert=EUR&per-page=100&page=1")
        self.price = 0
        self.hours = None

    @property
    def currency(self):
        """ getter of property currency """
        return self.__currency

    @currency.setter
    def currency(self, value):
        """ setter of property currency """
        self.__currency = value

    @property
    def crypto_name(self):
        """ getter of property crypto_name """
        return self.__crypto_name

    @crypto_name.setter
    def crypto_name(self, value):
        """
        Setter of property crypto_name
        Check if the crypto wanted is
        in the list of currency avalaible
        If yes, assigne the value
        [1:] = slice the ! of the command given
        """
        crypto_list = json.loads(os.getenv("CRYPTO"))
        if value[1:] in crypto_list:
            self.__crypto_name = value[1:]
        else:
            return None

    def get_price(self):
        """
        Deserialize and assign the price and hours
        """
        self.price = "{0:.2f}".format(float(self.content.json()[0]['price']))
        self.hours = self.content.json()[0]['price_timestamp']
