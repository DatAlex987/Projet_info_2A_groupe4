from colorama import Fore, Style
from InquirerPy import prompt

####
from service.sd_service import SDService
from service.session import Session

####
from view.abstractview import AbstractView


class ConsulterSDsView(AbstractView):

    def __init__(self):
        super().__init__()
        self.question = [
            {
                "type": "list",
                "name": "Choix SD",
                "message": (
                    "Quelle Sound-deck souhaitez-vous consulter ? \n"
                    " ID   |      Nom       |    Description               "
                    "| Date de création \n"
                    "-------------------------------------------------------------"
                    "---------------------"
                ),
                "choices": SDService().formatage_question_sds_to_consult(),
            }
        ]

    def make_choice(self):
        choix = prompt(self.question)
        if choix["Choix SD"] == "Retour au menu de recherche de consultation":
            from view.view_consulter_user.menuconsulteruser import MenuConsulterUserView

            next_view = MenuConsulterUserView()
        else:
            id_sd_select = choix["Choix SD"].split()[1]
            Session().sd_to_consult = SDService().instancier_sd_par_id(
                id_sd=id_sd_select, schema="ProjetInfo"
            )
            from view.view_consulter_user.consulter_choix_sd import ConsulterChoixSD

            next_view = ConsulterChoixSD()
        return next_view

    def display_info(self):
        print(Fore.BLUE + " [JEU] MENU SOUND-DECK ".center(80, "=") + Style.RESET_ALL)
