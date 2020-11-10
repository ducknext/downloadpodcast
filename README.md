# Download videos from a YouTube and Podbean channel

The script reads channel IDs from a Json file `.podcast_channels.json` which has been created by the user int the same folder as the python script. 
The channels Json file has the following structure with few example channels:

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


If there is a new channel added to the list then on the first run with this new channel the script will save all video IDs as already downloaded without downloading them. It goes with the assumption that you are up to date with the channel and want to download only new videos.


On every next run it will download those videos which hasn't been downloaded already.
