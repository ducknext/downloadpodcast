#!/usr/bin/env python3

from __future__ import unicode_literals
import youtube_dl
from bs4 import BeautifulSoup
import requests
import json


def get_youtube_link_ids(channel_id):
    page = requests.get('https://www.youtube.com/feeds/videos.xml?channel_id={}'.format(channel_id))
    soupeddata = BeautifulSoup(page.content, 'html.parser')

    return [x.string for x in soupeddata.find_all('yt:videoid')]


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


def download(video, downloads):
    ydl_opts = {
        'audio-format': 'bestaudio/best',
        'outtmpl': '%(id)s-%(uploader)s-%(title)s.%(ext)s',  # name the file
        'noplaylist': True,  # only single video, not playlist
        'progress_hooks': [my_hook],
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(
                ['https://www.youtube.com/watch?v={}'.format(video)])

        downloads.append({"id": video})
        dump_file(downloads, '.podcast_downloadsss.json')
    except youtube_dl.utils.DownloadError:
        print("Youtube Error with link https://www.youtube.com/watch?v={}".format(video))


def dump_file(data_dump, file_name):
    with open(file_name, 'w') as f:
        json.dump(data_dump, f)


def load_file_or_fail(file_name):
    try:
        with open(file_name) as f:
            return json.load(f)
    except:  # noqa
        print('Can not find file {}'.format(file_name))
        exit(1)


def load_file_or_default(file_name, place_holder):
    try:
        with open(file_name) as f:
            return json.load(f)
    except:  # noqa
        dump_file(place_holder, file_name)
        with open(file_name) as f:
            return json.load(f)


def main():
    for channel in load_file_or_fail('.podcast_channels.json'):
        video_ids = get_youtube_link_ids(channel['id'])

        for video in video_ids:
            downloads = load_file_or_default(
                '.podcast_downloadsss.json',
                [{"id": 'place_holder'}],
            )
            if not any(download['id'] == video for download in downloads):
                download(video, downloads)


if __name__ == "__main__":
    main()
