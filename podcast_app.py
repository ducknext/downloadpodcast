#!/usr/bin/env python3

from __future__ import unicode_literals
import youtube_dl
from bs4 import BeautifulSoup
import requests
import json
import os


def get_youtube_link_ids(channel_id):
    page = requests.get(
        'https://www.youtube.com/feeds/videos.xml?channel_id={}'
        .format(channel_id))
    soupeddata = BeautifulSoup(page.content, 'html.parser')

    return [x.string for x in soupeddata.find_all('yt:videoid')]


def get_podbean_links(channel_id):
    page = requests.get(
        'https://feed.podbean.com/{}/feed.xml'.format(channel_id))
    soupeddata = BeautifulSoup(page.content, 'html.parser')

    return [a.get('url') for a in soupeddata.find_all('enclosure')]


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


def download_youtube_file(video, downloads, channel, downloads_file_path):

    ydl_opts = {
        'audio-format': 'bestaudio/best',
        'outtmpl': '%(title)s-%(uploader)s-%(id)s.%(ext)s',
        'noplaylist': True,
        'progress_hooks': [my_hook],
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(
                ['https://www.youtube.com/watch?v={}'.format(video)])

        downloads.append({"id": video, "channel": channel})
        dump_file(downloads, downloads_file_path)
    except youtube_dl.utils.DownloadError:
        print("Youtube Error with link https://www.youtube.com/watch?v={}"
              .format(video))


def download_podbean_file(video, downloads, channel, downloads_file_path):
    title = str(video).split('/')[-1]

    print('Downloading {}...'.format(title))

    response = requests.get(video, stream=True)
    if response.status_code == 200:
        handle = open(title, "wb")
        for chunk in response.iter_content(chunk_size=512):
            if chunk:  # filter out keep-alive new chunks
                handle.write(chunk)

        print('Download done')

        downloads.append({"id": video, "channel": channel})
        dump_file(downloads, downloads_file_path)
    else:
        print("PodBean Error with link {}".format(video))


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


def first_time_channel(channel, video_ids, downloads_file_path):
    downloads = load_file_or_default(downloads_file_path,[],)

    if not any(download['channel'] == channel for download in downloads):
        for video in video_ids:
            downloads.append({"id": video, "channel": channel})
        dump_file(downloads, downloads_file_path)


def youtube_channel(channel, downloads_file_path):
    video_ids = get_youtube_link_ids(channel)

    first_time_channel(channel, video_ids, downloads_file_path)

    for video in video_ids:
        downloads = load_file_or_default(downloads_file_path,[],)

        if video not in [download['id'] for download in downloads]:
            download_youtube_file(
                video, downloads, channel, downloads_file_path)


def podbean_channel(channel, downloads_file_path):
    links = get_podbean_links(channel)

    first_time_channel(channel, links, downloads_file_path)

    for video in links:
        downloads = load_file_or_default(downloads_file_path,[],)

        if video not in [download['id'] for download in downloads]:
            download_podbean_file(
                video, downloads, channel, downloads_file_path)


def main():
    called_from = os.path.dirname(os.path.realpath(__file__))
    channels_file_path = called_from + '/' + '.podcast_channels.json'
    downloads_file_path = called_from + '/' + '.podcast_downloads.json'

    for channel in load_file_or_fail(channels_file_path):

        if channel['site'] == 'youtube':
            youtube_channel(channel['id'], downloads_file_path)

        if channel['site'] == 'podbean':
            podbean_channel(channel['id'], downloads_file_path)


if __name__ == "__main__":
    main()
