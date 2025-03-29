import downloader as dl
import convertor as cc
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
import threading
import os
from rich import print

scriptColor = "blue"
errorColor = "red"
successColor = "green"

def download():
    dl.Download()

def convert():
    threading.Thread(target=cc.Convert()).start()

def exit_program():
    print(f"[bold {errorColor}]MedKIT:[/] Exiting...")
    input("Press any key to continue...")
    exit()

def main_menu():
    options = {
        "download": download,
        "convert": convert,
        "exit": exit_program
    }

    completer = WordCompleter(options.keys(), ignore_case=True)
    
    while True:
        choice = prompt("Select an option: ", completer=completer).strip()
        if choice in options:
            options[choice]()
            if input(f"[bold {scriptColor}]MedKIT:[/] Do you want to download/convert another? (n/Y): ").lower() == "n":
                exit_program()

        else:
            print(f"[bold {errorColor}]MedKIT:[/] Invalid choice. Try again.")

if __name__ == "__main__":
    try:
        print(f"Welcome to [bold {scriptColor}]MedKIT[/]")
        print(f"[bold {scriptColor}]MedKIT:[/] Select what you want to do: (download, convert)")

        main_menu()
    except KeyboardInterrupt:
        print(f"\n[bold {errorColor}]MedKIT:[/] Interrupted... exiting...")
        os._exit(130)


#BUILD SCRIPT
#pyinstaller.exe --onefile --specpath .\build\ -n MedKIT .\main.py