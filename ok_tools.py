import requests
import os
import json
import environs
from common_function import download_image, get_file_extension


POST_TEXT = 'zz1'  # text_field
PUBLISH_DATE = '2023-03-17 06:53:00'


def main():
    env = environs.Env()
    env.read_env()
    session_key = env('OK_SESSION')
    access_token = env('OK_ACCESS_TOKEN')
    public_key = env('OK_PUBLIC_KEY')
    gid = env('OK_GROUP_ID')
    url = 'https://duet-cdn.vox-cdn.com/thumbor/0x0:900x500/640x427/filters:focal(450x250:451x251):format(webp)/cdn.vox-cdn.com/uploads/chorus_asset/file/6438793/this-is-fine.jpg'
    img_name = f'image.{get_file_extension(url)}'
    download_image(url, img_name)
    try:
        upload_url, photo_id = get_upload_url(access_token,
                                              public_key,
                                              session_key,
                                              gid
                                              )
        uploaded_image = upload_image(upload_url, img_name)
        image_token = uploaded_image['photos'][photo_id[0]]['token']
        make_post(access_token, public_key, session_key,
                  gid,
                  image_token,
                  POST_TEXT,
                  PUBLISH_DATE
                  )
    finally:
        os.remove(img_name)


def check_ok_answer(decoded_response):
    if 'error_code' in decoded_response:
        error_code = decoded_response['error_code']
        error_message = decoded_response['error_msg']
        raise requests.HTTPError(f'{error_code}: {error_message}')


def get_upload_url(ok_access_token, application_key, session_secret_key, gid):
    url = 'https://api.ok.ru/fb.do?method=photosV2.getUploadUrl'
    params = {'application_key': application_key,
              'access_token': ok_access_token,
              'session_secret_key': session_secret_key,
              'gid': gid
              }
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


def post_photo(access_token, public_key, session_key,
              group_id,
              image_token,
              post_text,
              publish_date
              ):
    save_url = 'https://api.ok.ru/fb.do?method=mediatopic.post'
    media = {"media": [{"type": "photo", "list": [{"id": image_token}]},
                       {'type': 'text', 'text': post_text}
                       ],
            "publishAt": publish_date
            }
    attachment = json.dumps(media)
    params = {'access_token': access_token, 'gid': group_id,
              'type': 'GROUP_THEME',
              'attachment': attachment,
              'application_key': public_key,
              'session_secret_key': session_key
              }
    response = requests.post(save_url, params=params)
    check_ok_answer(response)


if __name__ == '__main__':
    main()
