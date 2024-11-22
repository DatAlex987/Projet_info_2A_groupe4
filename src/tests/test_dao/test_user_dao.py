import pytest
from dao.user_dao import UserDAO
from business_object.user import User
from dao.db_connection import DBConnection
from utils.reset_database import ResetDatabase


@pytest.fixture
def user_dao():
    return UserDAO()


@pytest.fixture
def schema_test():
    return "SchemaTest"


def test_ajouter_user_succes(user_dao, utilisateur2_kwargs, schema_test):
    ResetDatabase().ResetTEST()
    """Test si l'utilisateur est bien ajouté dans schema_test."""
    user_to_add = User(**utilisateur2_kwargs)

    try:
        # Ajouter l'utilisateur et récupérer l'ID de l'utilisateur ajouté
        added_user = user_dao.ajouter_user(user_to_add, schema_test)
        with DBConnection(schema=schema_test).connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"SELECT * FROM {schema_test}.utilisateur WHERE id_user = %(id_user)s",
                    {"id_user": added_user.id_user},
                )
                result = cursor.fetchone()
                assert (
                    result is not None
                ), "L'utilisateur ajouté n'a pas été trouvé dans la base de données."

                # On compare les IDs
                assert (
                    result["id_user"] == added_user.id_user
                ), "L'ID de l'utilisateur ne correspond pas."

    finally:
        # Clean up the test data
        reseter = ResetDatabase()
        reseter.ResetTEST()


def test_supprimer_user_succes(user_dao, utilisateur2_kwargs, schema_test):
    ResetDatabase().ResetTEST()
    """Test que l'utilisateur peut être correctement supprimé de la base de données."""
    user_to_add = User(**utilisateur2_kwargs)

    try:
        added_user = user_dao.ajouter_user(user_to_add, schema_test)

        assert (
            user_dao.supprimer_user(added_user.id_user, schema_test) is True
        ), "La suppression de l'utilisateur a échoué."

        with DBConnection(schema=schema_test).connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"SELECT * FROM {schema_test}.utilisateur WHERE id_user = %(id_user)s",
                    {"id_user": added_user.id_user},
                )
                result = cursor.fetchone()
                assert result is None, "L'utilisateur n'a pas été supprimé de la base de données."
    finally:
        user_dao.supprimer_user(utilisateur2_kwargs["id_user"], schema_test)
    # Clean up the test data
    reseter = ResetDatabase()
    reseter.ResetTEST()


def test_consulter_users_succes(user_dao, utilisateur2_kwargs, schema_test):
    ResetDatabase().ResetTEST()
    # GIVEN: A user already added in the test schema
    user_to_add = User(**utilisateur2_kwargs)
    user_dao.ajouter_user(user_to_add, schema_test)
    # WHEN: Querying the users in the database
    all_found_users = user_dao.consulter_users(schema_test)
    # THEN: The returned list of users should have the correct length
    assert len(all_found_users) == 1
    # Clean up the test data
    reseter = ResetDatabase()
    reseter.ResetTEST()


def test_rechercher_par_id_user_succes(user_dao, utilisateur2_kwargs, schema_test):
    ResetDatabase().ResetTEST()
    """Test que l'utilisateur peut être récupéré par son ID."""
    user_to_add = User(**utilisateur2_kwargs)

    try:
        # Ajouter l'utilisateur
        added_user = user_dao.ajouter_user(user_to_add, schema_test)

        # Rechercher l'utilisateur par ID
        user = user_dao.rechercher_par_id_user(added_user.id_user, schema_test)

        # Vérifier que l'utilisateur a été trouvé
        assert user is not None, "L'utilisateur n'a pas été trouvé par ID."

        # Vérifier que l'ID de l'utilisateur correspond
        assert (
            str(user["id_user"]) == utilisateur2_kwargs["id_user"]
        ), "L'ID de l'utilisateur ne correspond pas."

    finally:
        # Clean up the test data
        reseter = ResetDatabase()
        reseter.ResetTEST()
