import tkinter.filedialog
import ffmpeg
import tkinter
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

def getFile():
    file = tkinter.filedialog.askopenfilename(filetypes=[("Media", ".mp4 .mov .mkv .avi .webm")])
    if file != "":
        return file
    else:
        print("Error occured")

def setTargetFormat(format):
    global targetFormat
    targetFormat = format

def convertVideo():
    formats = ["mp4", "mov", "mkv", "avi", "webm"]
    file = getFile()
    fileFormat = file.split(".")
    fileFormat = fileFormat[1].lower()
    formats.remove(fileFormat)
    userSelection(formats)

    print(targetFormat) //DOESNT WORK

def userSelection(formats):
    formatsClean = ' '.join(map(str, formats))
    print(f"Select to what format you want to convert: {formatsClean}")
    options = {format: (lambda fmt=format: setTargetFormat(fmt)) for format in formats}
    print(targetFormat)
    completer = WordCompleter(options.keys(), ignore_case=True)
    
    while True:
        choice = prompt("Select an option: ", completer=completer).strip().lower()
        if choice in options:
            options[choice]()
            exit()
        else:
            print("Invalid choice. Try again.")
    



if __name__ == "__main__":
    convertVideo()
