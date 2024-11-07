from tabulate import tabulate

from utils.log_decorator import log
from utils.securite import hash_password

from business_object.user import User
from dao.user_dao import UserDAO
from view.session import Session


class UserService:
    """Classe contenant les méthodes de service des Utilisateurs"""

    def __init__(self):
        self.user_dao = UserDAO()
        self.session = Session.connexion()

    def authenticate_user(self, nom, prenom, mdp):
        pass
        # vérifie que le user existe en BDD et instancie la session comme il faut


"""    @log
    def creer(self, nom, prenom, date_naissance, id_user, mdp, SD_possedes):

        new_user = User(nom, prenom, date_naissance, id_user, mdp, SD_possedes)
        return new_user if UserDAO().ajouter_user(new_user) else None

    @log
    def supprimer(self, utilisateur) -> bool:

        return UserDAO().supprimer(utilisateur)

    @log
    def se_connecter(self, pseudo, mdp) -> User:

        return UserDAO().se_connecter(pseudo, hash_password(mdp, pseudo))

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
