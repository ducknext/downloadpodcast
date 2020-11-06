#!/usr/bin/env python3

from __future__ import unicode_literals
import youtube_dl
from bs4 import BeautifulSoup
from urllib.request import urlopen
import json


def get_youtube_link_ids(channel_id):
    html = urlopen('https://www.youtube.com/feeds/videos.xml?channel_id={}'.format(channel_id))
    soupeddata = BeautifulSoup(html, 'html.parser')
    full_yt_video_id = soupeddata.find_all('yt:videoid')

    video_ids = []
    for x in full_yt_video_id:
        x = str(x)
        x = x.split('<yt:videoid>')
        x = x[1].split('</yt:videoid>')
        video_ids.append(x[0])

    return video_ids


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


def download(video_id):
    ydl_opts = {
        'audio-format': 'bestaudio/best',
        'outtmpl': '%(id)s-%(uploader)s-%(title)s.%(ext)s',  # name the file
        'noplaylist': True,  # only single video, not playlist
        'progress_hooks': [my_hook],
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(['https://www.youtube.com/watch?v={}'.format(video_id)])
    except youtube_dl.utils.DownloadError:
        print("Youtube Error")


def dump_file(data_dump, file_name):
    with open(file_name, 'w') as f:
        json.dump(data_dump, f)


def load_file(file_name):
    try:
        with open(file_name) as f:
            file_data = json.load(f)
        return file_data
    except:  # noqa
        return 'Can not find file {}'.format(file_name)


def main():
    channels = load_file('.podcast_channels.json')
    if not channels:
        return

    for channel in channels:
        video_ids = get_youtube_link_ids(channel['id'])

        for video in video_ids:
            downloads = load_file('.podcast_downloads.json')
            if not downloads:
                dump_file([{"id": 'place_holder'}], '.podcast_downloads.json')

            download_ids = []
            for item in downloads:
                download_ids.append(item['id'])

            if video not in download_ids:

                err = download(video)
                if err:
                    return err
                downloads.append({"id": video})

            dump_file(downloads, '.podcast_downloads.json')


if __name__ == "__main__":
    main()
