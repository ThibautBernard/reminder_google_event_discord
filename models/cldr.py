#!/usr/bin/python3
"""
    Class calendar that call api google calendar
    and retrieve informations about event
"""
from __future__ import print_function
import pickle
import json
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv(dotenv_path="../config_bot/config")
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CREDENTIALS_FILE = '../credentials.json'


class Calendar:

    def __init__(self):
        #self.creds = None
        self.service = None
        self.setup()
        self.reunion_name = 0
        self.info_event = None
        self.date_now = None
        self.get_date_now()
        self.date_event = None
        self.name_event = None
        self.seconds_event = 0
        self.link_event = None
        #self.import_meetings_list = json.loads(os.getenv("IMP_MEETINGS"))

    def setup(self):
        """ 
        Connect to the api and store values in token.pickle
        The file token.pickle stores the user's access and refresh tokens, and is
        created automatically when the authorization flow completes for the first
        time.
        """
        creds = None
        if os.path.exists('../token.pickle'):
            with open('../token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('../token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        self.service = build('calendar', 'v3', credentials=creds)

    def get_date_event(self):
        """Get the date time to the last event"""
        if self.info_event:
            tmp = self.info_event['start']['dateTime']
            format = "%Y-%m-%dT%H:%M:%S%z"
            tmp_date_env = datetime.strptime(tmp, format).strftime('%d-%H:%M:%S')
            self.date_event = datetime.strptime(tmp_date_env, "%d-%H:%M:%S") 

    def get_date_now(self):
        """Get the date now to the good format"""
        date_now = datetime.now()
        format = "%Y-%m-%dT%H:%M:%S%z"
        date_now_str = date_now.strftime(format)
        date_now_transform = datetime.strptime(date_now_str, "%Y-%m-%dT%H:%M:%S").strftime('%d-%H:%M:%S')
        self.date_now = datetime.strptime(date_now_transform, "%d-%H:%M:%S")

    def get_second_rest_event(self):
        """Return the secondes before/after the event """
        self.get_date_now()
        self.get_date_event()
        if self.date_event and self.date_now:
            self.seconds_event = (self.date_event - self.date_now).total_seconds()

    def get_name_event(self):
        """ Store if an event exist the name of this event"""
        if self.info_event:
            self.name_event = self.info_event['summary']
            if 'location' in self.info_event:
                self.link_event = self.info_event['location']

    def launch(self):
        """ Call different function needed"""
        self.get_last_event()
        self.get_date_now()
        self.get_date_event()
        self.get_name_event()
        self.get_second_rest_event()

    def get_all_event(self):
        s = ""
        date_min = datetime.today()
        date_min = date_min.replace(hour=8, minute=30)
        date_min = date_min.isoformat() + 'Z'

        date_max = datetime.today()
        date_max = date_max.replace(hour=22, minute=30)
        date_max = date_max.isoformat() + 'Z'
        events_result = self.service.events().list(
                                    calendarId='primary', timeMin=date_min, timeMax=date_max,
                                    singleEvents=True,
                                    orderBy='startTime').execute()
        for i in range(len(events_result['items'])):
            for y in events_result['items'][i]:
                if y == "summary":
                    s = s + events_result['items'][i][y] + " à "
                if y == "start":
                    format = "%Y-%m-%dT%H:%M:%S%z"
                    tmp_date = datetime.strptime(events_result['items'][i][y]['dateTime'], format).strftime('%H:%M:%S')
                    s = s + tmp_date + "\n"

        return s

    def get_last_event(self):
        """Call api and store if exist
        the informations about the last event that coming
        in the max_minutes
        Events_result: dict of list
        Events_result['items']: list
        """
        now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        max_minutes = datetime.utcnow() + timedelta(minutes = 10)
        max_minutes = max_minutes.isoformat() + 'Z'
        events_result = self.service.events().list(
                                    calendarId='primary', timeMin=now, 
                                    timeMax=max_minutes, maxResults=2, 
                                    singleEvents=True,
                                    orderBy='startTime').execute()
        if events_result:
            tmp = events_result['items']
            if len(tmp) > 0 and tmp:
                if events_result['items'][0]:
                    for i in range(len(events_result['items'])):
                        self.info_event = events_result['items'][i]