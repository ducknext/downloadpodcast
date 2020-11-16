# Download videos from YouTube and PodBean channels

The script reads channel IDs from a Json file `.podcast_channels.json` which has been created by the user in the same folder as the python script. 
The `.podcast_channels.json` has the following structure:

```
[
    {"id": "UCkB8eF4ATHl4Jm1BeCZgQ9A", "name": "Uneducated Economist", "site": "youtube"},
    {"id": "UC9ZM3N0ybRtp44-WLqsW3iQ", "name": "Mark Moss", "site": "youtube"},
    {"id": "UCpvyOqtEc86X8w8_Se0t4-w", "name": "George Gammon", "site": "youtube"},
    {"id": "UC0iTb2U2nWkm5X3XRityENw", "name": "WallStForMainSt", "site": "youtube"},
    {"id": "ttmygh", "name": "ttmygh", "site": "podbean"}
]

```

The script uses RSS feed link to find the most recent videos for a channel.


If there is a new channel added to the list then on the first run with this new channel the script will save all video IDs as already downloaded without downloading them. It goes with the assumption that the user is up to date with the channel and wants to download only the new videos.


On every next run it will download only those videos which hasn't been downloaded already.


For the script to succesfully convert to mp3 `ffmpeg` is needed. For Linux Ubuntu:

```
sudo apt install ffmpeg
```
