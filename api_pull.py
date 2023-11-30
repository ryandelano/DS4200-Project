import json

import pandas as pd
import requests
import random as rnd
import time
import io
import os

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
MONGODB_CONNECTION_STRING = os.environ.get('MONGODB_CONNECTION_STRING')
print(MONGODB_CONNECTION_STRING)
# Create a new client and connect to the server
client = MongoClient(MONGODB_CONNECTION_STRING)
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

url_dict = {
    "approved_apps" : "https://masscannabiscontrol.com/resource/hmwt-yiqy",
    "pending_apps" : "https://masscannabiscontrol.com/resource/piib-tj3f",
    "dbe_apps" : "https://masscannabiscontrol.com/resource/5dkg-e39p",
    "apro_apps" : "https://masscannabiscontrol.com/resource/albs-all",
    "total_apps" : "https://masscannabiscontrol.com/resource/n6qz-us6r",
    "agent_gender" : "https://masscannabiscontrol.com/resource/hhjg-atjk",
    "agent_race" : "https://masscannabiscontrol.com/resource/pt2c-wb44",
    "retdel_sales" : "https://masscannabiscontrol.com/resource/87rp-xn9v",
    "retdel_weekly" : "https://masscannabiscontrol.com/resource/dt9b-i6ds",
    "monthly_oz_price" : "https://masscannabiscontrol.com/resource/rqtv-uenj",
    "medical_stats" : "https://masscannabiscontrol.com/resource/g5mj-5pg3",
    "plant_activity" : "https://masscannabiscontrol.com/resource/meau-plav",
    "facility_sales" : "https://masscannabiscontrol.com/resource/fren-z7jq"
}

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15"
]

header = {
    'User-Agent': rnd.choice(user_agents),
    'Accept-Language': 'en-US, en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8,*/*;q=0.7,*/*;q=0.5',
    'Referer': 'https://www.mass.gov',
    'DNT': '1'
}

df_dict = {}

for title, url in url_dict.items():
    print(title)
    for _ in range(5):  # Retry up to 5 times
        try:
            with requests.get(url + ".json", headers=header, stream=False) as response:
                content = response.content.decode('utf-8-sig')  # Decode using 'utf-8-sig'
                data = json.loads(content)  # Parse the decoded content as JSON
                df = pd.DataFrame(data)
                df_dict[title] = df
                break  # If the request was successful, break the loop
        except Exception as error: # If not successful
            print(error)
            print("testing csv...")
            time.sleep(2)
            try:
                with requests.get(url + ".csv", headers=header, stream=False) as response:
                    content = response.content.decode('utf-8-sig') # Decode using 'utf-8-sig'
                    data = io.StringIO(content)  # Parse the decoded content as csv
                    df = pd.read_csv(data)
                    df_dict[title] = df
                    break  # If the request was successful, break the loop
            except Exception as error:
                print(error)
                print("ChunkedEncodingError occurred, retrying...")
                time.sleep(5)

def check_df_dict(df_dict):
    if len(df_dict) == len(url_dict):
        print("\nAll dataframes were successfully created.\n")
    else:
        print("\nError: Some dataframes were not created.\n")

def store_df_dict(df_dict):
    for title, df in df_dict.items():
        db = client['ccc']
        collection = db[title]
        collection.insert_many(df.to_dict('records'))


check_df_dict(df_dict)
store_df_dict(df_dict)

# def print_df_dict(df_dict):
#     for title, df in df_dict.items():
#         print(title)
#         print(df.head())
#         print(df.shape)
#         print("\n")

# print(df_dict)
