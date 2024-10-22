from utils.singleton import Singleton
from dao.db_connection import DBConnection

# from business_object.user import User


class UserDAO(metaclass=Singleton):
    """Implémente les méthodes du CRUD pour accéder à la base de données des users"""

    def ajouter_user(pseudo, mdp_hashe, age, nom, prenom) -> None:
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO ProjetInfo.Utilisateur(pseudo, mdp_hashe, age, nom, prenom) VALUES"
                    "(%(pseudo)s, %(mdp_hashe)s, %(age)s, %(nom)s, %(prenom)s)             "
                    "  RETURNING id_user;                                                ",
                    {
                        "pseudo": pseudo,
                        "mdp_hashe": mdp_hashe,
                        "age": age,
                        "nom": nom,
                        "prenom": prenom,
                    },
                )
                res = cursor.fetchone()

        return res

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
                    "DELETE FROM ProjetInfo.Utilisateur WHERE id_user = %(id_user)s;",
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
                cursor.execute("SELECT * FROM ProjetInfo.Utilisateur;")
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
            Un dictionnaire contenant les informations de l'utilisateur,
            ou None si aucun utilisateur trouvé.
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM ProjetInfo.Utilisateur WHERE id_user = %(id_user)s;",
                    {"id_user": id_user},
                )
                user = cursor.fetchone()
                return user if user else None

    def ajouter_sounddeck(self, id_user: int, nom: str) -> bool:
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
        return True

    def consulter_sounddecks_par_user(self, id_user: int) -> list:
        """
        Récupère tous les sounddecks d'un utilisateur.

        Parameters
        ----------
        id_user : int
            L'ID de l'utilisateur pour lequel récupérer les sounddecks.

        Returns
        -------
        list
            La liste des sounddecks associés à cet utilisateur.
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT nom FROM ProjetInfo.Sounddeck WHERE id_user = %(id_user)s;",
                    {"id_user": id_user},
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
        nom_sounddeck : str
            Le nom du sounddeck à supprimer.

        Returns
        -------
        bool
            True si le sounddeck a été supprimé avec succès, sinon False.
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM ProjetInfo.Sounddeck"
                    + " WHERE id_user = %(id_user)s AND nom = %(nom)s;",
                    {"id_user": id_user, "nom": nom},
                )
                return cursor.rowcount > 0
