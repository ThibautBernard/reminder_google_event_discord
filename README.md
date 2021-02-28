# Discord bot
# Reminder discord bot meeting zoom
### :star: Context
The purpose of this bot was to **create a reminder for event zoom** created in google calendar.
<br>*Five minutes before the meetings, the bot send a discord message to all that say that the meeting will start soon, pratical to remember.*
<br>We can show also all the meeting of the current day with one command and print the price of cryptocurrencies(BTC, ETH...).


### :star: Used 
* Api discord
* Asynchronous
* Api google calendar
* Api cryptocurrencies

### :star: Installation
* 1 - Install the library discord api https://github.com/Rapptz/discord.py
* 2 - Create a new application on https://discord.com/developers/applications
* 3 - Get on your application that you just register and go on the onglet "Oauth", coche the case "bot" and copy & paste the link in your browser, it will ask you which server you want your application on, so choose the server you want your bot in.
* 4 - Go on the onglet "bot" and create a bot, **a token will be give to you, save it**
* 5 - Do the step one on https://developers.google.com/calendar/quickstart/python and save the credentials in the root project
* 6 - Enter this command ``pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`` (if trouble, find another with to install this library on [here](https://developers.google.com/api-client-library/python/start/installation))
* 7 - Go in the **config** file and paste the token that you saved from your bot, at the TOKEN={your_token_bot} 
* 8 - Get the id of the channel you will send the message of your bot, right-click on the channel and copy the ID and paste it in **bot.py** at "id_main_channel = {the_id_of_the_channel}
* You finally good, congratz.
### :star: Usage 
* start the bot ``python3 bot.p``
