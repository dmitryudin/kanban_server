import requests
from app import app
import json
import hashlib
import secrets
import datetime
import qrcode
import base64
import io
salt = b'\x1c\xc5\xc1\xee\t\r\'\xff\xf2\xf4\x12\x1c\xa2\xc9\x98\xa1\xb7\xff}\x05k"A]3\xe18\'\xd6\xb2[P'


def sendImageToMediaServer(data):
    addr = app.config['MEDIA_SERVER_ADDRESS']
    r = requests.post(addr+"/create_image",
                      data='{"base64":"' + str(data)+'"}')
    print(r.json()['name'])

    return (r.json()['name'])


def remImageFromMediaServer(name):
    addr = app.config['MEDIA_SERVER_ADDRESS']
    r = requests.post(addr+"/delete_image", data='{"url":"' + str(name)+'"}')
    print(*r)


def generatePasswordHash(password):
    key = hashlib.pbkdf2_hmac('sha256', password.encode(
        'utf-8'), salt, 100000, dklen=128)
    return key


def checkPasswordHash(password, hash):
    current_key = generatePasswordHash(password)
    if current_key == hash:
        return True
    else:
        return False


def generateToken(power):
    return secrets.token_hex(power)


def makeQrCode(data):
    img = qrcode.make(data)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_code = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return sendImageToMediaServer(qr_code)
