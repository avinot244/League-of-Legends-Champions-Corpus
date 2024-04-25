from packages.model import DataEntry
from packages.utils import saveToJson

from colorama import Fore, Back, Style
import os

if __name__ == "__main__":
    temp : DataEntry = DataEntry("this is a text", "champion", "role")

    # saveToJson(temp, "./dataset.json")
    print(Fore.RED + Back.WHITE + "HELLO" + Style.RESET_ALL)


    exit_flag = False

    while not(exit_flag):
        os.system('clear')
        
