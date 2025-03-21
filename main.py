import downloader as dl
import convertor as cc
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
import threading

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
    print("Welcome to MedKIT")
    print("Select what you want to do: (download, convert)")
    main_menu()


#BUILD SCRIPT
#pyinstaller.exe --onefile --specpath .\build\ -n MedKIT .\main.py