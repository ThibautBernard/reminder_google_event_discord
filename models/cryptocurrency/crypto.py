#!/usr/bin/python3
"""
    Main class to all cryptocurrencies
"""
import os
import discord
import requests
import json
import datetime
from dotenv import load_dotenv
load_dotenv(dotenv_path="../../config")
class Crypto:
    """
    Parent class to all crypto
    """
    def __init__(self, crypto_n, currency):
        """
        crypto_n: name of the crypto wanted
        currency: the exchange of the price 
        """
        self.currency = currency
        self.crypto_name = crypto_n
        self.content = requests.get(f"https://api.nomics.com/v1/currencies/ticker?key=017e9266c7648d99c635eff96ebfc725&ids={self.crypto_name}&interval=1d,30d&convert=EUR&per-page=100&page=1")
        self.price = 0
        self.hours = None

    @property
    def currency(self):
        return self.__currency

    @currency.setter
    def currency(self, value):
        self.__currency = value

    @property
    def crypto_name(self):
        return self.__crypto_name

    @crypto_name.setter
    def crypto_name(self, value):
        """
        Check if the crypto wanted is
        in the list of currency avalaible
        If yes, assigne the value
        """
        crypto_list = json.loads(os.getenv("CRYPTO"))
        if value[1:4] in crypto_list:
            self.__crypto_name = value[1:4]
        else:
            return None

    def get_price(self):
        """
        Deserialize and assign the price and hours
        """
        self.price = "{0:.2f}".format(float(self.content.json()[0]['price']))
        self.hours = self.content.json()[0]['price_timestamp']
