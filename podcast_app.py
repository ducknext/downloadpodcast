#!/usr/bin/env python3

import youtube_dl
from bs4 import BeautifulSoup
import requests
import json
import os

"""
All script is about downloading files.
To shorten the variable names the word 'download' is shortened to 'dl'
"""


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


def download_youtube_file(
        video, dl_channels, dl_files, dl_content, channel, dl_file_path):

    ydl_opts = {
        'audio-format': 'bestaudio/best',
        'outtmpl': '%(title)s-%(uploader)s-%(id)s.%(ext)s',
        'noplaylist': True,
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

        dl_files.append({"id": video, "channel": channel})
        dl_content['downloads'] = dl_files
        dl_content['channels'] = dl_channels

        dump_file(dl_content, dl_file_path)

    except youtube_dl.utils.DownloadError:
        print("Youtube Error with link https://www.youtube.com/watch?v={}"
              .format(video))


def download_podbean_file(
        video, dl_channels, dl_files, dl_content, channel, dl_file_path):

    title = str(video).split('/')[-1]

    print('Downloading {}...'.format(title))

    response = requests.get(video, stream=True)

    if response.status_code == 200:
        handle = open(title, "wb")
        for chunk in response.iter_content(chunk_size=512):
            if chunk:  # filter out keep-alive new chunks
                handle.write(chunk)

        print('Download done')

        dl_files.append({"id": video, "channel": channel})
        dl_content['downloads'] = dl_files
        dl_content['channels'] = dl_channels

        dump_file(dl_content, dl_file_path)

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


def first_time_channel(channel, dl_channels, dl_files, video_ids):

    if channel not in dl_channels:
        dl_channels.append(channel)
        for video in video_ids:
            dl_files.append({"id": video, "channel": channel})

    return dl_channels, dl_files


def download_all_videos(channel, dl_channels, dl_files, dl_content,
                        dl_file_path, video_ids, dl_file):

    dl_channels, dl_files = first_time_channel(
        channel, dl_channels, dl_files, video_ids)

    for video in video_ids:
        if video not in [download['id'] for download in dl_files]:
            dl_file(video, dl_channels, dl_files, dl_content,
                    channel, dl_file_path)


def main():
    called_from = os.path.dirname(os.path.realpath(__file__))
    channels_file_path = called_from + '/' + '.podcast_channels.json'
    dl_file_path = called_from + '/' + '.podcast_downloads.json'

    dl_content = load_file_or_default(dl_file_path, [])
    dl_channels = dl_content['channels']
    dl_files = dl_content['downloads']

    for channel in load_file_or_fail(channels_file_path):
        if channel['site'] == 'youtube':
            video_ids = get_youtube_link_ids(channel['id'])
            download_all_videos(
                channel['id'],
                dl_channels,
                dl_files,
                dl_content,
                dl_file_path,
                video_ids,
                download_youtube_file
            )

        if channel['site'] == 'podbean':
            video_ids = get_podbean_links(channel['id'])
            download_all_videos(
                channel['id'],
                dl_channels,
                dl_files,
                dl_content,
                dl_file_path,
                video_ids,
                download_podbean_file
            )


if __name__ == "__main__":
    main()
