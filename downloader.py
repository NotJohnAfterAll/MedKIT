from yt_dlp import YoutubeDL
import ffmpeg
import os
from datetime import datetime

   

def videoResSelector(url):
    ydl_opts = {
        'quiet': True
    }
    with YoutubeDL(ydl_opts) as ydl:
        data = ydl.extract_info(url, download=False) 

    print("Available resolutions for " + getTitle(url) + ":")
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
    usrInput = 4
    
    ydl_opts = {
        'quiet': False,
        'format': usrToID.get(usrInput)
    }
    with YoutubeDL(ydl_opts) as ydl:
        data = ydl.download(url) 
    
    #print(formats)
        

def VideoDownloadWithSelector(url):
    now = datetime.now() 
    tempDirName = str(now.strftime("%d_%m_%Y_%H%M%S"))
    os.mkdir(tempDirName)
    os.chdir(tempDirName)
    
    videoDownload(url, videoResSelector(url))
    audioDownload(url, audioQtySelector(url))

       
    MergeTracks()

    ##ffmpeg.input("video.mp4").input("audio.m4a").output("output.mp4", vcodec="copy", acodec="copy", strict="experimental").run(overwrite_output=True)


    ##outputstream = ffmpeg.output(ffmpeg.input("./video.mp4"), ffmpeg.input("./audio.m4a"), (str(getTitle(url)) + '.mp4'), vcodec='copy', acodec='copy')
    ##ffmpeg.run(outputstream, quiet=False)


    ##ffmpeg.concat("./video", "./audio", v=1, a=1).output((str(getTitle(url)) + '.mp4')).run()
    
    ##NEFUNGUJE FFMPEG INPUT KURVAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

def MergeTracks():
    print(os.getcwd())
    ffmpeg.input("video.mp4").input("audio.m4a").output(
        "output.mp4",
        vcodec='copy',
        acodec='aac',
        strict='experimental',
        shortest=None  # Ensures output stops at the shortest track length
    ).run(overwrite_output=True)


def videoDownload(url, formatID):
    ydl_opts = {
        'outtmpl': "video.%(ext)s",
        'quiet': False,
        'format': formatID
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)
    
## UDELAT AUDIO DOWNLOAD A VE WORKDIR POTOM MERGNOUT DO JEDNOHO SOUBORU... DODELAT INTEGRACI DO MAIN.PY.... SMAZAT NEPOTREBNY FUNKCE

def audioDownload(url, formatID):
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


def list_formats(url):
    options = {
        'quiet': True,  # Suppress command-line output
        'listformats': True  # Display available formats
    }
    with YoutubeDL(options) as ydl:
        try:
            ydl.extract_info(url, download=False)
        except Exception as e:
            print(f"Error: {e}")

# Example usage
if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=doFViKgl-y0"
    print(str(getTitle(url)) + '.mp4')
#list_formats(video_url)


def test():
    now = datetime.now() 
    print(str(now.strftime("%d/%m/%Y %H:%M:%S")))

