from view.abstractview import AbstractView
from colorama import Fore, Style
from InquirerPy import prompt

####
from service.user_service import UserService
from service.sd_service import SDService

####
from view.abstractview import AbstractView
from view.session import Session

# from view.view_consulter_user.menu_consulter_createur_view import ConsulterCreateurView
# from view.view_consulter_user.menu_consulter_nom_view import ConsulterNomView


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

            next_view = ConsulterChoixSD()  # Il faut la créer
        return next_view

    def display_info(self):
        print(Fore.BLUE + " MENU DE CONSULTATION [SD] ".center(80, "=") + Style.RESET_ALL)
