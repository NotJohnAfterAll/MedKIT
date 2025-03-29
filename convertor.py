import tkinter.filedialog
import tkinter as tk
import ffmpeg
import tkinter
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
import os
import sys
from rich import print

sys.coinit_flags = 2  # COINIT_APARTMENTTHREADED
scriptColor = "yellow"
scriptSecondaryColor = "gold"
errorColor = "red"
successColor = "green"

types = {
        "video": ("Videos", ".mp4 .mov .mkv .avi .webm"),
        "audio": ("Audio", ".mp3 .flac .wav .m4a .ogg .webm .acc"),
        "image": ("Images", ".jpg .jpeg .png .webp .avif .ico"),
        "media": ("Media", ".mp4 .mov .mkv .avi .webm .mp3 .flac .wav .m4a .ogg .webm .acc" ),
        "any": ("Media", ".mp4 .mov .mkv .avi .webm .mp3 .flac .wav .m4a .ogg .webm .acc .jpg .jpeg .png .webp .avif .ico" )
    }

filetypes = {
    "video": ["mp4", "mov", "mkv", "avi", "webm"],
    "audio": ["mp3", "flac", "wav", "m4a", "ogg", "webm", "acc"],
    "image": ["jpg", "jpeg", "png", "webp", "avif", "ico"],
    "any": ["mp4", "mov", "mkv", "avi", "webm", "mp3", "flac", "wav", "m4a", "ogg", "acc"]
}

manualCovertOptions = {
    "vcodecs": ["h264", "h265", "av1"],
    "acodecs": ["aac", "mp3", "flac", "alac", ]
}

manualCovertOptionsFFmpeg = {
    "h264": "libx264",
    "h265": "libx265",
    "av1": "libaom-av1"
}

def Convert():
    print(f"[bold {scriptColor}]MedKIT Convertor:[/] Select your way to convert: (auto, manual, extract audio): ")
    options = {
        "manual": ManualConvert,
        "auto": AutoConvert,
        "extract audio": ExtractAudio
    }

    completer = WordCompleter(options.keys(), ignore_case=True)
    
    while True:
        choice = prompt("Select an option: ", completer=completer).strip()
        if choice in options:
            options[choice]()
            break
        else:
            print(f"[bold {errorColor}]MedKIT Convertor:[/] Invalid choice. Try again.")

def ExtractAudio():
    file = getFile("video")
    targetFormat = userSelection(filetypes["audio"], "format")
    convert(file, targetFormat)

def AutoConvert():
    file = getFile("any")
    fileFormat = file.split(".")[-1].lower()
    fileCategory = getFileCategory(fileFormat) 
    formats = filetypes[fileCategory]
    formats.remove(fileFormat)
    targetFormat = userSelection(formats, "format")

    if fileCategory == "image":
        stillconvert(file, targetFormat)
    else:
        convert(file, targetFormat)

def ManualConvert():
    formats = filetypes["any"]
    file = getFile("media")
    fileFormat = file.split(".")[-1].lower()
    formats.remove(fileFormat)
    targetFormat = userSelection(formats, "format")

    if getFileCategory(targetFormat) == "video" : manualConvert('video', file, targetFormat)
    else: manualConvert('audio', file, targetFormat)

def manualConvert(type, file, targetFormat):
    workdir = os.path.dirname(file)
    filename = os.path.basename(file).rsplit(".", 1)[0]
    filename = f"{filename}.{targetFormat}"

    os.chdir(workdir)

    vcodec = "copy"
    vbitrate = "0"
    acodec = "copy"

    if type == "video":
        vcodec = manualCovertOptionsFFmpeg[userSelection(manualCovertOptions["vcodecs"], "codec")]
        vbitrate = f"{input(f'[bold {scriptSecondaryColor}]MedKIT Convertor:[/] Enter video bitrate in thousands (6000 = 6000k): ')}k"
        nvencPresent = f"{input(f'[bold {scriptSecondaryColor}]MedKIT Convertor:[/] Do you have GPU with NVENC encoder? (y/N): ')}k"
        if nvencPresent.lower() == "y":
            vbitrate = f"{vbitrate}_nvenc"
        acodec = userSelection(manualCovertOptions["acodecs"], "codec")
    
    abitrate = f"{input(f'[bold {scriptSecondaryColor}]MedKIT Convertor:[/] Enter audio bitrate in thousands (320 = 320k): ')}k"

    ffmpeg_input = ffmpeg.input(file, hwaccel='cuda')
    ffmpeg.output(ffmpeg_input, filename, vcodec=vcodec, acodec=acodec, audio_bitrate=abitrate, video_bitrate=vbitrate).run()

    print(f"[bold {successColor}]MedKIT Convertor:[/] Your file has been successfully converted, you can find it in same directory called '{filename}'")

