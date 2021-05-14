#!/usr/bin/python3
"""
    Class Commands that handle commands request by the user
"""
import os
import json
from dotenv import load_dotenv
load_dotenv(dotenv_path="../config_bot/config")
from models.cryptocurrency.bitcoin import Bitcoin
from models.cldr import Calendar
from models.cryptocurrency.etherum import Etherum
from models.cryptocurrency.cro import Cro
from models.cryptocurrency.doge import Doge

class Commands:
    crypto_obj = {'BTC': Bitcoin, 'ETH': Etherum, 'CRO': Cro, 'DOGE': Doge}

    def __init__(self, list_messages_send):
        """
        list_messages_send: msg send by the user in a list
        separed by space
        """
        self.msg_list = list_messages_send
        self.commands = json.loads(os.getenv("COMMANDS"))
        self.list_cmd_crypto = json.loads(os.getenv("CRYPTO"))
        self.error_cmd_msg = os.getenv("ERROR_COMMANDS")

    def is_cmd_crypto(self, cmd):
        """ Check if the command is a cmd crypto"""
        if cmd in self.list_cmd_crypto:
            return True
        return False

    def msg_crypto(self):
        """ return the message price """
        for i in self.crypto_obj.keys():
            if i == self.msg_list[0][1:]:
                instance = self.crypto_obj[i]('EUR')
                return instance.message_price()
    
    def message_to_respond(self):
        """ return the correct msg for the cmd given
            otherwise return specifc error message
        """
        if self.is_command(self.msg_list[0]):
            if self.is_cmd_crypto(self.msg_list[0][1:]):
                return self.msg_crypto()
        else:
            return self.error_cmd_msg

    def is_command(self, cmd_to_check):
        """ Check that command send is in the list """
        if cmd_to_check in self.commands:
            return True
        return False
