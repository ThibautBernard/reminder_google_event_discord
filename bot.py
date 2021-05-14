#!/usr/bin/python3
"""
    Main client to the discord api
    and the discord channel
"""
import os
import discord
import json
from dotenv import load_dotenv
load_dotenv(dotenv_path="config_bot/config")
load_dotenv(dotenv_path="config_bot/commands")
from models.cldr import Calendar
from models.commands import Commands
import asyncio
from time import gmtime
from time import strftime


class MyClient(discord.Client):
    identifier_cmd = "!"
    id_main_channel = json.loads(os.getenv("ID_CHANNEL_TO_SEND_REMINDER_MSG"))
    time_to_wait = 60
    min_time_event = 60
    max_time_event = 300

    def __init__(self):
        """Initialize informations"""
        super().__init__()
        self.main_channel = None
        self.commands = json.loads(os.getenv("COMMANDS"))
        self.event_date = 0
        self.name_event = ""
        self.link_event = None
        self.msg_bot_start = os.getenv("MSG_BOT_START")
    
    def change_status(self, activity):
        """ Change the statut of the bot"""
        self.activity = discord.Game(activity)
    
    async def get_calendar_event(self):
        """ 
            Call the api calendar and get value from the event incoming
            and print to the console informations about this event
        """
        cldr = Calendar()
        cldr.launch()
        self.event_date = cldr.seconds_event
        self.name_event = cldr.name_event
        if cldr.info_event and cldr.link_event:
            self.link_event = cldr.link_event
        if self.event_date == 0:
            print("No event soon (last 10 minutes)")
        elif self.event_date < 0:
            print("Meeting '{}' has started since {:.2f} seconds".format(self.name_event, self.event_date))
        else:
            print("Meeting '{}' in {:.2f} seconds".format(self.name_event, self.event_date))
        await asyncio.sleep(3)

    async def check_reunion_is_soon(self):
        """ 
            Check if the datetime of the event is soon
            if yes, send a msg to the main channel
            and sleep the time before the event to start
            or only 1 minute if started
        """
        if self.event_date and self.name_event and self.event_date > self.min_time_event and self.event_date < self.max_time_event:
            await self.send_channel_msg("{} will start in: {} ({})".format(self.name_event, strftime("%M:%S", gmtime(int(self.event_date))), self.link_event))
            await asyncio.sleep(self.event_date)
        elif self.event_date and self.name_event and self.event_date >= -60 and self.event_date <= 0:
            await self.send_channel_msg("@here {} has started, it's time!!".format(self.name_event))
            await asyncio.sleep(self.time_to_wait)
        await asyncio.sleep(3)

    async def on_ready(self):
        """ 
            when the bot connect to the channel and ready
            setup some informations and start the loop
            to request the calendar api
        """
        self.main_channel = self.get_channel(self.id_main_channel)
        self.change_status("Working on the api")
        await self.change_presence(status=discord.Status.idle, activity=self.activity)
        while True:
            await self.get_calendar_event()
            await self.check_reunion_is_soon()
            await asyncio.sleep(3)

    async def send_channel_msg(self, msg):
        """Message to the main channel"""
        await self.main_channel.send(msg)

    async def on_message(self, message):
        """ 
            When someone send a message in the discord 
            and check if the message is a command
        """
        if message.author == self.user:
            return
        msg_user_list = message.content.split()
        msg_user = msg_user_list[0]
        if msg_user_list[0][0] == self.identifier_cmd:
            cmd = Commands(msg_user_list)
            await message.channel.send(cmd.message_to_respond())

b = MyClient()
b.run(os.getenv("TOKEN"))
