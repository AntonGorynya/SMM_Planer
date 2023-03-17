import environs
import os
import datetime
import time
import pandas as pd
import telegram_tools
from googleapiclient.discovery import build
from google_tools import get_credentials, get_sheet, write_cells, add_event, read_docs, get_id_from_url, SCOPES
from common_function import get_file_extension, download_image
from vk_tools import get_wall_upload_server, make_post, API_VERSION
from ok_tools import get_upload_url, upload_image, post_photo
from pyrogram import Client


if __name__ == '__main__':
    env = environs.Env()
    env.read_env()
    vk_token = env('VK_IMPLICIT_FLOW_TOKEN')
    vk_group_id = env.int('VK_GROUP_ID')
    vk_upload_url = get_wall_upload_server(vk_token, vk_group_id, API_VERSION)
    ok_session_key = env('OK_SESSION')
    ok_access_token = env('OK_ACCESS_TOKEN')
    ok_public_key = env('OK_PUBLIC_KEY')
    ok_gid = env('OK_GROUP_ID')
    tg_api_id = env('TG_API_ID')
    tg_app_api_hash = env('TG_APP_API_HASH')
    tg_cahannel = env('TG_CHAT_ID')
    tg_admin = env('TG_ADMIN')
    callendar_id = env('CALLENAR_ID')
    spreadsheet_id = env('SPREADSHEET_ID')
    credentials = get_credentials(SCOPES)
    sheets_service = build('sheets', 'v4', credentials=credentials)
    cal_service = build('calendar', 'v3', credentials=credentials)
    docs_service = build('docs', 'v1', credentials=credentials)
    table_range = 'List1!A1:I'

    values = get_sheet(sheets_service, spreadsheet_id, table_range)
    df = pd.DataFrame.from_records(values)
    df.columns = df.iloc[0]
    df = df[1:]
    for index, row in df.iterrows():
        if not row['VK_published'] or not row['OK_published'] or not row['Telegram_published']:
            img_url = row['img_url']
            doc_url = row['Text_description']
            img_name = f'test.{get_file_extension(img_url)}'
            img_description = read_docs(docs_service, get_id_from_url(doc_url))
            date_time = datetime.datetime.strptime(row['date'], '%Y-%m-%d %H:%M')
            unix_date = time.mktime(date_time.timetuple())
            download_image(img_url, img_name)

        if row['VK'] and not row['VK_published']:
            try:
                make_post(
                    img_name,
                    img_description,
                    vk_upload_url,
                    vk_token,
                    vk_group_id,
                    API_VERSION,
                    publish_date=unix_date
                )
                write_cells(sheets_service, spreadsheet_id, f'List1!G{index+1}', ['TRUE'])
                add_event(cal_service, callendar_id, date_time.strftime('%Y-%m-%d'), color_id=2, summary='VK')
            except:
                add_event(cal_service, callendar_id, date_time.strftime('%Y-%m-%d'), color_id=1, summary='VK exception')
            finally:
                os.remove(img_name)

        if row['OK'] and not row['OK_published']:
            try:
                upload_url, photo_id = get_upload_url(ok_access_token,
                                                    ok_public_key,
                                                    ok_session_key,
                                                    ok_gid
                                                    )
                uploaded_image = upload_image(upload_url, img_name)
                image_token = uploaded_image['photos'][photo_id[0]]['token']

                post_photo(ok_access_token, ok_public_key, ok_session_key,
                          ok_gid,
                          image_token,
                          img_description,
                          date_time.strftime('%Y-%m-%d %H:%M')
                          )
                write_cells(sheets_service, spreadsheet_id, f'List1!I{index+1}', ['TRUE'])
                add_event(cal_service, callendar_id, date_time.strftime('%Y-%m-%d'), color_id=2, summary='OK')
            except:
                add_event(cal_service, callendar_id, date_time.strftime('%Y-%m-%d'), color_id=1, summary='OK exception')
            finally:
                os.remove(img_name)
        if row['Telegram'] and not row['Telegram_published']:
            try:
                app = Client(name=tg_admin, api_id=tg_api_id, api_hash=tg_app_api_hash)
                app.run(telegram_tools.post_photo(app, img_url, img_description, date_time, tg_cahannel))
                write_cells(sheets_service, spreadsheet_id, f'List1!H{index + 1}', ['TRUE'])
                add_event(cal_service, callendar_id, date_time.strftime('%Y-%m-%d'), color_id=2, summary='OK')
            except:
                add_event(cal_service, callendar_id, date_time.strftime('%Y-%m-%d'), color_id=1,
                          summary='TG exception')

