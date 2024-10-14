import json
import requests
import threading
import time

with open('co.json', 'r') as json_file:
    config = json.load(json_file)

msg = config['messagecount']
message = config['message']
chid = config['channelid']

with open('token.txt', 'r') as token_file:
    tokens = [line.strip().replace('"', '') for line in token_file.readlines()]

def send_message(token, chid, message):
    url = f'https://discord.com/api/v10/channels/{chid}/messages'
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    data = {
        'content': message
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print(f"{token} message sent")
    elif response.status_code == 401:
        print(f"{token} failed to send message (invalid token)")
    elif response.status_code == 403:
        print(f"{token} failed to send message (mb bot protection on the channel)")
    else:
        print(f"{token} failed to send message (response: {response.text})")

def send_messages_concurrently(token):
    for _ in range(msg):
        send_message(token, chid, message)
        time.sleep(0)

threads = []
for token in tokens:
    thread = threading.Thread(target=send_messages_concurrently, args=(token,))
    threads.append(thread)
    thread.start()
for thread in threads:
    thread.join()

print("done")
