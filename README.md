# Reminder discord bot meeting zoom
### *Send a message with the link when a meeting on google calendar start*
### :star: Context
The purpose of this bot was to **create a reminder for event (Zoom)** created in google calendar.
<br>*Five minutes before the meeting, the bot send a discord message to all that say that the meeting will start soon, and send another message when the meeting start with the link of it, pratical to remember.*
<br>We can show also all the meeting of the current day with one command and print the price of cryptocurrencies(BTC, ETH...).


### :star: Used 
* Api discord
* Asynchronous
* Api google calendar
* Api cryptocurrencies

### :star: Installation
##### *Discord part*
* 1 - Install the library discord api https://github.com/Rapptz/discord.py
* 2 - Create a new application on https://discord.com/developers/applications
* 3 - Get on your application that you just registered and get you at the onglet "Oauth", coche the case "bot" and copy & paste the link in your browser, it will ask you which server you want your application on, so choose the server you want your bot in.
* 4 - Get you at the onglet "bot" and create a bot, **a token will be give to you, save it**
##### *Google calendar part*
* 5 - Do the step one on https://developers.google.com/calendar/quickstart/python and save the credentials in the root project
* 6 - Enter this command ``pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`` (if you have trouble, find another way to install this library [here](https://developers.google.com/api-client-library/python/start/installation))
##### *Api crypto*
* 7 - Sign in and get your api key [here](https://api.nomics.com) and save it for after. 
##### *Config*
* 8 - Open your file **config**  and paste the token that you saved from your bot (*step 4*), at the TOKEN={your_token_bot} 
* 9 - Open your file **bot.py** and paste the id of the channel at "id_main_channel = {the_id_of_the_channel}
  * To get the id of a channel, get at your parameters of discord app and give you access developpers
  * Right-click on a channel and copy the id of this one
* 10 - Open the file crypto in models/cryptocurrencies/crypto.py and paste your api key in *api_key = "your_api_key"*
* You finally good, congratz.
### :star: Usage 
* start the bot ``python3 bot.p``

### Commands
* !BTC (print the price of the bitcoin)
* !{whatever you type} (print a list of the current list commands you can use)
* !reunion (print all the reunion from your google calendar)
