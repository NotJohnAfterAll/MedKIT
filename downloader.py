from yt_dlp import YoutubeDL
import ffmpeg
import os
from datetime import datetime
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
import convertor as cc
import re
from rich import print
from rich.console import Console

console = Console()

scriptColor = "magenta"
scriptSecondaryColor = "dark_magenta"
errorColor = "red"
successColor = "green"

def Download():
    print(f"[bold {scriptColor}]MedKIT Downloader:[/] Select what you want to download: (video, audio)")
    options = {
        "video": VideoDownload,
        "audio": AudioDownload
    }

    completer = WordCompleter(options.keys(), ignore_case=True)
    
    while True:
        choice = prompt("Select an option: ", completer=completer).strip().lower()
        if choice in options:
            options[choice]()
            break
        else:
            print(f"[bold {errorColor}]MedKIT Downloader:[/] Invalid choice. Try again.")

def VideoDownload():
    print(f"[bold {scriptColor}]MedKIT Downloader:[/] Select how you want to download: (best quality, resolution selector) - PLAYLISTS ARE NOT SUPPORTED NOW")
    options = {
        "best quality": VideoDownloadBestQuality,
        "resolution selector": VideoDownloadWithSelector
    }

    completer = WordCompleter(options.keys(), ignore_case=True)
    
    while True:
        choice = prompt("Select an option: ", completer=completer).strip().lower()
        if choice in options:
            options[choice]()
            exit()
        else:
            print(f"[bold {errorColor}]MedKIT Downloader:[/] Invalid choice. Try again.")

def AudioDownload():
    print(f"[bold {scriptColor}]MedKIT Downloader:[/] Select how you want to download: (best quality, playlist)")
    options = {
        "best quality": AudioDownloadBestQuality,
        "playlist": AudioDownloadPlaylist
    }

    completer = WordCompleter(options.keys(), ignore_case=True)
    
    while True:
        choice = prompt("Select an option: ", completer=completer).strip().lower()
        if choice in options:
            options[choice]()
            exit()
        else:
            print(f"[bold {errorColor}]MedKIT Downloader:[/] Invalid choice. Try again.")
            
            
def AudioDownloadPlaylist():
    url = input("Enter URL: ")
    title = getTitle(url)
    urls = getPlaylistUrls(url)
    files = getPlaylistAudioTitles(url)
    dirname = f"{title}"
    dirname = re.sub(r'[<>:"/\\|?*]', '', dirname)
    
    if dirname in os.listdir("."):
        dirname = f"{dirname} {datetime.now().strftime("%Y%m%d-%H%M%S")}"
    
    os.mkdir(dirname)
    os.chdir(dirname)
    
    index = 1
    for url in urls:
        try:
            print(f"[bold {scriptSecondaryColor}]MedKIT Downloader:[/] Downloading entry {index}/{len(urls)}")
            audioDownload(url, audioQtySelector(url))
        except:
            print(f"[bold {errorColor}]MedKIT Downloader:[/] This entry is unavailable... continuing")
        index += 1
        if "[Deleted video]" in url:
            files.remove('[Deleted video]')
        
    cc.PostAudioDownloadConvertPlaylist(dirname, os.listdir("."))

def AudioDownloadBestQuality():
    url = input("Enter URL: ")
    title = getTitle(url)
    filename = f"{title}.m4a"
    
    audioDownload(url, audioQtySelector(url))
    cc.PostAudioDownloadConvert(filename, title)
    

def videoResSelector(url, title):
    ydl_opts = {
        'noplaylist': True,
        'quiet': True,
        'skip_download': True
    }
    with YoutubeDL(ydl_opts) as ydl:
        data = ydl.extract_info(url, download=False) 

    print(f"[bold {scriptSecondaryColor}]MedKIT Downloader:[/] Available resolutions for {title}: ")
    formats = data.get('formats', [])
    usrToID = {}
    id = 1;

    for f in formats:
        
        if f.get('resolution') != 'audio only' and ('vp' in f.get('vcodec') or 'avc1' in f.get('vcodec')) and f.get('fps') > 23 and f.get('ext') == "mp4":
            usrToID.update({id : f.get('format_id')})
            console.print(id, f.get('resolution'), f"{int(f.get('tbr'))}k", highlight=False)
            id = id + 1
        else:
            continue
        
    usrInput = input("Enter number coresponding to your selected resolution and bitrate:")        
    return usrToID[int(usrInput)]
        

