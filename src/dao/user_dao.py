from utils.singleton import Singleton
from dao.db_connection import DBConnection

# from business_object.user import User


class UserDAO(metaclass=Singleton):
    """Implémente les méthodes du CRUD pour accéder à la base de données des users"""

    def ajouter_user(pseudo, mdp, age, mail) -> None:
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO User(pseudo, mdp, age, mail) VALUES        "
                    "(%(pseudo)s, %(mdp)s, %(age)s, %(mail)s)             "
                    "  RETURNING id_user;                                                ",
                    {
                        "pseudo": pseudo,
                        "mdp": mdp,
                        "age": age,
                        "mail": mail,
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
