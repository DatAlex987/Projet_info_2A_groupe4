# from tabulate import tabulate
# from utils.log_decorator import log
# from utils.securite import hash_password
import hashlib
import random
import string
import re
from business_object.user import User
from dao.user_dao import UserDAO
from view.session import Session
from business_object.sd import SD
from business_object.scene import Scene
from business_object.son import Son
from business_object.son_continu import Son_Continu
from business_object.son_aleatoire import Son_Aleatoire
from business_object.son_manuel import Son_Manuel
import datetime


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
        generation = "".join(random.choices(string.ascii_letters + string.digits, k=6))
        unique_id = f"{generation}"
        return unique_id

    def input_checking_injection(
        self, nom: str, prenom: str, pseudo: str, mdp: str, date_naissance: str = None
    ):
        # Check inputs pour injection:
        # Définition de pattern regex pour qualifier les caractères acceptés pour chaque input
        name_pattern = r"^[a-zA-ZÀ-ÿ' -]+$"  # Autorise lettres, accents, trait d'union, espace
        pseudo_pattern = r"^[\w\d]{1,29}$"  # Autorise lettres, chiffres, entre 1 et 29 caractères
        password_pattern = r"^[\w\d!@#$%^&*()+=]{1,29}$"  # Autorise lettres, chiffres et quelques caractères spéciaux (mais pas ', ",-, ; car utilisés dans des injections SQL.
        date_of_birth_pattern = r"^[\d/]{10,10}$"  # Autorise chiffres et / .
        # On vérifie que les inputs sont conformes aux patternes regex.
        if not re.match(name_pattern, nom):
            raise ValueError("Le nom contient des caractères invalides.")
        if not re.match(name_pattern, prenom):
            raise ValueError("Le prénom contient des caractères invalides.")
        if date_naissance is not None:
            if not re.match(date_of_birth_pattern, date_naissance):
                raise ValueError("La date de naissance contient des caractères invalides.")
        if not re.match(pseudo_pattern, pseudo):
            raise ValueError(
                "Le pseudo contient des caractères invalides ou n'est pas de longueur valide."
            )
        if not re.match(password_pattern, mdp):
            raise ValueError(
                "Le mot de passe contient des caractères invalides ou n'est pas de longueur valide."
            )

    def instancier_par_id_user(self, id_user: str, schema: str):
        dic_user = UserDAO().rechercher_par_id_user(id_user=id_user, schema=schema)
        SDs_of_user = []  # List to hold all sounddecks
        for sd in dic_user["SD_possedes"]:
            Scenes_of_user = []  # Create scenes list for each SD

            for scene in sd["scenes"]:
                Sons_Alea_scene = []  # Create these lists inside the scene loop
                Sons_Cont_scene = []
                Sons_Manu_scene = []
                # Process Sons_Alea_scene for each scene of the sounddeck
                for son_alea_kwargs in scene["sons_aleatoires"]:
                    Sons_Alea_scene.append(
                        Son_Aleatoire(
                            nom=son_alea_kwargs["nom"],
                            description=son_alea_kwargs["description"],
                            duree=son_alea_kwargs["duree"],
                            id_freesound=son_alea_kwargs["id_freesound"],
                            tags=son_alea_kwargs["tags"],
                            cooldown_min=son_alea_kwargs["param1"],
                            cooldown_max=son_alea_kwargs["param2"],
                        )
                    )
                # Process Sons_Cont_scene for each scene
                for son_cont_kwargs in scene["sons_continus"]:
                    Sons_Cont_scene.append(
                        Son_Continu(
                            nom=son_cont_kwargs["nom"],
                            description=son_cont_kwargs["description"],
                            duree=son_cont_kwargs["duree"],
                            id_freesound=son_cont_kwargs["id_freesound"],
                            tags=son_alea_kwargs["tags"],
                        )
                    )
                # Process Sons_Manu_scene for each scene
                for son_manu_kwargs in scene["sons_manuels"]:
                    Sons_Manu_scene.append(
                        Son_Manuel(
                            nom=son_manu_kwargs["nom"],
                            description=son_manu_kwargs["description"],
                            duree=son_manu_kwargs["duree"],
                            id_freesound=son_manu_kwargs["id_freesound"],
                            tags=son_alea_kwargs["tags"],
                            start_key=son_manu_kwargs["param1"],
                        )
                    )
                # Create scene objects for this sounddeck
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

            # Now add the sounddeck with its scenes to SDs_of_user
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
                # l.86 - l.152 : On instancie tous les objets liés à l'utilisateur avec les données
                # fournies par l'appel DAO rechercher_par_pseudo_user()
                """SDs_of_user = []  # List to hold all sounddecks

                for sd in dic_user["SD_possedes"]:
                    Scenes_of_user = []  # Create scenes list for each SD

                    for scene in sd["scenes"]:
                        Sons_Alea_scene = []  # Create these lists inside the scene loop
                        Sons_Cont_scene = []
                        Sons_Manu_scene = []
                        # Process Sons_Alea_scene for each scene of the sounddeck
                        for son_alea_kwargs in scene["sons_aleatoires"]:
                            Sons_Alea_scene.append(
                                Son_Aleatoire(
                                    nom=son_alea_kwargs["nom"],
                                    description=son_alea_kwargs["description"],
                                    duree=son_alea_kwargs["duree"],
                                    id_freesound=son_alea_kwargs["id_freesound"],
                                    tags=son_alea_kwargs["tags"],
                                    cooldown_min=son_alea_kwargs["param1"],
                                    cooldown_max=son_alea_kwargs["param2"],
                                )
                            )
                        # Process Sons_Cont_scene for each scene
                        for son_cont_kwargs in scene["sons_continus"]:
                            Sons_Cont_scene.append(
                                Son_Continu(
                                    nom=son_cont_kwargs["nom"],
                                    description=son_cont_kwargs["description"],
                                    duree=son_cont_kwargs["duree"],
                                    id_freesound=son_cont_kwargs["id_freesound"],
                                    tags=son_alea_kwargs["tags"],
                                )
                            )
                        # Process Sons_Manu_scene for each scene
                        for son_manu_kwargs in scene["sons_manuels"]:
                            Sons_Manu_scene.append(
                                Son_Manuel(
                                    nom=son_manu_kwargs["nom"],
                                    description=son_manu_kwargs["description"],
                                    duree=son_manu_kwargs["duree"],
                                    id_freesound=son_manu_kwargs["id_freesound"],
                                    tags=son_alea_kwargs["tags"],
                                    start_key=son_manu_kwargs["param1"],
                                )
                            )
                        # Create scene objects for this sounddeck
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

                    # Now add the sounddeck with its scenes to SDs_of_user
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
                )"""
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

    def FindCloseNameUser(self, pseudo_approx: str, schema: str):
        all_users = UserDAO().consulter_users()
        users_close_name = []
        for user in all_users:
            if pseudo_approx.lower() in user["pseudo"].lower():
                users_close_name.append(
                    self.instancier_par_id_user(id_user=user.id_user, schema=schema)
                )
        pass


