import requests
import os
from dotenv import load_dotenv

def main():
    load_dotenv()
    session =  os.environ.get('OK_SESSION')
    access_token = os.environ.get('OK_ACCESS_TOKEN')
    public_key = os.environ.get('OK_PUBLIC_KEY')    
    comment = 'zz1'
    image_path = 'comix.png'
    upload_url, photo_id =  get_upload_url(access_token, public_key, session)
    uploaded_image = upload_image(upload_url, image_path)
    token = uploaded_image['photos'][photo_id[0]]['token']
    post_comics(public_key, access_token, session, comment, token, photo_id)

def check_ok_answer(decoded_response):
    if 'error_code' in decoded_response:
        raise Exception(decoded_response['error_msg'])


def get_upload_url(ok_access_token, application_key, session_secret_key):
    url = 'https://api.ok.ru/fb.do?method=photosV2.getUploadUrl'
    params = {'application_key': application_key, 'access_token' : ok_access_token, 'session_secret_key' : session_secret_key}
    upload_response = requests.get(url, params=params).json()
    check_ok_answer(upload_response)
    upload_url = upload_response['upload_url']
    photo_id = upload_response['photo_ids']
    return upload_url, photo_id


def upload_image(url, image_path):
    with open(image_path, 'rb') as file:
        file = {
                'photo': file,
                }
        upload_response = requests.post(url, files=file)
    upload_response.raise_for_status()
    uploaded_image = upload_response.json()
    check_ok_answer(uploaded_image)
    return uploaded_image


def post_comics(application_key, access_token,
                session_secret_key,
                comment,
                token,
                photo_id
                ):
        url = 'https://api.ok.ru/fb.do?method=photosV2.commit'        
        params_save = {'application_key': application_key,
                       'access_token' : access_token,
                       'session_secret_key': session_secret_key,
                       'comment': comment,
                       'token' : token,
                       'photo_id' : photo_id
                       }
        response = requests.post(url, params_save)
        decoded_response = response.json()
        check_ok_answer(decoded_response)

if __name__ == '__main__':
    main()