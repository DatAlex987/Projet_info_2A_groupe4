from src.dao.db_connection import DBConnection
from src.business_object.user import User
from src.business_object.personne import Personne
from datetime import date


# test de DBConnection
def test_db_connection():
    try:
        with DBConnection() as conn:
            print("Connection is open.")
            # Optionally test a simple query here
    except Exception as e:
        print(f"Error: {e}")

<<<<<<< HEAD

test_db_connection()

python -m pytest src/tests/
=======
print(S)
print(S.modifier_nom(12))
print(ord("A"))
>>>>>>> 7deb7d7681ffcb71e97a441c852f5eed7665dd0e
