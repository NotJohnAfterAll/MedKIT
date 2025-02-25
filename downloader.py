from yt_dlp import YoutubeDL
import ffmpeg
import os
import shutil
from datetime import datetime

   

def videoResSelector(url, title):
    ydl_opts = {
        'noplaylist': True,
        'quiet': True
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
        'quiet': True
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
        'format': combinedID
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)
    

def audioDownload(url, formatID):
    print("Downloading audio track... ")
    ydl_opts = {
        'outtmpl': "audio.%(ext)s",
        'quiet': False,
        'format': formatID
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)


def audioQtySelector(url) :
    ydl_opts = {
        'quiet': True
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
    ydl_opts = {'quiet': True, 'noplaylist': True}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info.get('title')  
        


if __name__ == "__main__":
    VideoDownloadBestQuality()


def test():
    now = datetime.now() 
    print(str(now.strftime("%d/%m/%Y %H:%M:%S")))

