#!/usr/bin/env python3

from __future__ import unicode_literals
import youtube_dl
from bs4 import BeautifulSoup
from urllib.request import urlopen
import logging
import csv

logging.basicConfig(filename="podcastAppLog.log")


def csv_to_list(csv_file):
    full_csv_data = []
    with open(csv_file) as csv_file:
        csvReader = csv.reader(csv_file, delimiter=',')
        for row in csvReader:
            full_csv_data.append(row)

    csv_data_first = []
    for line in full_csv_data:
        csv_data_first.append(line[0])

    return csv_data_first


def download(video_id, saved_videos):
    ydl_opts = {
        'audio-format': 'bestaudio/best',
        # 'extractaudio': True,  # only keep the video
        # 'audioformat': 'mp3',  # convert to mp3
        'outtmpl': '%(id)s-%(uploader)s-%(title)s.%(ext)s',  # name the file
        'noplaylist': True,  # only single video, not playlist
    }

    # TODO errors!
    if video_id in saved_videos:
        return "Already downloaded"

    if len(video_id) != 11:
        return "Faulty ID"

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['https://www.youtube.com/watch?v={}'.format(video_id)])

    save_row = [video_id]
    with open('yt_downloads.csv', 'a') as write_obj:
        csv_writer = csv.writer(write_obj)
        csv_writer.writerow(save_row)

    return None


def get_meta():

    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(
            'https://www.youtube.com/watch?v=dP15zlyra3c', download=False)

    print(meta)


def get_youtube_link_ids(channel_id):
    html = urlopen('https://www.youtube.com/feeds/videos.xml?channel_id={}'.format(channel_id))
    soupeddata = BeautifulSoup(html, 'html.parser')
    full_yt_video_id = soupeddata.find_all('yt:videoid')

    video_ids = []
    for x in full_yt_video_id:
        x = str(x)
        x = x.lstrip('<yt:videoid>')
        x = x.rstrip('</yt:videoid>')
        video_ids.append(x)

    return video_ids


def main():
    channel_ids = csv_to_list('yt_channels.csv')
    saved_videos = csv_to_list('yt_downloads.csv')

    for channel in channel_ids:
        video_ids = get_youtube_link_ids(channel)

        for video in video_ids:
            err = download(video, saved_videos)
            if err:
                logging.info("Video ID {} for channel ID {} failed".format(video, channel))


if __name__ == "__main__":
    main()
