# phdl
`phdl` is a small `youtube-dl` front end which enhances ease of use with a popular video sharing website. Download videos and organize by user, automatically, using simple drag and drop. No typing required.

## Getting Started
### Prerequisites
- Python 3
- watchdog
- youtube-dl

### Installing
Simply place `phdl.py` somewhere in your $PATH, or call it directly.

### Usage
```
phdl.py [-h] [--keeplinks] [--watchdir WATCHDIR] [outdir]

Saves some videos in a tidy directory structure

positional arguments:
  outdir               The root directory where saved videos will be organized
                       [default: ./]

optional arguments:
  -h, --help           show this help message and exit
  --keeplinks          Don't delete shortcut files after download
  --watchdir WATCHDIR  The directory that will be watched for new download
                       links [default: outdir]
```

In Windows you can drag and drop a URL from your favorite web browser to a File Explorer window to create an internet shortcut. `phdl` monitors a directory of your choosing for these shortcuts, instructs `youtube-dl` to download the videos, places them into appropriate subdirectories, and cleans up the shortcut files.

For example, you could run

```
phdl.py --watchdir /path/to/watch/ /path/to/save/
```

to monitor the directory `/path/to/watch/`. Open a File Explorer window and navigate to `/path/to/watch/`. Open a web browser, pull up popular video sharing hub, and find some videos to save. You find an interesting video by `User 12345`. Grab the URL, drag it over to the File Explorer window, and drop it right in there. `phdl` detects the shortcut, downloads the video, saves it to `/path/to/save/user-12345/`, and deletes the internet shortcut you just created.