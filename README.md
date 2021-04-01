# Twitter Bot that tweets the Weather everyday!
Works by tweeting at the bot with the location you want to be notified  

## Usage
`@bot_tag Lisbon, Portugal`  
The bot will tweet at you everyday at 10:00 (GMT+00) the maximum and minimum expected temperature for Madrid, Spain

## Bot features
- Tweets everyday at 10am GMT+00
- Doesn't allow multiple locations for 1 user automatically (can be done manually by changing your users_accepted.txt)
- Auto follow back (if enabled)
- Information provided:
  - Forecast for maximum and minimum temperature
  - Actual temperature and sensation temperature
  - Bad conditions warning (Rain & Snow)
  - UV Index
  - Advice for sunscreen on high UV
  - Tell if the weather is good to go to the beach
  - Sunset time (GMT+00 hour)

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
