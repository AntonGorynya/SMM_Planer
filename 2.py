import environs
import os.path
from google.oauth2 import service_account
import requests

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from urllib.parse import urlparse
from pathlib import PurePath


# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/calendar.events',
    'https://www.googleapis.com/auth/documents.readonly',
    'https://www.googleapis.com/auth/spreadsheets'
]

def get_credentials(scopes):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


#def main():
    #try:
        #print(1)
       #write_cells(sheets_service, spreadsheet_id, SAMPLE_RANGE_NAME2, ['TRUE'])               
        #credentials = service_account.Credentials.from_service_account_file(
        #    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        #credentials = None
        #print(credentials)
        #sheets_service = build('sheets', 'v4', credentials=credentials)
        #print(sheets_service)
        #print(2)
        #sheet = sheets_service.spreadsheets()
        #request = sheet.values().update(
        #    spreadsheetId=spreadsheet_id,
        #    range=SAMPLE_RANGE_NAME2,
        #    valueInputOption='USER_ENTERED',
        #    body=value_range_body
        #)
        #sheet = sheets_service.spreadsheets()
        #range = 'Sheet1!R1C1:R2C2'
        #print(3)
        #result = sheet.values.get(spreadsheetId=spreadsheet_id, range=range).execute()
        #request = sheets_service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range)
        #response = request.execute()
        #print(response.text)
        #url = f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{range}'
        #result = requests.get(url)
        #print(result.text)
        #request = sheets_service.spreadsheets.values.update(value_range_body, spreadsheet_id, 'A1', {'valueInputOption':'USER_ENTERED'})
        #request.execute()        
        #https://docs.google.com/spreadsheets/d/1-iO6RJoqEb4ucbTKmPGjSWnmmOWm15xHy9pvy_OSeyc/edit#gid=0&range=D2

    #except:
    #    print('fail')


def main():
    spreadsheet_id = '1fC-0e427bjDfmObYuSa9wTVLl1q-_1mHkGFiZnXR-6k'
    credentials = get_credentials(SCOPES)
    SAMPLE_RANGE_NAME = 'List1!A1:E'    
    sheets_service = build('sheets', 'v4', credentials=credentials)
    values = get_sheet(sheets_service, spreadsheet_id, SAMPLE_RANGE_NAME)
    print(values)

def get_credentials(scopes):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def get_sheet(service, spreadsheet_id, range_name):
    sheet = service.spreadsheets()
    result = sheet.values.get(
        spreadsheetId=spreadsheet_id,
        range=range_name).execute()
    values = result.get('values', [])
    return values


if __name__ == '__main__':
    main()