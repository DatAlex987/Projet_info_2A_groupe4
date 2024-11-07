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
import datetime


class UserService:
    """Classe contenant les méthodes de service des Utilisateurs"""

    def __init__(self):
        self.user_dao = UserDAO()
        self.session = None

    def compare_mdp(self, mdp: str, sel: str, mdp_hashe: str):
        """Compare un mot de passe et son sel avec sa version hashé"""
        print(mdp_hashe)
        gen_hash = hashlib.pbkdf2_hmac("sha256", mdp.encode("utf-8"), sel.encode("utf-8"), 100000)
        print(gen_hash.hex())
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

    def authenticate_user(self, nom: str, prenom: str, pseudo: str, mdp: str, schema: str):
        """Methode d'authentification : vérifie que les informations fournies
        corrrespondent et instancie la session avec l'objet User qui convient"""
        dic_user = self.user_dao.rechercher_par_pseudo_user(pseudo_user=pseudo, schema=schema)
        if dic_user:
            # Si le pseudo et le mdp correspondent :
            if dic_user["pseudo"] == pseudo and UserService.compare_mdp(
                self, mdp=mdp, sel=nom, mdp_hashe=dic_user["mdp_hashe"]
            ):
                self.session = Session()  # On lance la session avec le bon user
                utilisateur = User(
                    nom=dic_user["nom"],
                    prenom=dic_user["prenom"],
                    date_naissance=dic_user["date_naissance"],
                    id_user=dic_user["id_user"],
                    SD_possedes=dic_user["SD_possedes"],
                    pseudo=dic_user["pseudo"],
                )
                self.session.connexion(utilisateur)
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
        # Check inputs pour injection:
        # Définition de pattern regex pour qualifier les caractères acceptés pour chaque input
        name_pattern = r"^[a-zA-ZÀ-ÿ' -]+$"  # Autorise lettres, accents, trait d'union, espace
        pseudo_pattern = r"^[\w\d]{1,29}$"  # Autorise lettres, chiffres, entre 1 et 29 caractères
        password_pattern = r"^[\w\d!@#$%^&*()+=]{1,29}$"  # Autorise lettres, chiffres et quelques caractères spéciaux (mais pas ', ",-, ; car utilisés dans des injections SQL.

        # On vérifie que les inputs sont conformes aux patternes regex.
        if not re.match(name_pattern, nom):
            raise ValueError("Le nom contient des caractères invalides.")
        if not re.match(name_pattern, prenom):
            raise ValueError("Le prénom contient des caractères invalides.")
        if not re.match(pseudo_pattern, pseudo):
            raise ValueError(
                "Le pseudo contient des caractères invalides ou n'est pas de longueur valide."
            )
        if not re.match(password_pattern, mdp):
            raise ValueError(
                "Le mot de passe contient des caractères invalides ou n'est pas de longueur valide."
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
        except ValueError:
            raise ValueError("Erreur lors de la création du compte.")


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
