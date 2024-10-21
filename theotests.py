from src.dao.db_connection import DBConnection


def test_db_connection():
    try:
        with DBConnection() as conn:
            print("Connection is open.")
            # Optionally test a simple query here
    except Exception as e:
        print(f"Error: {e}")


test_db_connection()
