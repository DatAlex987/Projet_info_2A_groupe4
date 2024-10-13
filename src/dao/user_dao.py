from utils.singleton import Singleton
from dao.db_connection import DBConnection

# from business_object.user import User


class UserDAO(metaclass=Singleton):
    """Implémente les méthodes du CRUD pour accéder à la base de données des users"""

    def ajouter_user(pseudo, mdp_hashe, age, nom, prenom) -> None:
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Utilisateur(pseudo, mdp_hashe, age, nom, prenom) VALUES        "
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

    def supprimer_user():
        pass

    def consulter_users():
        pass

    def rechercher_par_id_users():
        pass
