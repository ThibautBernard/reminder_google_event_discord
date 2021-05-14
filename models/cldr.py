#!/usr/bin/python3
"""
    Class calendar that call api google calendar
    and retrieve informations about one recent event or
    all event
"""
from __future__ import print_function
import pickle
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
        """
        info_event: all informations return by the api google calendar
        """
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
        """Set the datetime for the last event to a specific format"""
        if self.info_event:
            tmp = self.info_event['start']['dateTime']
            format = "%Y-%m-%dT%H:%M:%S%z"
            tmp_date_env = datetime.strptime(tmp, format).strftime('%d-%H:%M:%S')
            self.date_event = datetime.strptime(tmp_date_env, "%d-%H:%M:%S") 

    def get_date_now(self):
        """Set the date now to the correct format"""
        date_now = datetime.now()
        format = "%Y-%m-%dT%H:%M:%S%z"
        date_now_str = date_now.strftime(format)
        date_now_transform = datetime.strptime(date_now_str, "%Y-%m-%dT%H:%M:%S").strftime('%d-%H:%M:%S')
        self.date_now = datetime.strptime(date_now_transform, "%d-%H:%M:%S")

    def get_second_rest_event(self):
        """Set the secondes rest before the event to start"""
        self.get_date_now()
        self.get_date_event()
        if self.date_event and self.date_now:
            self.seconds_event = (self.date_event - self.date_now).total_seconds()

    def get_name_event(self):
        """ Set the name of the event if exist"""
        if self.info_event:
            self.name_event = self.info_event['summary']
            if 'location' in self.info_event:
                self.link_event = self.info_event['location']

    def launch(self):
        """ Call methods to make the request """
        self.get_last_event()
        self.get_date_now()
        self.get_date_event()
        self.get_name_event()
        self.get_second_rest_event()

    def get_last_event(self):
        """Call api and store if exist
        the informations about the last event that coming
        in the max_minutes
        Event_result: dict of list
        Event_result['items']: list
        """
        now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        max_minutes = datetime.utcnow() + timedelta(minutes = 10)
        max_minutes = max_minutes.isoformat() + 'Z'
        event_result = self.service.events().list(
                                    calendarId='primary', timeMin=now, 
                                    timeMax=max_minutes, maxResults=1, 
                                    singleEvents=True,
                                    orderBy='startTime').execute()
        if event_result:
            tmp = event_result['items']
            if len(tmp) > 0 and tmp:
                if event_result['items'][0]:
                    self.info_event = event_result['items'][0]