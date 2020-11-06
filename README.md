# Download videos from youtube channel

The script reads channel IDs from a Json file `.podcast_channels.json` created by the user. 
The Json file has the following structure with few example channels:

```
[
    {"id": "UCkB8eF4ATHl4Jm1BeCZgQ9A", "name": "Uneducated Economist"},
    {"id": "UC9ZM3N0ybRtp44-WLqsW3iQ", "name": "Mark Moss"},
    {"id": "UCpvyOqtEc86X8w8_Se0t4-w", "name": "George Gammon"},
    {"id": "UC0iTb2U2nWkm5X3XRityENw", "name": "WallStForMainSt"}
]

```

The script uses RSS feed link to find the most recent videos and download those which hasn't been downloaded already.
