import environs
import os.path


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


def add_event(service, callendar_id, post_date, summary='', description='', color_id=1):
    event = {
        'summary': summary,
        'description': description,
        'start': {
            'date': post_date,
        },
        'end': {
            'date': post_date,
        },
        'colorId': color_id
    }

    event = service.events().insert(calendarId=callendar_id, body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))


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
    result = sheet.values().get(
        spreadsheetId=spreadsheet_id,
        range=range_name).execute()
    values = result.get('values', [])
    return values


def write_cells(service, spreadsheet_id, range_name, values):
    value_range_body = {
        "majorDimension": "ROWS",
        "values": [values],
    }
    sheet = service.spreadsheets()
    request = sheet.values().update(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption='USER_ENTERED',
        body=value_range_body
    )
    response = request.execute()
    return response


def read_paragraph_element(element):
    """Returns the text in the given ParagraphElement.

        Args:
            element: a ParagraphElement from a Google Doc.
    """
    text_run = element.get('textRun')
    if not text_run:
        return ''
    return text_run.get('content')


def read_docs(docs_service, document_id):
    text = ''
    doc = docs_service.documents().get(documentId=document_id).execute()
    elements = doc.get('body').get('content')
    for value in elements:
        if 'paragraph' in value:
            elements = value.get('paragraph').get('elements')
            for elem in elements:
                text += read_paragraph_element(elem)
    return text


def get_id_from_url(url):
    path = urlparse(url).path
    return PurePath(path).parts[3]


if __name__ == '__main__':
    env = environs.Env()
    env.read_env()
    callendar_id = env('CALLENAR_ID')
    spreadsheet_id = env('SPREADSHEET_ID')
    credentials = get_credentials(SCOPES)
    SAMPLE_RANGE_NAME = 'List1!A1:E'
    SAMPLE_RANGE_NAME2 = 'List1!I2'
    DISCOVERY_DOC = 'https://docs.google.com/document/d/1EIuGItBETsXkK6J5wJGJWko18pHmSiYDPwmWc5W-Scw/edit?usp=sharing'

    try:
        cal_service = build('calendar', 'v3', credentials=credentials)
        # add_event(cal_service, callendar_id, '2023-03-16', color_id=2, summary='111')

        sheets_service = build('sheets', 'v4', credentials=credentials)
        values = get_sheet(sheets_service, spreadsheet_id, SAMPLE_RANGE_NAME)
        print(values)
        #write_cells(sheets_service, spreadsheet_id, SAMPLE_RANGE_NAME2, ['TRUE'])

        docs_service = build('docs', 'v1', credentials=credentials)
        get_id_from_url(DISCOVERY_DOC)
        #text = read_docs(docs_service, get_id_from_url(DISCOVERY_DOC))
    except HttpError as err:
        print(err)
