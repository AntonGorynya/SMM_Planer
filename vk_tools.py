import requests
import os
import environs
from common_function import download_image, get_file_extension


API_VERSION = '5.131'
IMG_URL = 'https://xkcd.com/{id}/info.0.json'
VK_API_URL = 'https://api.vk.com/method/{metod}'


def check_vk_response(response):
    if 'error' in response:
        error_code = response['error']['error_code']
        error_msg = response['error']['error_msg']
        raise requests.HTTPError(f'{error_code}: {error_msg}')


def get_wall_upload_server(vk_token, vk_group_id, api_version):
    params = {
        'access_token': vk_token,
        'v': api_version,
        'owner_id': vk_group_id,
    }
    response = requests.get(
        VK_API_URL.format(
            metod='photos.getWallUploadServer'),
            params=params
    )
    response.raise_for_status()
    response = response.json()
    check_vk_response(response)
    return response['response']['upload_url']


def upload_photo(img_name, upload_url, vk_token, vk_group_id, api_version):
    with open(img_name, 'rb') as photo:
        response = requests.post(
            upload_url,
            files={'photo': photo}
        )
    response.raise_for_status()
    photo_meta = response.json()
    check_vk_response(photo_meta)
    params = {
        'access_token': vk_token,
        'v': api_version,
        'owner_id': vk_group_id,
        'server': photo_meta['server'],
        'photo': photo_meta['photo'],
        'hash': photo_meta['hash'],
    }
    response = requests.post(
        VK_API_URL.format(metod='photos.saveWallPhoto'),
        params=params
    )
    response.raise_for_status()
    response = response.json()
    check_vk_response(response)
    return response['response'][0]


def post_photo(media_id, owner_id, img_description, vk_token, vk_group_id, api_version, publish_date=''):
    params = {
        'access_token': vk_token,
        'v': api_version,
        'owner_id': f'-{vk_group_id}',
        'from_group': 1,
        'message': img_description,
        'attachments': f'photo{owner_id}_{media_id}',
        'publish_date': publish_date
    }
    response = requests.post(
        VK_API_URL.format(metod='wall.post'),
        params=params
    )
    response.raise_for_status()
    response = response.json()
    check_vk_response(response)
    return response


def make_post(img_name, img_description, upload_url, vk_token, vk_group_id, API_VERSION, publish_date=''):
    photo_meta = upload_photo(img_name, upload_url, vk_token, vk_group_id, API_VERSION)
    media_id = photo_meta['id']
    owner_id = photo_meta['owner_id']
    post_photo(media_id, owner_id, img_description, vk_token, vk_group_id, API_VERSION, publish_date=publish_date)


if __name__ == '__main__':
    env = environs.Env()
    env.read_env()
    vk_token = env('VK_IMPLICIT_FLOW_TOKEN')
    vk_group_id = env.int('VK_GROUP_ID')
    url = 'https://duet-cdn.vox-cdn.com/thumbor/0x0:900x500/640x427/filters:focal(450x250:451x251):format(webp)/cdn.vox-cdn.com/uploads/chorus_asset/file/6438793/this-is-fine.jpg'
    img_name = f'test.{get_file_extension(url)}'
    img_description = 'ololo3'
    download_image(url, img_name)
    try:
        upload_url = get_wall_upload_server(vk_token, vk_group_id, API_VERSION)
        make_post(img_name, img_description, upload_url, vk_token, vk_group_id, API_VERSION)
    finally:
        os.remove(img_name)
