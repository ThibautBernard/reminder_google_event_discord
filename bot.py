#!/usr/bin/python3
"""
    Main client to the discord api
    and the discord channel
"""
import os
import discord
import requests
import json
import datetime
import time
from dotenv import load_dotenv
load_dotenv(dotenv_path="config")
from models.cldr import Calendar
from models.commands import Commands
import asyncio
from time import gmtime
from time import strftime


class MyClient(discord.Client):
    identifier_cmd = "!"
    id_main_channel = id_of_the_channel

    def __init__(self):
        super().__init__()
        self.main_channel = None
        self.commands = json.loads(os.getenv("COMMANDS"))
        self.msg_to_respond = json.loads(os.getenv("MSG_RESPONDS"))
        self.reunion_date = 0
        self.name_reunion = ""
        self.link_event = None
        self.msg_bot_start = os.getenv("MSG_BOT_START")
    
    def change_status(self, activity):
        """Change the statut of the bot"""
        self.activity = discord.Game(activity)
    
    async def get_calendar_event(self):
        """Call the api calendar and get value from event"""
        c = Calendar()
        c.launch()
        self.reunion_date = c.seconds_event
        self.name_reunion = c.name_event
        if c.info_event and c.link_event:
            self.link_event = c.link_event
        print(self.reunion_date)
        await asyncio.sleep(3)

    async def check_reunion_is_soon(self):
        """ Check if the datetime of the event is soon
        if yes, send a msg to the main channel
        and sleep the time of the event to start"""
        if self.reunion_date and self.name_reunion and self.reunion_date > 60 and self.reunion_date < 300:
            await self.send_channel_msg("{} va commencer dans moins de : {}".format(self.name_reunion, strftime("%M:%S", gmtime(int(self.reunion_date)))))
            await asyncio.sleep(self.reunion_date)
        elif self.reunion_date and self.name_reunion and self.reunion_date >= -60 and self.reunion_date <= 0:
            await self.send_channel_msg("@everyone {} commence actuellement ! ({})".format(self.name_reunion, self.link_event))
            await asyncio.sleep(60)

        await asyncio.sleep(3)

    async def on_ready(self):
        """ When the bot connect into channel """
        self.main_channel = self.get_channel(self.id_main_channel)
        self.change_status("Working on the api")
        #await self.main_channel.send("@everyone " + "Just a test!")
        await self.change_presence(status=discord.Status.idle, activity=self.activity)
        while True:
            await self.get_calendar_event()
            await self.check_reunion_is_soon()
            await asyncio.sleep(3)

    async def send_channel_msg(self, msg):
        """msg to the main channel"""
        await self.main_channel.send(msg)

    async def on_member_join(self, member):
        """ When somebody join the discord """
        await member.create_dm()
        await member.dm_channel.send(f'Salut {member.name}, merci d\'avoir rejoins le discord ;) !')

    async def on_message(self, message):
        """ When someone send a message in the discord """
        if message.author == self.user:
            return
        msg_user_list = message.content.split()
        msg_user = msg_user_list[0]
        if msg_user_list[0][0] == self.identifier_cmd:
            cmd = Commands(msg_user_list)
            await message.channel.send(cmd.message_to_respond())

b = MyClient()
b.run(os.getenv("TOKEN"))
