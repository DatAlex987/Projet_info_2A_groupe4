# from utils.reset_database import ResetDatabase
from view.accueilview import AccueilView
from colorama import Fore, Style

# from business_object.user import User
# from dao.user_dao import UserDAO
# import datetime

view = AccueilView()

banner_start = (
    f"{Fore.CYAN}{'~' * 100}\n"
    f"{Fore.WHITE}{' ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ '.center(100)}\n"
    f"{Fore.MAGENTA}{Style.BRIGHT}{'WELCOME TO THE DM SOUND S BUDDY'.center(100)}\n"
    f"{Fore.BLUE}{'Enhance your Roleplay experience'.center(100)}\n"
    f"{Fore.WHITE}{' ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ '.center(100)}\n"
    f"{Fore.CYAN}{'~' * 100}{Style.RESET_ALL}\n"
)
print(banner_start)

while view:
    view.display_info()
    view = view.make_choice()

# Insérer la suppression des objets orphelins ici

banner_quit = (
    f"{Fore.CYAN}{'~' * 100}\n"
    f"{Fore.WHITE}{' ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ '.center(100)}\n"
    f"{Fore.MAGENTA}{Style.BRIGHT}{'The sounds will miss you...'.center(100)}\n"
    f"{Fore.BLUE}{'and so will we!'.center(100)}\n"
    f"{Fore.WHITE}{' ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ '.center(100)}\n"
    f"{Fore.CYAN}{'~' * 100}{Style.RESET_ALL}\n"
)
print(banner_quit)

# pip install pygame