def getFileCategory(fileFormat):
    for type, extention in filetypes.items():
        for ext in extention:
            if ext == fileFormat:
                return type

def getFile(type):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    root.update()
    root.call('wm', 'attributes', '.', '-topmost', True)
    file = tkinter.filedialog.askopenfilename(filetypes=[types[type]])

    if file == "":
        raise ValueError(f"[bold {errorColor}]MedKIT Convertor:[/] File is empty")
    
    return file

def convert(filepath, targetFormat):
    workdir = os.path.dirname(filepath)
    filename = os.path.basename(filepath).rsplit(".", 1)[0]
    filename = f"{filename}.{targetFormat}"
    os.chdir(workdir)

    input = ffmpeg.input(filepath, hwaccel='auto')
    ffmpeg.output(input, filename).run()

    print(f"[bold {successColor}]MedKIT Convertor:[/] Your file has been successfully converted, you can find it in same directory called '{filename}'")

def stillconvert(filepath, targetFormat):
    workdir = os.path.dirname(filepath)
    filename = os.path.basename(filepath).rsplit(".", 1)[0]
    filename = f"{filename}.{targetFormat}"
    os.chdir(workdir)

    input = ffmpeg.input(filepath, hwaccel='auto')
    ffmpeg.output(input, filename, vframes=1).run()
    
    print(f"\n [bold {successColor}]MedKIT Convertor:[/] Your file has been successfully converted, you can find it in same directory called '{filename}'")

def userSelection(formats, txt):
    formatsClean = ' '.join(map(str, formats))
    print(f"[bold {scriptSecondaryColor}]MedKIT Convertor:[/] Select to what {txt} you want to convert: {formatsClean}")
    
    options = {format: (lambda fmt=format: fmt) for format in formats}
    completer = WordCompleter(options.keys(), ignore_case=True)
    
    while True:
        choice = prompt("Select an option: ", completer=completer).strip().lower()

        if choice not in options:
            raise ValueError(f"[bold {errorColor}]MedKIT Convertor:[/] Invalid choice. Try again")
        options[choice]()
        print(choice)
        return choice
        break
    
def PostAudioDownloadConvertPlaylist(dirname, files):
    targetFormat = postDownloadConvertUserSelection(filetypes["audio"])
    if targetFormat == 0:
        print(f"[bold {successColor}]MedKIT Convertor:[/] Playlist downloaded successfully, new folder has been created for your playlist files called '{dirname}'")
        exit()
        
    print(f"[bold {scriptColor}]MedKIT Convertor:[/] Converting your playlist now, please wait...")
        
    index = 0
    for file in files:
        print(f"Convering entry {index}/{len(files)}")
        postAudioDownloadConvert(file, targetFormat)
        index += 1
    print(f"[bold {successColor}]MedKIT Convertor:[/] Playlist downloaded and converted successfully, new folder has been created for your playlist files called '{dirname}'")
    
def PostAudioDownloadConvert(file, title):
    targetFormat = postDownloadConvertUserSelection(filetypes["audio"])
    if targetFormat == 0:
        print(f"[bold {successColor}]MedKIT Convertor:[/] Audio downloaded successfully, you can find it in this directory named {title}")
        exit()
    
    postAudioDownloadConvert(file, targetFormat)
    print(f"[bold {successColor}]MedKIT Convertor:[/] Your file has been successfully downloaded and converted, you can find it in same directory called '{file}.{targetFormat}'")
    
def postDownloadConvertUserSelection(formats):
    print(f"[bold {scriptSecondaryColor}]MedKIT Convertor:[/] What file format you want your audio to be? Hit enter for skip (m4a) or select from following (mp3, flac, wav, ogg, webm, acc)")
    options = {format: (lambda fmt=format: fmt) for format in formats}
    completer = WordCompleter(options.keys(), ignore_case=True)
    
    while True:
        choice = prompt("Select an option: ", completer=completer).strip().lower()
        if choice not in options and choice != "":
            raise ValueError(f"[bold {errorColor}]MedKIT Convertor:[/] Invalid choice. Try again")
        elif choice == "":
            return 0
        options[choice]()
        break
    
def postAudioDownloadConvert(filepath, targetFormat):
    oldfile = os.path.basename(filepath)
    filename = os.path.basename(filepath).rsplit(".", 1)[0]
    filename = f"{filename}.{targetFormat}"

    input = ffmpeg.input(filepath, hwaccel='auto')
    ffmpeg.output(input, filename, loglevel="quiet").run()
    os.remove(oldfile)


if __name__ == "__main__":
    Convert()
