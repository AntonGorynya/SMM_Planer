import requests
import os
from dotenv import load_dotenv


load_dotenv()
session =  os.environ.get('OK_SESSION')
access_token = os.environ.get('OK_ACCESS_TOKEN')
public_key = os.environ.get('OK_PUBLIC_KEY')
url = 'https://api.ok.ru/fb.do?method=mediatopic.post'

params = {'uid': '573378303742',  'application_key': public_key, 'type':'USER', 'access_token':access_token, 'gid' : '70000001952510'
          "attachment" : attachment}

response = requests.post(url, params = params)
print(response.json())
