"""Ce module implémente la view dédiée la consultation d'un son d'un autre utilisateur"""

from colorama import Fore, Style
from InquirerPy import prompt
from view.abstractview import AbstractView
from service.session import Session
from business_object.son_aleatoire import Son_Aleatoire
from business_object.son_continu import Son_Continu
from business_object.son_manuel import Son_Manuel

# from service.sd_service import SDService
# from service.scene_service import SceneService
from service.son_service import SonService


class MenuConsulterInfoSonSelectView(AbstractView):
    """Classe représentant la view de la consultation d'un son"""

    def __init__(self):
        super().__init__()

        self.question = [
            {
                "type": "list",
                "name": "choix",
                "message": "Que souhaitez-vous faire",
                "choices": ["Ecouter le son", "Revenir au menu de consultation des sons"],
            }
        ]

    def make_choice(self):
        if isinstance(Session().son_to_consult, Son_Aleatoire):
            SonService().afficher_details_son_aleatoire(son_aleatoire=Session().son_to_consult)
        elif isinstance(Session().son_to_consult, Son_Manuel):
            SonService().afficher_details_son_manuel(son_manuel=Session().son_to_consult)
        elif isinstance(Session().son_to_consult, Son_Continu):
            SonService().afficher_details_son_continu(son_continu=Session().son_to_consult)
        answer = prompt(self.question)
        if answer["choix"] == "Ecouter le son":
            SonService().previsualiser_son_consult(son=Session().son_to_consult)
        elif answer["choix"] == "Revenir au menu de consultation des sons":
            pass
        from view.view_consulter_user.consulter_son_view import MenuConsulterSonsView

        return MenuConsulterSonsView()

    def display_info(self):
        print(Fore.BLUE + " [PARAMETRAGE] MENU SON ".center(80, "=") + Style.RESET_ALL)
