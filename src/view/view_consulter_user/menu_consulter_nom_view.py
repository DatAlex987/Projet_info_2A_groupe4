from view.abstractview import AbstractView
from colorama import Fore, Style
from InquirerPy import prompt

####
from service.sd_service import SDService

####
from view.abstractview import AbstractView
from view.view_consulter_user.consulter_sds_view import ConsulterSDsView

# from view.view_consulter_user.menu_consulter_createur_view import ConsulterCreateurView
# from view.view_consulter_user.menu_consulter_nom_view import ConsulterNomView


class ConsulterNomView(AbstractView):
    "test"

    def __init__(self):
        super().__init__()
        self.question_sd = [
            {
                "type": "input",
                "name": "nom",
                "message": "Entrez le nom de la Sound-deck souhaitée :",
            },
        ]

    def make_choice(self):
        nom_approx = prompt(self.question_sd)
        SDService().FindCloseNameSDs(nom_approx=nom_approx["nom"], schema="ProjetInfo")
        return ConsulterSDsView()

    def display_info(self):
        print(Fore.BLUE + " [JEU] MENU RECHERCHE NOM ".center(80, "=") + Style.RESET_ALL)
