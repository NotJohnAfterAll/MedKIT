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
    print("Select what file type you want to download (audio, video): ")
    options = {
        "audio": ConvertAudio,
        "video": ConvertVideo
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
        "audio": ("Audio", ".mp3 .flac .wav .m4a .ogg .webm .acc")
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


def convert(filepath, targetFormat):
    workdir = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    filename = filename.rsplit(".", 1)[0]
    filename = f"{filename}.{targetFormat}"
    os.chdir(workdir)

    input = ffmpeg.input(filepath, hwaccel='cuda')
    ffmpeg.output(input, filename).run()

    print(f"Your file has been successfully converted, you can find it in same directory called '{filename}'")

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
    

if __name__ == "__main__":
    Convert()
