import datetime
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
            Le schéma de la base de données. Par défaut, c'est 'projetinfo'.

        Returns
        -------
        int
            L'ID de l'utilisateur ajouté.
        """
        if user.mot_de_passe_hash is None:  # Permet de s'assurer qu'un mdp est rentré la 1ère fois.
            raise TypeError("Vous devez renseigner un mot de passe pour créer votre compte.")

        with DBConnection(schema=schema).connection as connection:
            with connection.cursor() as cursor:
                query = f"""
                INSERT INTO {schema}.utilisateur(id_user, mdp_hashe, date_naissance, nom, prenom)
                VALUES (%(id_user)s, %(mdp_hashe)s, %(date_naissance)s, %(nom)s, %(prenom)s)
                RETURNING id_user;
                """
                cursor.execute(
                    query,
                    {
                        "schema": schema,
                        "id_user": user.id_user,
                        "mdp_hashe": user.mot_de_passe_hash,
                        "date_naissance": user.date_naissance,
                        "nom": user.nom,
                        "prenom": user.prenom,
                    },
                )
                # .strftime("%Y-%m-%d")
                # res = cursor.fetchone()
        return user

    def supprimer_user(self, id_user: int, schema: str) -> bool:
        """
        Supprime un utilisateur par son ID.

        Parameters
        ----------
        id_user : int
            L'ID de l'utilisateur à supprimer.
        schema : str
            Le schéma de la base de données. Par défaut, c'est 'projetinfo'.

        Returns
        -------
        bool
            True si la suppression a réussi, sinon False.
        """
        with DBConnection(schema=schema).connection as connection:
            with connection.cursor() as cursor:
                query = f"""DELETE FROM {schema}.Utilisateur WHERE id_user = %(id_user)s;"""
                cursor.execute(
                    query,
                    {"id_user": id_user},
                )
                return cursor.rowcount > 0  # Indique le nombre de lignes supprimées

    def consulter_users(self, schema: str) -> list:
        """
        Récupère la liste de tous les utilisateurs dans la base de données.

        Parameters
        ----------
        schema : str
            Le schéma de la base de données. Par défaut, c'est 'projetinfo'.

        Returns
        -------
        list
            Une liste de dictionnaires contenant les informations des utilisateurs.
        """
        with DBConnection(schema=schema).connection as connection:
            with connection.cursor() as cursor:

                cursor.execute(f"SELECT * FROM {schema}.Utilisateur;")

                users = cursor.fetchall()

                if users:
                    users_trouves = []
                    for user in users:
                        users_trouves.append(
                            {
                                "nom": user["nom"],
                                "prenom": user["prenom"],
                                "date_naissance": user["date_naissance"],
                                "id_user": str(user["id_user"]),
                                "SD_possedes": [],  # A AJOUTER ENSUITE
                            }
                        )
                        # Le mot de passe est ignoré pour évité d'être hashé de nouveau.
                    return users_trouves
                return None

    def rechercher_par_id_user(self, id_user: int, schema) -> dict:
        """
        Recherche un utilisateur dans la base de données par son ID.

        Parameters
        ----------
        id_user : int
            L'ID de l'utilisateur à rechercher.
        schema : str
            Le schéma de la base de données. Par défaut, c'est 'projetinfo'.

        Returns
        -------
        User
            Une instance de la classe User contenant les informations de l'utilisateur, ou None si aucun utilisateur trouvé.
        dict
            Un dictionnaire contenant les informations de l'utilisateur,
            ou None si aucun utilisateur trouvé.
        """
        with DBConnection(schema=schema).connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"SELECT * FROM {schema}.Utilisateur WHERE id_user = %(id_user)s;",
                    {"id_user": id_user},
                )
                user_data = cursor.fetchone()
                if user_data:
                    user_trouve = {
                        "nom": user_data["nom"],
                        "prenom": user_data["prenom"],
                        "date_naissance": user_data["date_naissance"],
                        "id_user": str(user_data["id_user"]),
                        "SD_possedes": [],  # A AJOUTER ENSUITE
                    }
                    return user_trouve
                return None


# Pas de modifier user car rien à modifier

# ###"def ajouter_sounddeck(self, user: User, nom: str, schema) -> None:
#     """
#     Ajoute un sounddeck pour un utilisateur.

#     Parameters
#     ----------
#     user : User
#         Instance de la classe User à qui associer le sounddeck.
#     nom : str
#         Le nom du sounddeck à ajouter.
#     """
#     if nom not in user.SD_possedes:
#         user.SD_possedes.append(nom)
#         print(f"Le sounddeck '{nom}' a été ajouté pour l'utilisateur {user.id_user}.")
#     else:
#         print(f"Le sounddeck '{nom}' existe déjà pour l'utilisateur {user.id_user}.")

# def consulter_sounddecks_par_user(self, user: User, schema) -> list:
#     """
#     Récupère tous les sounddecks d'un utilisateur.

#     Returns
#     -------
#     list
#         La liste des sounddecks associés à cet utilisateur.
#     """
#     return user.SD_possedes

# def supprimer_sounddeck(self, user: User, nom: str, schema) -> bool:
#     """
#     Supprime un sounddeck d'un utilisateur.

#     Parameters
#     ----------
#     user : User
#         Instance de la classe User à partir de laquelle supprimer le sounddeck.
#     nom : str
#         Le nom du sounddeck à supprimer.

#     Returns
#     -------
#     bool
#         True si le sounddeck a été supprimé avec succès, sinon False.
#     """
#     if nom in user.SD_possedes:
#         user.SD_possedes.remove(nom)
#         print(f"Le sounddeck '{nom}' a été supprimé pour l'utilisateur {user.id_user}.")
#         return True
#     else:
#         print(f"Le sounddeck '{nom}' n'existe pas pour l'utilisateur {user.id_user}.")
#         return False
