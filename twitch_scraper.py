import gspread 
from google.oauth2.service_account import Credentials 
import pandas as pd
import requests
from datetime import datetime
import numpy as np
from numpy import array

def getStreamersFromSheet(client):
  google_sh = client.open("_Controle do grupo")
  sheet1 = google_sh.get_worksheet(6)  
  df = pd.DataFrame(data=sheet1.get_all_records())
  streamers_list = []
  for data in df.to_numpy():
    streamers_list.append(data[1])
  getViewersFromTwitch(streamers_list,client)

def getViewersFromTwitch(streamers,client):
  data = []
  for streamer in streamers:
    response = requests.get(f"https://tmi.twitch.tv/group/user/{streamer}/chatters")
    if response:
      data.append([streamer, response.json()['chatters']])
  insertDataIntoGoogleSheets(data, client)      
  
def insertDataIntoGoogleSheets(data, client):    
  google_sh = client.open("_Controle do grupo")
  sheet1 = google_sh.get_worksheet(0)  
  
  for viewer in data['viewers']:
    dateTuple = getTimestamp()  
    date = ''.join(str(v) for v in dateTuple)
    sheet1.append_rows(values=[[date, viewer]])
  
def getTimestamp():
  datetime.now(tz=None)
  dateTimeObj = datetime.now()
  return dateTimeObj.year, '/', dateTimeObj.month, '/', dateTimeObj.day, '  ', dateTimeObj.hour, ':', dateTimeObj.minute, ':', dateTimeObj.second
  
def main():
  # use creds to create a client to interact with the Google Drive API
  scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
  creds = Credentials.from_service_account_file("client_secret.json", scopes=scope)
  client = gspread.authorize(creds)  
  getStreamersFromSheet(client)

if __name__ == "__main__":
  main()    