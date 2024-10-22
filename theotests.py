from src.dao.db_connection import DBConnection
from src.business_object.user import User
from src.business_object.personne import Personne
from src.business_object.scene import Scene
from datetime import date


# test de DBConnection
def test_db_connection():
    try:
        with DBConnection() as conn:
            print("Connection is open.")
            # Optionally test a simple query here
    except Exception as e:
        print(f"Error: {e}")


test_db_connection()

son_dao = SonDAO()
Sound = Son(
    "moteur",
    "bruit d'un moteur V8",
    datetime.time(0, 3, 52),
    "481395",
    ["voiture", "moteur", "puissance"],
)
print(son_dao.ajouter_son(Sound))


sd_dao = SDDAO()
sounddeck = SD(
    "",
    "",
    date.time(1, 3, 22),
    "12345",



)
