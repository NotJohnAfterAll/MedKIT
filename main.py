import downloader as dl
import convertor as cc
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
import threading

def downloadVideo():
    
    print("Select how you want to download: (BEST QUALITY, RESOLUTION SELECTOR)")
    options = {
        "best quality": dl.VideoDownloadBestQuality,
        "resolution selector": dl.VideoDownloadWithSelector
    }

    completer = WordCompleter(options.keys(), ignore_case=True)
    
    while True:
        choice = prompt("Select an option: ", completer=completer).strip().lower()
        if choice in options:
            options[choice]()
            exit()
        else:
            print("Invalid choice. Try again.")

    
def downloadAudio():
    print("Downloading Audio...")

def convert():
    threading.Thread(target=cc.ConvertVideo()).start()

def transcode():
    print("Transcoding...")

def exit_program():
    print("Exiting...")
    exit()

def main_menu():
    options = {
        "downloadvideo": downloadVideo,
        "downloadaudio": downloadAudio,
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
    print("Select what you want to do: (DOWNLOAD VIDEO - DV, DOWNLOAD AUDIO - DA, CONVERT - CC, TRANSCODE = TS)")
    main_menu()

