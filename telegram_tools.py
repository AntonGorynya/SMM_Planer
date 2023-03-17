import environs
from pyrogram import Client, types, raw
from _datetime import datetime



async def post_photo(app, image, description, date, channel):
    async with app:
        await app.send_photo(channel, photo=image, caption=description, schedule_date=date)


if __name__ == '__main__':
    env = environs.Env()
    env.read_env()
    tg_api_id = env('TG_API_ID')
    tg_app_api_hash = env('TG_APP_API_HASH')
    tg_cahannel = env('TG_CHAT_ID')
    tg_admin = env('TG_ADMIN')

    app = Client(name=tg_admin, api_id=tg_api_id, api_hash=tg_app_api_hash)
    date = datetime(year=2023, month=3, day=17, hour=22, minute=6)
    print(date)
    image = "https://cs14.pikabu.ru/post_img/2023/03/16/11/1678996500118751201.webp"

    app.run(post_photo(app, image, 'description', date, tg_cahannel))