"""    @log
    def creer(self, nom, prenom, date_naissance, id_user, mdp, SD_possedes):

        new_user = User(nom, prenom, date_naissance, id_user, mdp, SD_possedes)
        return new_user if UserDAO().ajouter_user(new_user) else None

    @log
    def supprimer(self, utilisateur) -> bool:

        return UserDAO().supprimer(utilisateur)

    @log
    def lister_tous_les_utilisateurs(self, inclure_mdp=False) -> list[User]:
        "Lister tous les joueurs
        Si inclure_mdp=True, les mots de passe seront inclus
        Par défaut, tous les mdp des joueurs sont à None
        "
        utilisateurs = UserDAO().consulter_users()
        if not inclure_mdp:
            for u in utilisateurs:
                u.mdp = None
        return utilisateurs

    @log
    def afficher_tous(self) -> str:

        entetes = ["pseudo", "..."]

        utilisateurs = UserDAO().consulter_users()

        for u in utilisateurs:  # mesure de sécurité dans le cas d'une l'implémentation
            if u.pseudo == "admin":  # futur objet Admin
                utilisateurs.remove(u)

        utilisateurs_as_list = [u.as_list() for u in utilisateurs]

        str_users = "-" * 100
        str_users += "\nListe des joueurs \n"
        str_users += "-" * 100
        str_users += "\n"
        str_users += tabulate(
            tabular_data=utilisateurs_as_list,
            headers=entetes,
            tablefmt="psql",
            floatfmt=".2f",
        )
        str_users += "\n"

        return str_users

    @log
    def trouver_par_id(self, id_user) -> User:

        return UserDAO().rechercher_par_id_users(id_user)

    @log
    def pseudo_deja_utilise(self, pseudo) -> bool:
        "Vérifie si le pseudo est déjà utilisé
        Retourne True si le pseudo existe déjà en BDD"
        utilisateurs = UserDAO().consulter_users()
        return pseudo in [u.pseudo for u in utilisateurs]"""
