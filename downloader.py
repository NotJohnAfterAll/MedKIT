from yt_dlp import YoutubeDL
import ffmpeg

    

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
        
    return usrToID
    usrInput = 4
    
    ydl_opts = {
        'quiet': False,
        'format': usrToID.get(usrInput)
    }
    with YoutubeDL(ydl_opts) as ydl:
        data = ydl.download(url) 
    
    #print(formats)
        

def download(url, formatID):
    ydl_opts = {
        'quiet': False,
        'format': formatID
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(url) 
        
        ## DOPSAT DOWNLOADER SCRIPT POTOM MERGER


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
