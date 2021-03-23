from telethon import TelegramClient
import os
import shutil
import sys
from Crypto.Cipher import AES
from hashlib import sha256
import base64

api_id = os.environ['API_ID']
api_hash = os.environ['API_HASH']
chat = os.environ['CHAT']
client = TelegramClient('telegram_client', api_id, api_hash)
secret = sha256(os.environ['SECRET'].encode('utf-8')).digest()
secret_hash = sha256(secret).hexdigest()
cipher = AES.new(secret, AES.MODE_EAX)
nonce = cipher.nonce


async def main(type):
    if type == 'backup':
        if os.path.isfile('db.bak'):
            os.remove('db.bak')
        if os.path.isfile('db.enc'):
            os.remove('db.enc')
        shutil.copy('db.sqlite3', 'db.bak')
        with open('db.bak', 'rb') as file1:
            with open('db.enc', 'wb') as file2:
                while data := file1.read(512):
                    ciphertext, tag = cipher.encrypt_and_digest(data)
                    file2.write(data)
        file = await client.upload_file('db.enc')
        await client.send_message(chat, f'nonce:base64:{base64.b64encode(nonce).decode()}\n'
                                        f'secret:sha256:{secret_hash}',
                                  file=file)
        os.remove('db.bak')
        os.remove('db.enc')
    elif type == 'boot':
        await client.send_message(chat, 'booted')


def run(type):
    with client:
        client.loop.run_until_complete(main(type))


if __name__ == '__main__':
    run(sys.argv[1])
