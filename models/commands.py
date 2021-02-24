#!/usr/bin/python3
"""
    Class Commands that handle commands request by the user
"""
import os
import discord
import requests
import json
import datetime
from dotenv import load_dotenv
load_dotenv(dotenv_path="../config")
from models.cryptocurrency.bitcoin import Bitcoin
from models.cldr import Calendar
from models.cryptocurrency.etherum import Etherum
from models.cryptocurrency.cro import Cro
from models.cryptocurrency.doge import Doge

class Commands:
    crypto_obj = {'BTC': Bitcoin, 'ETH': Etherum, 'CRO': Cro, 'DOGE': Doge}
    other_cmd = {'!reunion': Calendar}

    def __init__(self, list_messages_send):
        """
        list_messages_send: msg send by the user in a list
        """
        self.msg_list = list_messages_send
        self.commands = json.loads(os.getenv("COMMANDS"))
        self.msg_to_respond = json.loads(os.getenv("MSG_RESPONDS"))
        self.list_cmd_crypto = json.loads(os.getenv("CRYPTO"))
        self.error_cmd_msg = os.getenv("ERROR_COMMANDS")

    def parse_cmd_list(self, to_find):
        """ Parse the list to return the msg to the cmd """
        idx = self.commands.index(to_find)
        return self.msg_to_respond[idx]

    def is_cmd_crypto(self, cmd):
        """ Check if the command is a cmd crypto"""
        if cmd in self.list_cmd_crypto:
            return True
        return False

    def is_other_cmd(self, cmd):
        """Check in dictionnary if the cmd given exist"""
        for key in self.other_cmd.keys():
            if key == cmd:
                return True
        return False

    def msg_other_cmd(self, cmd):
        """ Return the msg of other cmd for the cmd given"""
        for key in self.other_cmd.keys():
            if key == cmd:
                calendar = self.other_cmd[key]()
                calendar.launch()
                str_to_print = calendar.get_all_event()
                if str_to_print and len(str_to_print) > 0:
                    return str_to_print
                else:
                    return "Pas de réunion de prévu"

    def msg_crypto(self):
        for i in self.crypto_obj.keys():
            if i == self.msg_list[0][1:]:
                instance = self.crypto_obj[i]('EUR')
                return instance.message_price()
    
    def message_to_respond(self):
        """ return the msg to the cmd"""
        if self.is_command(self.msg_list[0]):
            if self.has_msg_to_respond(self.msg_list[0]):
                return self.parse_cmd_list(self.msg_list[0])
            elif self.is_cmd_crypto(self.msg_list[0][1:]):
                return self.msg_crypto()
            elif self.is_other_cmd(self.msg_list[0]):
                return self.msg_other_cmd(self.msg_list[0])
        else:
            return self.error_cmd_msg

    def is_command(self, cmd_to_check):
        """ Check that command send is in the list """
        if cmd_to_check in self.commands:
            return True
        return False

    def has_msg_to_respond(self, cmd_to_check):
        """Check if the command has a msg to return """
        idx = self.commands.index(cmd_to_check)
        for index, i in enumerate(self.msg_to_respond):
            if index == idx:
                return True
        return False