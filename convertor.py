import tkinter.filedialog
import tkinter as tk
import ffmpeg
import tkinter
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
import os
import sys

sys.coinit_flags = 2  # COINIT_APARTMENTTHREADED

def Convert():
    print("Select what file type you want to download (video, audio, image): ")
    options = {
        "video": ConvertVideo,
        "audio": ConvertAudio,
        "image": ConvertImage
    }

    completer = WordCompleter(options.keys(), ignore_case=True)
    
    while True:
        choice = prompt("Select an option: ", completer=completer).strip()
        if choice in options:
            options[choice]()
            exit()
        else:
            print("Invalid choice. Try again.")


def getFile(type):
    types = {
        "video": ("Videos", ".mp4 .mov .mkv .avi .webm"),
        "audio": ("Audio", ".mp3 .flac .wav .m4a .ogg .webm .acc"),
        "image": ("Images", ".jpg .jpeg .png .webp .svg .avif .ico")
    }
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    root.update()
    root.call('wm', 'attributes', '.', '-topmost', True)
    file = tkinter.filedialog.askopenfilename(filetypes=[types[type]])

    if file == "":
        raise ValueError("File is empty")
    
    return file

def setTargetFormat(format):
    global targetFormat
    targetFormat = format

def ConvertVideo():
    formats = ["mp4", "mov", "mkv", "avi", "webm"]
    file = getFile("video")
    fileFormat = file.split(".")[-1].lower()
    formats.remove(fileFormat)
    userSelection(formats)

    if targetFormat == "":
        raise ValueError("Invalid File")

    convert(file, targetFormat)

def ConvertAudio():
    formats = ["mp3", "flac", "wav", "m4a", "ogg", "webm", "acc"]
    file = getFile("audio")
    fileFormat = file.split(".")[-1].lower()
    formats.remove(fileFormat)
    userSelection(formats)

    if targetFormat == "":
        raise ValueError("Invalid File")

    convert(file, targetFormat)

def ConvertImage():
    formats = ["jpg", "jpeg", "png", "webp", "svg", "avif", "ico"]
    file = getFile("image")
    fileFormat = file.split(".")[-1].lower()
    formats.remove(fileFormat)
    userSelection(formats)

    if targetFormat == "":
        raise ValueError("Invalid File")

    stillconvert(file, targetFormat)

def convert(filepath, targetFormat):
    workdir = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    filename = filename.rsplit(".", 1)[0]
    filename = f"{filename}.{targetFormat}"
    os.chdir(workdir)

    input = ffmpeg.input(filepath, hwaccel='cuda')
    ffmpeg.output(input, filename).run()

    print(f"Your file has been successfully converted, you can find it in same directory called '{filename}'")

def stillconvert(filepath, targetFormat):
    workdir = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    filename = filename.rsplit(".", 1)[0]
    filename = f"{filename}.{targetFormat}"
    os.chdir(workdir)


    input = ffmpeg.input(filepath, hwaccel='cuda')
    ffmpeg.output(input, filename, vframes=1).run()
    
    
    print(f"\n Your file has been successfully converted, you can find it in same directory called '{filename}'")

def userSelection(formats):
    formatsClean = ' '.join(map(str, formats))
    print(f"Select to what format you want to convert: {formatsClean}")
    options = {format: (lambda fmt=format: setTargetFormat(fmt)) for format in formats}
    
    completer = WordCompleter(options.keys(), ignore_case=True)
    
    while True:
        choice = prompt("Select an option: ", completer=completer).strip().lower()

        if choice not in options:
            raise ValueError("Invalid choice. Try again")
        options[choice]()
        break
    
def PostAudioDownloadConvertPlaylist(dirname, files):
    formats = ["mp3", "flac", "wav", "ogg", "webm", "acc"]
    if postDownloadConvertUserSelection(formats) == 0:
        print(f"Playlist downloaded successfully, new folder has been created for your playlist files called '{dirname}'")
        exit()
        
    print("Converting your playlist now, please wait...")
        
    index = 0
    for file in files:
        file = f"{file}.m4a"
        print(f"Convering entry {index}/{len(files)}")
        postAudioDownloadConvert(file, targetFormat)
        index += 1
    print(f"Playlist downloaded and converted successfully, new folder has been created for your playlist files called '{dirname}'")
    
def PostAudioDownloadConvert(file, title):
    formats = ["mp3", "flac", "wav", "ogg", "webm", "acc"]
    if postDownloadConvertUserSelection(formats) == 0:
        print(f"Audio downloaded successfully, you can find it in this directory named {title}")
        exit()
    
    postAudioDownloadConvert(file, targetFormat)
    print(f"Your file has been successfully downloaded and converted, you can find it in same directory called '{file}.{targetFormat}'")
    
def postDownloadConvertUserSelection(formats):
    print("What file format you want your audio to be? Hit enter for skip (m4a) or select from following (mp3, flac, wav, ogg, webm, acc)")
    options = {format: (lambda fmt=format: setTargetFormat(fmt)) for format in formats}
    
    completer = WordCompleter(options.keys(), ignore_case=True)
    
    while True:
        choice = prompt("Select an option: ", completer=completer).strip().lower()

        if choice not in options and choice != "":
            raise ValueError("Invalid choice. Try again")
        elif choice == "":
            return 0
        options[choice]()
        break
    
def postAudioDownloadConvert(filepath, targetFormat):
    oldfile = os.path.basename(filepath)
    filename = os.path.basename(filepath)
    filename = filename.rsplit(".", 1)[0]
    filename = f"{filename}.{targetFormat}"

    input = ffmpeg.input(filepath, hwaccel='cuda')
    ffmpeg.output(input, filename, loglevel="quiet").run()
    os.remove(oldfile)


if __name__ == "__main__":
    Convert()
