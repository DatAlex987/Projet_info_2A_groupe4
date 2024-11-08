import re
import datetime
import random
import string
from view.session import Session
from business_object.sd import SD
from dao.sd_dao import SDDAO


class SDService:
    """Classe contenant les méthodes de service des Sound-decks"""

    def input_checking_injection(self, nom: str, description: str):
        # Check inputs pour injection:
        # Définition de pattern regex pour qualifier les caractères acceptés pour chaque input
        pattern = r"^[a-zA-Zà-öø-ÿÀ-ÖØ-ß\s0-9\s,.\-:!@#%^&*()_+=|?/\[\]{}']*$"  # Autorise lettres, et autres caractères
        # On vérifie que les inputs sont conformes aux patternes regex.
        if not re.match(pattern, nom):
            raise ValueError("Le nom de la SD contient des caractères invalides.")
        if not re.match(pattern, description):
            raise ValueError("La description de la SD contient des caractères invalides.")

    @staticmethod  # Ne nécessite pas d'instance de SDService pour exister
    def id_sd_generator():
        """Génère un identifiant pour une SD.

        Identifiant de la forme XYZRSTU où X,Y,Z,R,S,T,U sont des caractères alphanumériques

        Returns:
        -------------------------
        str
            Identifiant (supposé unique) généré pour une SD.
        """
        generation = "".join(random.choices(string.ascii_letters + string.digits, k=7))
        unique_id = f"{generation}"
        return unique_id

    def creer_sd(self, nom: str, description: str, schema: str):
        """Instancie une SD avec les inputs de l'utilisateur et l'ajoute dans la BDD

        Param
        ------------
        nom : str
            nom donné à la SD par l'utilisateur
        description : str
            description donnée à la SD par l'utilisateur
        schema : str
            schema sur lequel opérer l'ajout de la SD

        Returns
        ------------
        ???
        """
        SDService().input_checking_injection(nom=nom, description=description)
        try:
            new_sd = SD(
                nom=nom,
                description=description,
                id_sd=SDService.id_sd_generator(),
                scenes=[],
                date_creation=datetime.datetime.today().date(),
            )
            SDDAO().ajouter_sd(sd=new_sd, schema=schema)
            SDDAO().ajouter_association_user_sd(
                id_user=Session().utilisateur.id_user, id_sd=new_sd.id_sd, schema=schema
            )
            Session().utilisateur.SD_possedes.append(new_sd)
            return True
        except ValueError as e:
            raise ValueError(f"{e}")

    def formatage_question_sds_of_user(self):
        sds_user = Session().utilisateur.SD_possedes
        print(sds_user)
        choix = []
        compteur = 1
        for sd in sds_user:
            print(sd.nom)
            print(sd.description[: min(len(sd.description), 40)])
            print(sd.date_creation)
            mise_en_page_ligne = f"{compteur}. {sd.id_sd} | {sd.nom} | {sd.description[:min(len(sd.description), 40)]}... | {sd.date_creation}"
            choix.append(mise_en_page_ligne)
            compteur += 1
        choix.append("Retour au menu de paramétrage")
        return choix
