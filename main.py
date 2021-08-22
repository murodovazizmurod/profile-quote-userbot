from telethon.sync import TelegramClient
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
from telethon.tl.functions.account import UpdateStatusRequest
import requests
from PIL import Image, ImageDraw, ImageFont
import textwrap
import time

client = TelegramClient('name', "", "")
client.start()


def get_quote():
    data = requests.get('https://quote-garden.herokuapp.com/api/v3/quotes/random').json()['data'][0]
    return data['quoteText'], data['quoteAuthor']

def image():
    text, author = get_quote()
    astr = f'''"{text}"'''
    para = textwrap.wrap(astr, width=50)

    MAX_W, MAX_H = 900, 900
    im = Image.new('RGB', (MAX_W, MAX_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(
        './font.ttf', 35)
    font2 = ImageFont.truetype(
        './font2.ttf', 20)

    current_h, pad = MAX_H/2-100, 10
    for line in para:
        w, h = draw.textsize(line, font=font)
        draw.text(((MAX_W - w) / 2, current_h), line, font=font)
        current_h += h + pad
    w, h = draw.textsize(f' - {author}', font=font2)
    draw.text(((MAX_W - w) / 2, MAX_H-100), f' - {author}', font=font2)
    

    im.save('profile.png')
    upload()


def upload():
    client(DeletePhotosRequest(client.get_profile_photos('me')))
    client(UploadProfilePhotoRequest(
        file=client.upload_file('profile.png')
    ))
    client(UpdateStatusRequest(
        offline=False
    ))

while True:
    image()
    time.sleep(10)

client.run_until_disconnected()