from utils.singleton import Singleton
from dao.db_connection import DBConnection
from business_object.user import User
from datetime import date


class UserDAO(metaclass=Singleton):
    """Implémente les méthodes du CRUD pour accéder à la base de données des utilisateurs."""

    def ajouter_user(self, user: User) -> int:
        """
        Ajoute un utilisateur dans la base de données.

        Parameters
        ----------
        user : User
            Instance de la classe User contenant les informations de l'utilisateur.

        Returns
        -------
        int
            L'ID de l'utilisateur ajouté.
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO ProjetInfo.User(id_user, mdp_hash, date_naissance, nom, prenom) VALUES"
                    "(%(id_user)s, %(mdp_hash)s, %(date_naissance)s, %(nom)s, %(prenom)s) RETURNING id_user;",
                    {
                        "id_user": user.id_user,
                        "mdp_hash": user.mot_de_passe_hash,
                        "date_naissance": user.date_naissance,
                        "nom": user.nom,
                        "prenom": user.prenom,
                    },
                )
                res = cursor.fetchone()
        return res["id_user"] if res else None

    def supprimer_user(self, id_user: int) -> bool:
        """
        Supprime un utilisateur par son ID.

        Parameters
        ----------
        id_user : int
            L'ID de l'utilisateur à supprimer.

        Returns
        -------
        bool
            True si la suppression a réussi, sinon False.
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM ProjetInfo.User WHERE id_user = %(id_user)s;",
                    {"id_user": id_user},
                )
                return cursor.rowcount > 0

    def consulter_users(self) -> list:
        """
        Récupère la liste de tous les utilisateurs dans la base de données.

        Returns
        -------
        list
            Une liste de dictionnaires contenant les informations des utilisateurs.
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM ProjetInfo.User;")
                users = cursor.fetchall()
                return users if users else []

    def rechercher_par_id_user(self, id_user: int) -> dict:
        """
        Recherche un utilisateur dans la base de données par son ID.

        Parameters
        ----------
        id_user : int
            L'ID de l'utilisateur à rechercher.

        Returns
        -------
        dict
            Un dictionnaire contenant les informations de l'utilisateur, ou None si aucun utilisateur trouvé.
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM ProjetInfo.User WHERE id_user = %(id_user)s;",
                    {"id_user": id_user},
                )
                user = cursor.fetchone()
                return user if user else None

    def ajouter_sounddeck(self, id_user: int, nom: str) -> None:
        """
        Ajoute un sounddeck pour un utilisateur.

        Parameters
        ----------
        id_user : int
            L'ID de l'utilisateur à qui associer le sounddeck.
        nom : str
            Le nom du sounddeck à ajouter.
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO ProjetInfo.Sounddeck(nom, id_user) VALUES (%(nom)s, %(id_user)s);",
                    {"nom": nom, "id_user": id_user},
                )
        print(f"Le sounddeck '{nom}' a été ajouté pour l'utilisateur {id_user}.")

    def consulter_sounddecks_par_user(self, user: User) -> list:
        """
        Récupère tous les sounddecks d'un utilisateur.

        Parameters
        ----------
        user : User
            Instance de la classe User pour laquelle récupérer les sounddecks.

        Returns
        -------
        list
            La liste des sounddecks associés à cet utilisateur.
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT nom FROM ProjetInfo.Sounddeck WHERE id_user = %(id_user)s;",
                    {"id_user": user.id_user},
                )
                sounddecks = cursor.fetchall()
                return [sounddeck["nom"] for sounddeck in sounddecks] if sounddecks else []

    def supprimer_sounddeck(self, id_user: int, nom: str) -> bool:
        """
        Supprime un sounddeck d'un utilisateur.

        Parameters
        ----------
        id_user : int
            L'ID de l'utilisateur auquel appartient le sounddeck.
        nom : str
            Le nom du sounddeck à supprimer.

        Returns
        -------
        bool
            True si le sounddeck a été supprimé avec succès, sinon False.
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM ProjetInfo.Sounddeck WHERE id_user = %(id_user)s AND nom = %(nom)s;",
                    {"id_user": id_user, "nom": nom},
                )
                return cursor.rowcount > 0
