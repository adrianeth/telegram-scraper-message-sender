from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError
import configparser
import os, sys
import csv
import random
import time

re="\033[1;31m"
gr="\033[1;32m"
cy="\033[1;36m"
ye="\033[1;33m"
SLEEP_TIME = 30

class main():

    def banner():
        
        print(f"""
    {cy}
█████████████████████████████████████▀███████████████████████████████████████████████
█▄─▀█▀─▄█▄─▄▄─█─▄▄▄▄█─▄▄▄▄██▀▄─██─▄▄▄▄█▄─▄▄─███─▄▄▄▄█▄─▄▄─█▄─▀█▄─▄█▄─▄▄▀█▄─▄▄─█▄─▄▄▀█
██─█▄█─███─▄█▀█▄▄▄▄─█▄▄▄▄─██─▀─██─██▄─██─▄█▀███▄▄▄▄─██─▄█▀██─█▄▀─███─██─██─▄█▀██─▄─▄█
▀▄▄▄▀▄▄▄▀▄▄▄▄▄▀▄▄▄▄▄▀▄▄▄▄▄▀▄▄▀▄▄▀▄▄▄▄▄▀▄▄▄▄▄▀▀▀▄▄▄▄▄▀▄▄▄▄▄▀▄▄▄▀▀▄▄▀▄▄▄▄▀▀▄▄▄▄▄▀▄▄▀▄▄▀
            """)

    def send_dms():
        try:
            cpass = configparser.RawConfigParser()
            cpass.read('config.data')
            api_id = cpass['cred']['id']
            api_hash = cpass['cred']['hash']
            phone = cpass['cred']['phone']
        except KeyError:
            os.system('clear')
            main.banner()
            print(re+"Run python setup.py first!\n")
            sys.exit(1)

        client = TelegramClient(phone, api_id, api_hash)
         
        client.connect()
        if not client.is_user_authorized():
            client.send_code_request(phone)
            os.system('clear')
            main.banner()
            client.sign_in(phone, input(ye+'Enter the code from Telegram: '+re))
        
        os.system('clear')
        main.banner()
        input_file = sys.argv[1]
        users = []
        with open(input_file, encoding='UTF-8') as f:
            rows = csv.reader(f,delimiter=",",lineterminator="\n")
            next(rows, None)
            for row in rows:
                user = {}
                user['username'] = row[0]
                user['id'] = int(row[1])
                user['access_hash'] = int(row[2])
                user['name'] = row[3]
                users.append(user)
        print(cy+"[1] send DMs by user ID\n[2] send DMs by username")
        mode = int(input(cy+"Input : "+re))
         
        message = input(ye+"Enter Your Message: "+re)
         
        for user in users:
            if mode == 2:
                if user['username'] == "":
                    continue
                receiver = client.get_input_entity(user['username'])
            elif mode == 1:
                receiver = InputPeerUser(user['id'],user['access_hash'])
            else:
                print(re+"Invalid Mode. Exiting.")
                client.disconnect()
                sys.exit()
            try:
                print(ye+"Sending message to:", user['name'])
                client.send_message(receiver, message.format(user['name']))
                print(cy+"Waiting {} seconds".format(SLEEP_TIME))
                time.sleep(SLEEP_TIME)
            except PeerFloodError:
                print(re+"Getting Flood Error from Telegram. \nScript is stopping now. \n Please try again after some time or setup a new account.")
                client.disconnect()
                sys.exit()
            except Exception as e:
                print(re+"Error:", e)
                print(re+"Trying to continue..")
                continue
        client.disconnect()
        print("Done. Message sent to all targets.")



main.send_dms()
