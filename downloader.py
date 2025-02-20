from yt_dlp import YoutubeDL
import ffmpeg
import os
import shutil
from datetime import datetime

   

def videoResSelector(url, title):
    ydl_opts = {
        'quiet': True
    }
    with YoutubeDL(ydl_opts) as ydl:
        data = ydl.extract_info(url, download=False) 

    print(f"Available resolutions for {title}: ")
    formats = data.get('formats', [])
    
    usrToID = {}
    id = 1;


    for f in formats:
        
        if f.get('resolution') != 'audio only' and "vp" in f.get('vcodec') and f.get('fps') > 23 and f.get('ext') == "mp4":
            usrToID.update({id : f.get('format_id')})
            print(id, f.get('resolution'), f"{int(f.get('tbr'))}k")
            id = id + 1
        else:
            continue
        
        
    usrInput = input("Enter number coresponding to your selected resolution and quality:")        
    return usrToID[int(usrInput)]
        

def VideoDownloadWithSelector():
    url = input("Enter URL: ")
    title = getTitle(url)
    now = datetime.now() 
    tempDirName = str(now.strftime("%d_%m_%Y_%H%M%S"))

    os.mkdir(tempDirName)
    os.chdir(tempDirName)
    
    videoDownload(url, videoResSelector(url, title))
    audioDownload(url, audioQtySelector(url))

    
    MergeTracks()

    dTitle = title.replace(" ", "_")
    os.rename("output.mp4", dTitle + '.mp4')
    shutil.move(f"./{dTitle}.mp4", f"../{dTitle}.mp4")
    os.chdir("../")
    shutil.rmtree(tempDirName, ignore_errors=True)


def MergeTracks():
    print("Merging audio and video tracks... ")
    video = ffmpeg.input('video.mp4', hwaccel='cuda')
    audio = ffmpeg.input('audio.m4a', hwaccel='cuda')

    ffmpeg.output(video, audio, "output.mp4",  vcodec='copy', acodec='aac', strict='experimental', shortest=None, loglevel='info').run(overwrite_output=True)


def videoDownload(url, formatID):
    print("Downloading video track... ")
    ydl_opts = {
        'outtmpl': "video.%(ext)s",
        'quiet': True,
        'format': formatID
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
    url = "https://www.youtube.com/watch?v=doFViKgl-y0"
    print(str(getTitle(url)) + '.mp4')


def test():
    now = datetime.now() 
    print(str(now.strftime("%d/%m/%Y %H:%M:%S")))

