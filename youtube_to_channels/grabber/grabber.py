import requests
import os
import sys
import json

from importlib import resources
from models.channel import Channel

__session = requests.Session()

def __grab(url):
    response = __session.get(url, timeout=15).text
    if '.m3u8' not in response:
        response = requests.get(url).text
        if '.m3u8' not in response:
            os.system(f'curl "{url}" > temp.txt')
            response = ''.join(open('temp.txt').readlines())
            if '.m3u8' not in response:
                return
    end = response.find('.m3u8') + 5
    tuner = 100
    while True:
        if 'https://' in response[end-tuner : end]:
            link = response[end-tuner : end]
            start = link.find('https://')
            end = link.find('.m3u8') + 5
            break
        else:
            tuner += 5
    
    return f"{link[start : end]}"

def channel_from(data):
    stream = __grab(data['url'])

    return Channel(
        data['id'],
        data['name'],
        stream,
        data['logo'],
        'youtube'
    )

def fetch_channels():
    resource = resources.files("resources").joinpath("channels_list.json")
    
    with resources.open_text("resources", "channels_list.json") as file:
        data = json.load(file)

        channels = list(map(channel_from, data))

        if 'temp.txt' in os.listdir():
            os.system('rm temp.txt')
            os.system('rm watch*')

        channels = [channel for channel in channels if channel.url is not None]
        return list(map(lambda channel: channel._asdict(), channels))
