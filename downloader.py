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
    return usrToID.get(usrInput)
    usrInput = 4
    
    ydl_opts = {
        'quiet': False,
        'format': usrToID.get(usrInput)
    }
    with YoutubeDL(ydl_opts) as ydl:
        data = ydl.download(url) 
    
    #print(formats)
        

def MasterDownload(url):
    now = datetime.now() 
    tempDirName = str(now.strftime("%d/%m/%Y %H:%M:%S"))
    os.mkdir(tempDirName)
    os.chdir(tempDirName)
    
    
    Download(url, videoResSelector(url))
        
    


def videoDownload(url, formatID):
    ydl_opts = {
        'outtmpl': "video.%(ext)s",
        'quiet': False,
        'format': formatID
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)
    
## UDELAT AUDIO DOWNLOAD A VE WORKDIR POTOM MERGNOUT DO JEDNOHO SOUBORU... DODELAT INTEGRACI DO MAIN.PY.... SMAZAT NEPOTREBNY FUNKCE


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
    video_url = "https://www.youtube.com/watch?v=MZZSMaEAC2g"
    videoResSelector(video_url)
#list_formats(video_url)


def test():
    now = datetime.now() 
    print(str(now.strftime("%d/%m/%Y %H:%M:%S")))
    
