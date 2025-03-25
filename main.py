import downloader as dl
import convertor as cc
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
import threading
import os

def download():
    dl.Download()
    
def downloadAudio():
    print("Downloading Audio...")

def convert():
    threading.Thread(target=cc.Convert()).start()

def transcode():
    print("Transcoding...")

def exit_program():
    print("Exiting...")
    exit()

def main_menu():
    options = {
        "download": download,
        "convert": convert,
        "transcode": transcode,
        "exit": exit_program
    }

    completer = WordCompleter(options.keys(), ignore_case=True)
    
    while True:
        choice = prompt("Select an option: ", completer=completer).strip()
        if choice in options:
            options[choice]()
            exit()
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    try:
        print("Welcome to MedKIT")
        print("Select what you want to do: (download, convert)")

        currentDir = os.path.dirname(os.path.abspath(__file__))
        ffmpegBin = os.path.join(currentDir, 'build', 'ffmpeg', 'bin')
        os.environ['PATH'] += os.pathsep + ffmpegBin

        main_menu()
        print("Exiting...")
        input("Press any key to continue...")
    except KeyboardInterrupt:
        print("Interrupted... exiting...")
        os._exit(130)


#BUILD SCRIPT
#pyinstaller.exe --onefile --specpath .\build\ -n MedKIT .\main.py