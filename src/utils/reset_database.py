from utils.singleton import Singleton
from dao.db_connection import DBConnection


class ResetDatabase(metaclass=Singleton):
    """
    Reinitialisation de la base de données
    """

    def ResetALL(self):
        print("[START] - Ré-initialisation de la base de données")

        init_db = open("data/init_db.sql", encoding="utf-8")
        init_db_as_string = init_db.read()

        try:
            with DBConnection(schema="ProjetInfo").connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(init_db_as_string)
        except Exception as e:
            print(e)
            raise

        print("[END] - Ré-initialisation de la base de données")

        print("[START] - Ré-initialisation de la base de données test")

        init_db_test = open("data/init_db_test.sql", encoding="utf-8")
        init_db_test_as_string = init_db_test.read()

        try:
            with DBConnection(schema="SchemaTest").connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(init_db_test_as_string)
        except Exception as e:
            print(e)
            raise

        print("[END] - Ré-initialisation de la base de données test")

        return True

        def ResetMAIN(self):
            print("[START] - Ré-initialisation de la base de données")

            init_db = open("data/init_db.sql", encoding="utf-8")
            init_db_as_string = init_db.read()

            try:
                with DBConnection(schema="ProjetInfo").connection as connection:
                    with connection.cursor() as cursor:
                        cursor.execute(init_db_as_string)
            except Exception as e:
                print(e)
                raise

            print("[END] - Ré-initialisation de la base de données")

        return True

    def ResetTEST(self):

        print("[START] - Ré-initialisation de la base de données test")

        init_db_test = open("data/init_db_test.sql", encoding="utf-8")
        init_db_test_as_string = init_db_test.read()

        try:
            with DBConnection(schema="SchemaTest").connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(init_db_test_as_string)
        except Exception as e:
            print(e)
            raise

        print("[END] - Ré-initialisation de la base de données test")

        return True
