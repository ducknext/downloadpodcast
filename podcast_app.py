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
        # 'extractaudio': True,  # only keep the video
        # 'audioformat': 'mp3',  # convert to mp3
        'outtmpl': '%(id)s-%(uploader)s-%(title)s.%(ext)s',  # name the file
        'noplaylist': True,  # only single video, not playlist
        'progress_hooks': [my_hook],
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(['https://www.youtube.com/watch?v={}'.format(video_id)])
    except youtube_dl.utils.DownloadError:
        print("Youtube Error")


def main():
    with open('.podcast_channels.json') as f:
        channels = json.load(f)

    for channel in channels:
        video_ids = get_youtube_link_ids(channel['id'])

        for video in video_ids:
            with open('.podcast_downloads.json') as f:
                downloads = json.load(f)

            download_ids = []
            for item in downloads:
                download_ids.append(item['id'])

            if video not in download_ids:

                err = download(video)
                if err:
                    return err
                downloads.append({"id": video})

            with open('.podcast_downloads.json', 'w') as f:
                json.dump(downloads, f)


if __name__ == "__main__":
    main()