def videoBestQualitySelector(url, title):
    ydl_opts = {
        'quiet': True,
        'skip_download': True
    }
    with YoutubeDL(ydl_opts) as ydl:
        data = ydl.extract_info(url, download=False) 

    formats = data.get('formats', [])

    for f in formats:
        if f.get('resolution') != 'audio only' and ('vp' in f.get('vcodec') or 'avc1' in f.get('vcodec')) and f.get('fps') > 23 and f.get('ext') == "mp4" and len(f.get('format_id')) == 3:
            selectedResolution = f.get('resolution')
            selectedFormat = f.get('format_id')
        else:
            continue
        
    print(f"[bold {scriptSecondaryColor}]MedKIT Downloader:[/] Downloading best quality possible for {title}, being {selectedResolution}: ")
    return selectedFormat


def VideoDownloadBestQuality():
    url = input("Enter URL: ")
    title = getTitle(url)
    
    videoDownload(url, videoBestQualitySelector(url, title))
    print(f"[bold {successColor}]MedKIT Downloader:[/] Video downloaded successfully, you can find it in this directory named {title}")


def VideoDownloadWithSelector():
    url = input("Enter URL: ")
    title = getTitle(url)
    
    videoDownload(url, videoResSelector(url, title))
    print(f"[bold {successColor}]MedKIT Downloader:[/] Video downloaded successfully, you can find it in this directory named {title}")


def videoDownload(url, formatID):
    audioFormatID = audioQtySelector(url)
    combinedID_tuple = (formatID, audioFormatID)
    combinedID = '+'.join(combinedID_tuple)
    print(f"[bold {scriptSecondaryColor}]MedKIT Downloader:[/] Downloading video and audio track... ")
    ydl_opts = {
        'outtmpl': "%(title)s.%(ext)s",
        'noplaylist': True,
        'quiet': True,
        'format': combinedID,
        'progress':True,
        'no-warnings': True
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)
    

def audioDownload(url, formatID):
    print(f"[bold {scriptSecondaryColor}]MedKIT Downloader:[/] Downloading audio track... ")
    ydl_opts = {
        'outtmpl': "%(title)s.%(ext)s",
        'quiet': True,
        'format': formatID,
        'progress':True,
        'no-warnings': True
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)


def audioQtySelector(url) :
    ydl_opts = {
        'quiet': True,
        'skip_download': True
    }
    with YoutubeDL(ydl_opts) as ydl:
        data = ydl.extract_info(url, download=False) 

    formats = data.get('formats', [])
    multipletracks = ""

    for f in formats:
        if len(f.get('format_id')) == 5:
            multipletracks = "original"
        
    for f in formats:
        if f.get('resolution') == 'audio only' and f.get('ext') == "m4a" and multipletracks in f.get('format_note') and len(f.get('format_id')) <= 5:
            return f.get('format_id')
        else:
            continue

def getTitle(url):
    ydl_opts = {'quiet': True, 'noplaylist': True, 'skip_download': True, 'no-warnings': True, 'ignoreerrors': True}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info.get('title')  
        
def getPlaylistUrls(url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'skip_download': True,
        'no-warnings': True
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return [entry['url'] for entry in info.get('entries', []) if 'url' in entry]


def getPlaylistAudioTitles(url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'skip_download': True,
        'no-warnings': True
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        titles = []
        for entry in info.get('entries'):
            titles.append(entry['title'])
        return titles

if __name__ == "__main__":
    print(audioQtySelector("https://www.youtube.com/watch?v=d-4JJbk3ZS0"))