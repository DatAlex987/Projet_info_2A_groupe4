from utils.singleton import Singleton
from dao.db_connection import DBConnection
from business_object.user import User


class UserDAO(metaclass=Singleton):
    """Implémente les méthodes du CRUD pour accéder à la base de données des utilisateurs."""

    def ajouter_user(self, user: User, schema: str) -> int:
        """
        Ajoute un utilisateur dans la base de données.

        Parameters
        ----------
        user : User
            Instance de la classe User contenant les informations de l'utilisateur.
        schema : str
            Le schéma de la base de données.

        Returns
        -------
        int
            L'ID de l'utilisateur ajouté.
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:

                cursor.execute(
                    f"INSERT INTO {schema}.utilisateur(id_user, mdp_hashe, date_naissance, nom, prenom) VALUES"
                    "(%(id_user)s, %(mdp_hashe)s, %(date_naissance)s, %(nom)s, %(prenom)s) RETURNING id_user;",
                    {
                        "id_user": user.id_user,
                        "mdp_hashe": user.mot_de_passe_hash,
                        "date_naissance": user.date_naissance,
                        "nom": user.nom,
                        "prenom": user.prenom,
                    },
                )
                res = cursor.fetchone()
        return res["id_user"] if res else None

    def supprimer_user(self, id_user: int, schema: str) -> bool:
        """
        Supprime un utilisateur par son ID.

        Parameters
        ----------
        id_user : int
            L'ID de l'utilisateur à supprimer.
        schema : str
            Le schéma de la base de données.

        Returns
        -------
        bool
            True si la suppression a réussi, sinon False.
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"DELETE FROM {schema}.Utilisateur WHERE id_user = %(id_user)s;",
                    {"id_user": id_user},
                )
                return cursor.rowcount > 0

    def consulter_users(self, schema: str) -> list:
        """
        Récupère la liste de tous les utilisateurs dans la base de données.

        Parameters
        ----------
        schema : str
            Le schéma de la base de données.

        Returns
        -------
        list
            Une liste de dictionnaires contenant les informations des utilisateurs.
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {schema}.Utilisateur;")
                users = cursor.fetchall()
                return users if users else []

    def rechercher_par_id_user(self, id_user: int, schema: str) -> dict:
        """
        Recherche un utilisateur dans la base de données par son ID.

        Parameters
        ----------
        id_user : int
            L'ID de l'utilisateur à rechercher.
        schema : str
            Le schéma de la base de données.

        Returns
        -------
        dict
            Un dictionnaire contenant les informations de l'utilisateur, ou None si aucun utilisateur trouvé.
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"SELECT * FROM {schema}.Utilisateur WHERE id_user = %(id_user)s;",
                    {"id_user": id_user},
                )
                user = cursor.fetchone()
                return user if user else None

    def ajouter_sounddeck(self, id_user: int, nom: str, schema: str) -> None:
        """
        Ajoute un sounddeck pour un utilisateur.

        Parameters
        ----------
        id_user : int
            L'ID de l'utilisateur à qui associer le sounddeck.
        nom : str
            Le nom du sounddeck à ajouter.
        schema : str
            Le schéma de la base de données.
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"INSERT INTO {schema}.Sounddeck(nom, id_user) VALUES (%(nom)s, %(id_user)s);",
                    {"nom": nom, "id_user": id_user},
                )
        print(f"Le sounddeck '{nom}' a été ajouté pour l'utilisateur {id_user}.")

    def consulter_sounddecks_par_user(self, user: User, schema: str) -> list:
        """
        Récupère tous les sounddecks d'un utilisateur.

        Parameters
        ----------
        user : User
            Instance de la classe User pour laquelle récupérer les sounddecks.
        schema : str
            Le schéma de la base de données.

        Returns
        -------
        list
            La liste des sounddecks associés à cet utilisateur.
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"SELECT nom FROM {schema}.Sounddeck WHERE id_user = %(id_user)s;",
                    {"id_user": user.id_user},
                )
                sounddecks = cursor.fetchall()
                return [sounddeck["nom"] for sounddeck in sounddecks] if sounddecks else []

    def supprimer_sounddeck(self, id_user: int, nom: str, schema: str) -> bool:
        """
        Supprime un sounddeck d'un utilisateur.

        Parameters
        ----------
        id_user : int
            L'ID de l'utilisateur auquel appartient le sounddeck.
        nom : str
            Le nom du sounddeck à supprimer.
        schema : str
            Le schéma de la base de données.

        Returns
        -------
        bool
            True si le sounddeck a été supprimé avec succès, sinon False.
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"DELETE FROM {schema}.Sounddeck WHERE id_user = %(id_user)s AND nom = %(nom)s;",
                    {"id_user": id_user, "nom": nom},
                )
                return cursor.rowcount > 0
