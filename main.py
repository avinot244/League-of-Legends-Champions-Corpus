from packages.model import DataEntry
from packages.utils import saveToJson
from packages.ui.interface import displayHeader

from colorama import Fore, Back, Style

import os

if __name__ == "__main__":
    temp : DataEntry = DataEntry("this is a text", "champion", "role")

    # saveToJson(temp, "./dataset.json")

    
    exit_flag = False
    while not(exit_flag):
        displayHeader()

        # Getting the text
        print(Back.WHITE + Fore.BLACK + "Enter the text (-1 for exit) :", end="")
        print(Style.RESET_ALL)
        text : str = input()
        exit_flag = text == "-1"

        # Getting the champion
        print(Back.WHITE + Fore.BLACK + "Enter the champion (-1 for exit) :", end="")
        print(Style.RESET_ALL)
        champion : str = input()
        exit_flag = text == "-1"

        # Getting the role
        print(Back.WHITE + Fore.BLACK + "Enter the role (-1 for exit) :", end="")
        print(Style.RESET_ALL)
        role : str = input()
        exit_flag = text == "-1"

        if not(exit_flag):
            data : DataEntry = DataEntry(text, champion, role)
        
        saveToJson(data, "./dataset.json")


