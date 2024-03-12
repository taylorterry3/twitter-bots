import requests
from bs4 import BeautifulSoup

import os

from datetime import datetime
import pytz

from dotenv import load_dotenv

import tweepy

url = "https://www.washingtonpost.com/local/dc/"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
dates = soup.select(".dot-xxs-gray-dark")

date_list = [datetime.strptime(date.text, "%B %d, %Y") for date in dates]

# Finding the most recent date, probably could just take first one but w/ev
most_recent_date = max(date_list)

most_recent_count = str(sum([1 for d in date_list if d == most_recent_date]))

s_if_multiple = "" if most_recent_count == "1" else "s"

most_recent_date_s = datetime.strftime(most_recent_date, "%B %-d, %Y")

# WIP timezones
tz = pytz.timezone("America/New_York")

current_date = datetime.now(tz=tz).date()
current_date_s = current_date.strftime("%B %-d, %Y")

if current_date <= most_recent_date.date():
    message = f"The @washingtonpost ran {most_recent_count} article{s_if_multiple} about DC today, {current_date_s}."
else:
    message = f"The @washingtonpost didn't cover DC today, {current_date_s}. The last time they covered DC was on {most_recent_date_s}, when they ran {most_recent_count} article{s_if_multiple}."

print(message)

load_dotenv()

# Authenticate to Twitter
client = tweepy.Client(
    consumer_key=os.environ.get("CONSUMER_KEY"),
    consumer_secret=os.environ.get("CONSUMER_SECRET"),
    access_token=os.environ.get("ACCESS_TOKEN"),
    access_token_secret=os.environ.get("ACCESS_TOKEN_SECRET"),
)

# Fire ze missiles
client.create_tweet(text=message)
