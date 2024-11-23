from utils.singleton import Singleton
from dao.db_connection import DBConnection
from business_object.user import User
from dao.sd_dao import SDDAO


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
                INSERT INTO {schema}.utilisateur(id_user, mdp_hashe, date_naissance, nom, prenom,
                pseudo)
                VALUES (%(id_user)s, %(mdp_hashe)s, %(date_naissance)s, %(nom)s, %(prenom)s,
                %(pseudo)s) RETURNING id_user;
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
                        "pseudo": user.pseudo,
                    },
                )
        return user

    def supprimer_user(self, id_user: str, schema: str) -> bool:
        """
        Supprime un utilisateur par son ID et toutes les associations liées (car ON DELETE CASCADE dans
        le script de création de la BDD)

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
                query = f"DELETE FROM {schema}.Utilisateur WHERE id_user = %(id_user)s;"
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
                        "pseudo": user["pseudo"],
                        "SD_possedes": SDDAO().rechercher_sds_par_user(
                            str(user["id_user"]), schema=schema
                        ),
                    }
                )
                # Le mot de passe est ignoré pour évité d'être hashé de nouveau.
            return users_trouves
        return None

    def rechercher_par_id_user(self, id_user: str, schema: str) -> dict:
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
            Une instance de la classe User contenant les informations de l'utilisateur,
            ou None si aucun utilisateur trouvé.
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
                "pseudo": user_data["pseudo"],
                "SD_possedes": SDDAO().rechercher_sds_par_user(
                    str(user_data["id_user"]), schema=schema
                ),
            }
            return user_trouve
        return None

    def rechercher_par_pseudo_user(self, pseudo_user: str, schema: str) -> dict:
        """
        Recherche un utilisateur dans la base de données par son pseudo.

        Parameters
        ----------
        pseudo_user : str
            Le pseudo de l'utilisateur à rechercher.
        schema : str
            Le schéma de la base de données à requêter.

        Returns
        -------
        dict
            Un dictionnaire contenant les informations de l'utilisateur,
            ou None si aucun utilisateur trouvé.
        """
        with DBConnection(schema=schema).connection as connection:
            with connection.cursor() as cursor:
                query = f"""SELECT * FROM {schema}.Utilisateur
                WHERE pseudo = %(pseudo_user)s;"""
                cursor.execute(
                    query,
                    {"pseudo_user": pseudo_user},
                )
                user_data = cursor.fetchone()
        if user_data:
            user_trouve = {
                "nom": user_data["nom"],
                "prenom": user_data["prenom"],
                "pseudo": user_data["pseudo"],
                "date_naissance": user_data["date_naissance"],
                "mdp_hashe": user_data["mdp_hashe"],
                "id_user": str(user_data["id_user"]),
                "SD_possedes": SDDAO().rechercher_sds_par_user(
                    str(user_data["id_user"]), schema=schema
                ),
            }
            return user_trouve
        return None

    def get_sds_of_user(self, id_user: str, schema: str):
        """
        Renvoie la liste des id des SDs qui sont dans le répertoire de id_user/
        """
        with DBConnection(schema=schema).connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"SELECT id_sd FROM {schema}.User_Sounddeck WHERE id_user = %(id_user)s;",
                    {"id_user": id_user},
                )
                res = cursor.fetchall()
        return [row["id_sd"] for row in res]
