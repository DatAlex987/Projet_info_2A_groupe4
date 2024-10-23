from utils.singleton import Singleton
from dao.db_connection import DBConnection


class ResetDatabase(metaclass=Singleton):
    """
    Reinitialisation de la base de données
    """

    def lancer(self):
        print("Ré-initialisation de la base de données")

        init_db = open("data/init_db.sql", encoding="utf-8")
        init_db_as_string = init_db.read()

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(init_db_as_string)
        except Exception as e:
            print(e)
            raise

        print("Ré-initialisation de la base de données - Terminée")

        print("Ré-initialisation de la base de données test")

        init_db_test = open("data/init_db_test.sql", encoding="utf-8")
        init_db_test_as_string = init_db_test.read()

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(init_db_test_as_string)
        except Exception as e:
            print(e)
            raise

        print("Ré-initialisation de la base de données test - Terminée")

        return True


if __name__ == "__main__":
    ResetDatabase().lancer()
