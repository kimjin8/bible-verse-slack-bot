# Slack App: Bible Verse
# A Bible verse to kickstart your day.
# 
# git clone https://github.com/guymorrell/slack-webhooks-blockkit
# YouVersion API Reference: https://yv-public-api-docs.netlify.com/getting-started.html

import os
import json
import time
import requests


# Functions
# Calculate Day of the Year
def day_of_year():
  day_of_year = time.localtime().tm_yday
  day_of_year = str(day_of_year)
  print("day of year:", day_of_year)
  return day_of_year


# Convert Bytes to JSON
def bytes_to_json(bytes_value): 
  json_value = bytes_value.decode('utf8')
  json_value = json.loads(json_value)
  return json_value


# Get Verse of a Day
def verse_of_day(day_of_year):
  headers = {
      'accept': "application/json",
      "x-youversion-developer-token": YOUVERSION_DEVELOPER_TOKEN,
      "accept-language": "en"
  }
  api_url = "https://developers.youversionapi.com/1.0/verse_of_the_day/" + day_of_year + "?version_id=1"
  response = requests.get(
      api_url,
      headers=headers
  )
  print('api response:', response.content)
  
  verse_json = bytes_to_json(response.content)
  
  verse_ref = verse_json["verse"]["human_reference"]
  verse_text = verse_json["verse"]["text"]
  verse = verse_text + "  " + verse_ref
  print(verse)
  
  return verse


# Slack Message Block Text
def message_block_text(text):
  block_text = \
    [
      {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": text
        }
      }
    ]
  print("block text:", block_text)
  return block_text

def post_to_slack(message):
  slack_data = json.dumps({'blocks': message})
  response = requests.post(
      WEBHOOK_URL, data=slack_data,
      headers={'Content-Type': 'application/json'}
  )
  if response.status_code != 200:
      raise ValueError(
          'Request to slack returned an error %s, the response is:\n%s'
          % (response.status_code, response.text)
      )
  else:
    print("API callL status code: ", response.status_code)


# ---------------------------------------------------
# Main()
def lambda_handler(event, context):

  global WEBHOOK_URL
  global YOUVERSION_DEVELOPER_TOKEN
  
  # Environment variables
  WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
  YOUVERSION_DEVELOPER_TOKEN = os.environ.get("YOUVERSION_DEVELOPER_TOKEN")
  print("WEBHOOK_URL:", WEBHOOK_URL, "\n YOUVERSION_DEVELOPER_TOKEN:", YOUVERSION_DEVELOPER_TOKEN)
  if (WEBHOOK_URL is None) or (YOUVERSION_DEVELOPER_TOKEN is None):
    print("Environment variable retrieval error")
    return
  
  day_of_year_var = day_of_year()

  verse_of_day_var = verse_of_day(day_of_year_var)
  verse_of_day_message = "*"+"Day " + day_of_year_var +"*" + "\n" + verse_of_day_var

  verse_of_day_message_block = message_block_text(verse_of_day_message)

  post_to_slack(verse_of_day_message_block)
  
  return 


# ---------------------------------------------------
def local():
  from dotenv import load_dotenv

  load_dotenv() 

  event = "event"
  context = "context"

  lambda_handler(event, context)
  return

# Uncomment to run in local environment; Comment libraries for AWS lambda 
# local()