import hashlib
import random
import string
import datetime
import re

####
from dao.user_dao import UserDAO
from business_object.user import User
from business_object.sd import SD
from business_object.scene import Scene
from business_object.son_continu import Son_Continu
from business_object.son_aleatoire import Son_Aleatoire
from business_object.son_manuel import Son_Manuel

####
from service.session import Session


class UserService:
    """Classe contenant les méthodes de service des Utilisateurs"""

    def __init__(self):
        self.user_dao = UserDAO()
        self.session = None

    def compare_mdp(self, mdp: str, sel: str, mdp_hashe: str):
        """Compare un mot de passe et son sel avec sa version hashé"""
        gen_hash = hashlib.pbkdf2_hmac("sha256", mdp.encode("utf-8"), sel.encode("utf-8"), 100000)
        return gen_hash.hex() == mdp_hashe

    @staticmethod  # Ne nécessite pas d'instance de UserService pour exister
    def id_user_generator():
        """Génère un identifiant pour un utilisateur.

        Identifiant de la forme XYZRST où X,Y,Z,R,S,T sont des caractères alphanumériques

        Returns:
        -------------------------
        str
        Identifiant (supposé unique) généré pour un utilisateur.
        """
        all_users = UserDAO().consulter_users(schema="ProjetInfo")
        all_ids = [user["id_user"] for user in all_users]
        generation = "".join(random.choices(string.ascii_letters + string.digits, k=6))
        unique_id = f"{generation}"
        while unique_id in all_ids:  # On vérifie que l'id n'existe pas déjà
            generation = "".join(random.choices(string.ascii_letters + string.digits, k=6))
            unique_id = f"{generation}"
        return unique_id

    def input_checking_injection(
        self, nom: str, prenom: str, pseudo: str, mdp: str, date_naissance: str = None
    ):
        # Patterns pour éviter les injections SQL
        patterns = [
            r"(--|#)",  # Commentaires
            r"(\bUNION\b)",  # UNION
            r"(;|\bDROP\b|\bDELETE\b|\bINSERT\b|\bUPDATE\b|\bSELECT\b)",  # CRUD
            r"(\')",  # guillemet simple
            r"(\bEXEC\b|\bEXECUTE\b)",  # EXECUTE
        ]

        # Autres patterns, plus spécifiques
        name_pattern = r"^[a-zA-ZÀ-ÿ' -]{1,29}$"
        pseudo_pattern = r"^[\w\d]{1,29}$"
        password_pattern = r"^[\w\d!@#$%^&*()]{1,29}$"
        date_of_birth_pattern = r"^[\d/]{10,10}$"

        # On vérifie
        if not re.match(name_pattern, nom):
            raise ValueError("Le nom contient des caractères invalides.")
        if not re.match(name_pattern, prenom):
            raise ValueError("Le prénom contient des caractères invalides.")
        if date_naissance and not re.match(date_of_birth_pattern, date_naissance):
            raise ValueError("La date de naissance contient des caractères invalides.")
        if not re.match(pseudo_pattern, pseudo):
            raise ValueError(
                "Le pseudo contient des caractères invalides ou n'est pas de longueur valide."
            )
        if not re.match(password_pattern, mdp):
            raise ValueError(
                "Le mot de passe contient des caractères invalides ou n'est pas de longueur valide."
            )

        # On vérifie pour les injections SQL
        inputs = [nom, prenom, pseudo, mdp]
        if date_naissance:
            inputs.append(date_naissance)
        for input_str in inputs:
            for pattern in patterns:
                if re.search(pattern, input_str, re.IGNORECASE):
                    raise ValueError(
                        f"La chaîne de caracères {input_str} est invalide car suspecte."
                    )

    def instancier_par_id_user(self, id_user: str, schema: str):
        dic_user = UserDAO().rechercher_par_id_user(id_user=id_user, schema=schema)
        SDs_of_user = []  # Liste de toutes les SDs
        for sd in dic_user["SD_possedes"]:
            Scenes_of_user = []

            for scene in sd["scenes"]:
                Sons_Alea_scene = []
                Sons_Cont_scene = []
                Sons_Manu_scene = []
                for son_alea_kwargs in scene["sons_aleatoires"]:
                    Sons_Alea_scene.append(
                        Son_Aleatoire(
                            nom=son_alea_kwargs["nom"],
                            description=son_alea_kwargs["description"],
                            duree=son_alea_kwargs["duree"],
                            id_freesound=son_alea_kwargs["id_freesound"],
                            id_son=son_alea_kwargs["id_son"],
                            tags=son_alea_kwargs["tags"],
                            cooldown_min=son_alea_kwargs["param1"],
                            cooldown_max=son_alea_kwargs["param2"],
                        )
                    )
                for son_cont_kwargs in scene["sons_continus"]:
                    Sons_Cont_scene.append(
                        Son_Continu(
                            nom=son_cont_kwargs["nom"],
                            description=son_cont_kwargs["description"],
                            duree=son_cont_kwargs["duree"],
                            id_freesound=son_cont_kwargs["id_freesound"],
                            id_son=son_cont_kwargs["id_son"],
                            tags=son_cont_kwargs["tags"],
                        )
                    )
                for son_manu_kwargs in scene["sons_manuels"]:
                    Sons_Manu_scene.append(
                        Son_Manuel(
                            nom=son_manu_kwargs["nom"],
                            description=son_manu_kwargs["description"],
                            duree=son_manu_kwargs["duree"],
                            id_freesound=son_manu_kwargs["id_freesound"],
                            id_son=son_manu_kwargs["id_son"],
                            tags=son_manu_kwargs["tags"],
                            start_key=son_manu_kwargs["param1"],
                        )
                    )
                Scenes_of_user.append(
                    Scene(
                        nom=scene["nom"],
                        description=scene["description"],
                        id_scene=scene["id_scene"],
                        sons_aleatoires=Sons_Alea_scene,
                        sons_manuels=Sons_Manu_scene,
                        sons_continus=Sons_Cont_scene,
                        date_creation=scene["date_creation"],
                    )
                )

            SDs_of_user.append(
                SD(
                    nom=sd["nom"],
                    description=sd["description"],
                    id_sd=sd["id_sd"],
                    scenes=Scenes_of_user,
                    date_creation=sd["date_creation"],
                    id_createur=sd["id_createur"],
                )
            )

        utilisateur = User(
            nom=dic_user["nom"],
            prenom=dic_user["prenom"],
            date_naissance=dic_user["date_naissance"],
            id_user=dic_user["id_user"],
            SD_possedes=SDs_of_user,
            pseudo=dic_user["pseudo"],
        )
        return utilisateur

    def authenticate_user(self, nom: str, prenom: str, pseudo: str, mdp: str, schema: str):
        """Methode d'authentification : vérifie que les informations fournies
        corrrespondent et instancie la session avec l'objet User qui convient"""
        UserService().input_checking_injection(nom=nom, prenom=prenom, pseudo=pseudo, mdp=mdp)
        dic_user = self.user_dao.rechercher_par_pseudo_user(pseudo_user=pseudo, schema=schema)
        if dic_user:
            # Si le pseudo et le mdp correspondent :
            if dic_user["pseudo"] == pseudo and UserService.compare_mdp(
                self, mdp=mdp, sel=nom, mdp_hashe=dic_user["mdp_hashe"]
            ):
                self.session = Session()  # On lance la session avec le bon user
                self.session.connexion(
                    self.instancier_par_id_user(id_user=dic_user["id_user"], schema=schema)
                )
                return True
            else:
                raise ValueError("Les informations renseignées sont incorrectes.")
        else:
            raise ValueError("Utilisateur inconnu.")

    def creer_compte(
        self,
        nom: str,
        prenom: str,
        date_naissance: datetime.date,
        pseudo: str,
        mdp: str,
        schema: str,
    ):
        UserService().input_checking_injection(
            nom=nom, prenom=prenom, date_naissance=date_naissance, pseudo=pseudo, mdp=mdp
        )
        try:
            new_user = User(
                nom=nom,
                prenom=prenom,
                date_naissance=datetime.datetime.strptime(date_naissance, "%d/%m/%Y").date(),
                id_user=UserService.id_user_generator(),
                mdp=mdp,
                pseudo=pseudo,
            )
            self.user_dao.ajouter_user(new_user, schema="ProjetInfo")
            UserService().authenticate_user(
                nom=nom, prenom=prenom, pseudo=pseudo, mdp=mdp, schema="ProjetInfo"
            )
        except ValueError as e:
            raise ValueError(f"{e}")

    def FindCloseNameUsers(self, pseudo_approx: str, schema: str):
        all_users = UserDAO().consulter_users(schema=schema)
        users_close_name = []
        for user in all_users:
            if pseudo_approx.lower() in user["pseudo"].lower():
                users_close_name.append(
                    self.instancier_par_id_user(id_user=user["id_user"], schema=schema)
                )
        Session().users_to_consult = users_close_name

    def formatage_question_users_to_consult(self):
        """Construit une liste des choix à afficher dans le menu consult user

        Returns
        -------------
        list
            Liste des choix proposés à l'utilisateur, incluant tous les users
            susceptibles de l'intéresser
        """
        users = Session().users_to_consult
        choix = []
        compteur = 1
        for user in users:
            mise_en_page_ligne = (
                f"{compteur}. {user.id_user} | {user.prenom} | {user.prenom} | {user.pseudo}"
            )
            choix.append(mise_en_page_ligne)
            compteur += 1
        choix.append("Retour au menu de consultation")
        return choix
