from yt_dlp import YoutubeDL
import ffmpeg
import os
import shutil
from datetime import datetime
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
import convertor as cc

def Download():
    print("Select how you want to download: (video, audio)")
    options = {
        "video": VideoDownload,
        "audio": AudioDownload
    }

    completer = WordCompleter(options.keys(), ignore_case=True)
    
    while True:
        choice = prompt("Select an option: ", completer=completer).strip().lower()
        if choice in options:
            options[choice]()
            exit()
        else:
            print("Invalid choice. Try again.")

def VideoDownload():

    print("Select how you want to download: (best quality, resolution selector) - PLAYLISTS ARE NOT SUPPORTED NOW")
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
            print("Invalid choice. Try again.")

def AudioDownload():

    print("Select how you want to download: (best quality, playlist)")
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
            print("Invalid choice. Try again.")
            
            
def AudioDownloadPlaylist():
    url = input("Enter URL: ")
    title = getTitle(url)
    urls = getPlaylistUrls(url)
    files = getPlaylistAudioTitles(url)
    dirname = f"{title} - MedKIT"
    
    if dirname in os.listdir("."):
        dirname = f"{dirname} {datetime.now().strftime("%Y%m%d-%H%M%S")}"
    
    os.mkdir(dirname)
    os.chdir(dirname)
    
    index = 1
    for url in urls:
        print(f"Downloading entry {index}/{len(urls)}")
        audioDownload(url, audioQtySelector(url))
        index += 1
    
    cc.PostDownloadConvertPlaylist(dirname, files)
    
    print(f"Playlist downloaded successfully, new folder has been created for your playlist files called '{dirname}'")

def AudioDownloadBestQuality():
    url = input("Enter URL: ")
    title = getTitle(url)
    filename = f"{title}.m4a"
    
    audioDownload(url, audioQtySelector(url))
    cc.PostDownloadConvert(filename, title)
    


def videoResSelector(url, title):
    ydl_opts = {
        'noplaylist': True,
        'quiet': True,
        'skip_download': True
    }
    with YoutubeDL(ydl_opts) as ydl:
        data = ydl.extract_info(url, download=False) 

    print(f"Available resolutions for {title}: ")
    formats = data.get('formats', [])
    usrToID = {}
    id = 1;


    for f in formats:
        
        if f.get('resolution') != 'audio only' and ('vp' in f.get('vcodec') or 'avc1' in f.get('vcodec')) and f.get('fps') > 23 and f.get('ext') == "mp4":
            usrToID.update({id : f.get('format_id')})
            print(id, f.get('resolution'), f"{int(f.get('tbr'))}k")
            id = id + 1
        else:
            continue
        
        
    usrInput = input("Enter number coresponding to your selected resolution and quality:")        
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
        
    print(f"Downloading best quality possible for {title}, being {selectedResolution}: ")
    return selectedFormat

def VideoDownloadBestQuality():
    url = input("Enter URL: ")
    title = getTitle(url)
    
    videoDownload(url, videoBestQualitySelector(url, title))
    print(f"Video downloaded successfully, you can find it in this directory named {title}")


def VideoDownloadWithSelector():
    url = input("Enter URL: ")
    title = getTitle(url)
    
    videoDownload(url, videoResSelector(url, title))
    print(f"Video downloaded successfully, you can find it in this directory named {title}")


def MergeTracks():
    print("Merging audio and video tracks... ")
    video = ffmpeg.input('video.mp4', hwaccel='cuda')
    audio = ffmpeg.input('audio.m4a', hwaccel='cuda')

    ffmpeg.output(video, audio, "output.mp4",  vcodec='copy', acodec='aac', strict='experimental', shortest=None, loglevel='info').run(overwrite_output=True)


def videoDownload(url, formatID):
    audioFormatID = audioQtySelector(url)
    combinedID_tuple = (formatID, audioFormatID)
    combinedID = '+'.join(combinedID_tuple)
    print("Downloading video and audio tracks... ")
    ydl_opts = {
        'noplaylist': True,
        'quiet': True,
        'format': combinedID,
        'progress':True
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)
    

def audioDownload(url, formatID):
    print("Downloading audio track... ")
    ydl_opts = {
        'outtmpl': "%(title)s.%(ext)s",
        'quiet': True,
        'format': formatID,
        'progress':True
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

    for f in formats:
        if f.get('resolution') == 'audio only' and f.get('ext') == "m4a" and len(f.get('format_id')) == 3:
            return f.get('format_id')
        else:
            continue

def getTitle(url):
    ydl_opts = {'quiet': True, 'noplaylist': True, 'skip_download': True, 'no-warnings': True}
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
    getPlaylistAudioTitles("https://music.youtube.com/playlist?list=PL5jddfnHUMMX3RKNFu-xngVGufOGxtCZ0")


def test():
    now = datetime.now() 
    print(str(now.strftime("%d/%m/%Y %H:%M:%S")))

