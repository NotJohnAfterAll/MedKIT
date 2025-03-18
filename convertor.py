import tkinter.filedialog
import tkinter as tk
import ffmpeg
import tkinter
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
import os
import sys

sys.coinit_flags = 2  # COINIT_APARTMENTTHREADED

def getFile():
    print("Function started")
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    root.update()
    root.call('wm', 'attributes', '.', '-topmost', True)
    print("update")
    file = tkinter.filedialog.askopenfilename(filetypes=[("Media", ".mp4 .mov .mkv .avi .webm")])

    if file == "":
        raise ValueError("File is empty")
    
    return file

def setTargetFormat(format):
    global targetFormat
    targetFormat = format

def ConvertVideo():
    formats = ["mp4", "mov", "mkv", "avi", "webm"]
    file = getFile()
    fileFormat = file.split(".")[-1].lower()
    formats.remove(fileFormat)
    userSelection(formats)
    print("past user selecion")

    if targetFormat == "":
        raise ValueError("Invalid File")

    print("past target check")
    convert(file, targetFormat)

def convert(filepath, targetFormat):
    workdir = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    filename = filename.rsplit(".", 1)[0]
    filename = f"{filename}.{targetFormat}"
    os.chdir(workdir)

    input = ffmpeg.input(filepath, hwaccel='cuda')
    ffmpeg.output(input, filename).run()

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
    ConvertVideo()
