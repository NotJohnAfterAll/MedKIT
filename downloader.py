from yt_dlp import YoutubeDL

def formats_selector(ctx):
    formats = ctx.get('formats')[::-1]

    

def list_resolutions(url):
    ydl_opts = {}
    with YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(url, download=False) 

    formats = meta.get('formats', [])
    resolution_to_id = {}
    for f in formats:
        res = f.get('resolution')
        print(f)
        




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
video_url = "https://www.instagram.com/p/DD5kT5qxdjZ/"
list_resolutions(video_url)
