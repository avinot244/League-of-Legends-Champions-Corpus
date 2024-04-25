import os
from colorama import Fore, Back, Style

def displayHeader():
    os.system("clear")
    print(Fore.CYAN + f"{'':#^50}")
    print(Fore.CYAN + "#" + f"{' Data Input ': ^48}" + "#")
    print(Fore.CYAN + f"{'':#^50}")



    print(Style.RESET_ALL)