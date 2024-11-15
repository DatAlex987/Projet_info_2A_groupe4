"""Ce module implémente la view dédiée à l'ajout d'un son de l'utilisateur"""

from colorama import Fore, Style
from InquirerPy import prompt
from view.abstractview import AbstractView
from view.session import Session

# from service.sd_service import SDService
# from service.scene_service import SceneService
from service.son_service import SonService


class MenuParamAjoutSonView(AbstractView):
    """Classe représentant la view d'un son à une scène"""

    def __init__(self):
        super().__init__()

        self.question_description = [
            {
                "type": "input",
                "name": "desc",
                "message": "Donnez une description à votre son:",
            }
        ]
        self.question_type_son = [
            {
                "type": "list",
                "name": "type son",
                "message": "Quel sera le type de ce son ?",
                "choices": ["Son aléatoire", "Son continu", "Son manuel"],
            }
        ]
        self.question_param_alea = [
            {
                "type": "input",
                "name": "param alea min",
                "message": "Entrez le temps minimal à attendre avant que le son se rejoue aléatoirement (en secondes) :",
            },
            {
                "type": "input",
                "name": "param alea max",
                "message": "Entrez le temps maximal à attendre avant que le son se rejoue aléatoirement (en secondes):",
            },
        ]
        self.question_param_manuel = [
            {
                "type": "input",
                "name": "param manuel key",
                "message": "Entrez la lettre de la touche du clavier pour déclencher le son:",
            },
        ]

    def make_choice(self):  # NON TESTE YET
        son_desc = prompt(self.question_description)
        Session().son_to_dl["description"] = son_desc["desc"]
        choix_type = prompt(self.question_type_son)
        if choix_type["type son"] == "Son aléatoire":
            choix_param = prompt(self.question_param_alea)
            param1 = choix_param["param alea min"]
            param2 = choix_param["param alea max"]
        elif choix_type["type son"] == "Son manuel":
            choix_param = prompt(self.question_param_manuel)
            param1 = choix_param["param manuel key"]
            param2 = None
        elif choix_type["type son"] == "Son continu":
            param1 = None
            param2 = None
        # On stocke ces nouvelles infos en session pour les utiliser ensuite pour l'ajout en DAO
        Session().son_to_dl["type_son"] = choix_type["type son"]
        Session().son_to_dl["param1"] = param1
        Session().son_to_dl["param2"] = param2
        if SonService().ajouter_nouveau_son(son_kwargs=Session().son_to_dl, schema="ProjetInfo"):
            print("Ajout du son avec succès. Retour au menu de votre scène.")
        else:
            print("L'ajout du son n'a pas pu aboutir.")
        from view.menuparamscenespecifiqueview import MenuParamSceneSpecifiqueView

        return MenuParamSceneSpecifiqueView()

    def display_info(self):
        print(Fore.BLUE + " MENU DE PARAMETRAGE ".center(80, "=") + Style.RESET_ALL)
