# Twitter Bot that tweets the Weather everyday!
Works by tweeting at the bot with the location you want to be notified  

## Usage
`@bot_tag Lisbon, Portugal`  
The bot will tweet at you everyday at 08:00 Lisbon Time the maximum and minimum expected temperature for Madrid, Spain

## Bot features
- Tweets everyday at 9am Lisbon Time
- Doesn't allow multiple locations for 1 user automatically (can be done manually by changing your users_accepted.txt)
- Auto follow back (if enabled)
- Information provided:
  - Forecast for maximum and minimum temperature
  - Actual temperature and sensation temperature
  - Bad conditions warning (Rain & Snow)
  - UV Index
  - Advice for sunscreen on high UV
  - Tell if the weather is good to go to the beach
  - Sunset time (Lisbon Time)

## Dependencies
`pip install tweepy`  
`pip install pycountry`  
`pip install pyowm`  
`pip install google-trans-new`  
`pip install python-dotenv`  

## API Keys
To use this repository create a file named `.env` on `weather_twitterbot` directory  
For this you need to create a Developer Twitter Account
```
CONSUMER_KEY=YOUR_CONSUMER_KEY_TWITTER_DEVELOPER_ACCOUNT
CONSUMER_SECRET=YOUR_CONSUMER_SECRET_KEY_TWITTER_DEVELOPER_ACCOUNT
ACCESS_TOKEN=YOUR_ACCESS_TOKEN_TWITTER_DEVELOPER_ACCOUNT
ACCESS_TOKEN_SECRET=YOUR_ACCESS_TOKEN_SECRET_TWITTER_DEVELOPER_ACCOUNT
API_KEY=YOUR_API_KEY_OWM
```

## Create a service
On `line 8` in `twitterbot.service`  
Change `~/github/weather_twitterbot/bot.py` to `your_path_to_file/bot.py`  
If you aren't sure what's the path to the file go inside the directory that contains the file and do `pwd` on the terminal  

Now open the terminal on `weather_twitterbot/` and run  
```
sudo cp twitterbot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start twitterbot.service
sudo systemctl enable twitterbot.service
```
The last command is to make sure that the service is started on system startup
