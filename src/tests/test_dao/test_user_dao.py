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

                # Assurez-vous que vous comparez le bon ID ici
                assert (
                    result["id_user"] == added_user.id_user
                ), "L'ID de l'utilisateur ne correspond pas."

    finally:
        # Clean up the test data
        reseter = ResetDatabase()
        reseter.ResetTEST()


def test_supprimer_user_succes(user_dao, utilisateur2_kwargs, schema_test):
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

    def compare_test(user_dao, utilisateur2_kwargs, shema_test):
        pass


# def test_ajouter_sounddeck(user_dao, utilisateur2_kwargs, schema_test):
#     """Test qu'un sounddeck peut être ajouté pour un utilisateur."""
#     user_to_add = User(**utilisateur2_kwargs)

#     try:
#         # Ajouter l'utilisateur
#         user_dao.ajouter_user(user_to_add, schema_test)

#         sounddeck_name = "My Sounddeck"
#         user_dao.ajouter_sounddeck(user_to_add, sounddeck_name, schema_test)

#         # Vérifier que le sounddeck a été ajouté
#         assert (
#             sounddeck_name in user_to_add.SD_possedes
#         ), "Le sounddeck n'a pas été ajouté pour l'utilisateur."

#         # Vérifier dans la base de données
#         with DBConnection(schema=schema_test).connection as connection:
#             with connection.cursor() as cursor:
#                 cursor.execute(
#                     f"SELECT * FROM {schema_test}.utilisateur WHERE id_user = %(id_user)s AND nom
# = %(nom)s",
#                     {"id_user": user_to_add.id_user, "nom": sounddeck_name},
#                 )
#                 result = cursor.fetchone()
#                 assert (
#                     result is not None
#                 ), "Le sounddeck n'a pas été trouvé dans la base de données."
#                 # Vérifiez ici que le nom est bien celui du sounddeck
#                 assert result["SD_possedes"] is not None, "La liste des sounddecks est vide."
#                 assert (
#                     sounddeck_name in result["SD_possedes"]
#                 ), "Le sounddeck n'est pas présent dans la liste des sounddecks."
#     finally:
#         user_dao.supprimer_user(utilisateur2_kwargs["id_user"], schema_test)


# def test_consulter_sounddecks_par_user(user_dao, utilisateur2_kwargs, schema_test):
#     """Test que les sounddecks pour un utilisateur peuvent être récupérés."""
#     user_to_add = User(**utilisateur2_kwargs)

#     try:
#         user_dao.ajouter_user(user_to_add, schema_test)

#         sounddeck_name = "My Sounddeck"
#         user_dao.ajouter_sounddeck(user_to_add, sounddeck_name, schema_test)

#         # Vérifier que le sounddeck est dans la liste des sounddecks de l'utilisateur
#         sounddecks = user_dao.consulter_sounddecks_par_user(user_to_add, schema_test)
#         assert sounddeck_name in sounddecks, "Le sounddeck n'a pas été trouvé pour l'utilisateur."

#         # Vérifier aussi dans la base de données
#         with DBConnection(schema=schema_test).connection as connection:
#             with connection.cursor() as cursor:
#                 cursor.execute(
#                     f"SELECT nom FROM {schema_test}.utilisateur WHERE id_user = %(id_user)s",
#                     {"id_user": utilisateur2_kwargs["id_user"]},  # Utiliser l'ID de l'utilisateur
#                 )
#                 results = cursor.fetchall()
#                 sounddeck_names = [r["nom"] for r in results]
#                 assert (
#                     sounddeck_name in sounddeck_names
#                 ), "Le sounddeck n'a pas été trouvé dans la base de données."
#     finally:
#         user_dao.supprimer_user(utilisateur2_kwargs["id_user"], schema_test)


# def test_supprimer_sounddeck(user_dao, utilisateur2_kwargs, schema_test):
#     """Test qu'un sounddeck peut être supprimé d'un utilisateur."""
#     user_to_add = User(**utilisateur2_kwargs)

#     try:
#         user_dao.ajouter_user(user_to_add, schema_test)

#         sounddeck_name = "My Sounddeck"
#         user_dao.ajouter_sounddeck(user_to_add, sounddeck_name, schema_test)

#         assert (
#             user_dao.supprimer_sounddeck(user_to_add, sounddeck_name, schema_test) is True
#         ), "La suppression du sounddeck a échoué."

#         # Vérifier que le sounddeck a été supprimé
#         assert (
#             sounddeck_name not in user_to_add.SD_possedes
#         ), "Le sounddeck n'a pas été supprimé de l'utilisateur."

#         # Vérifier dans la base de données
#         with DBConnection(schema=schema_test).connection as connection:
#             with connection.cursor() as cursor:
#                 cursor.execute(
#                     f"SELECT nom FROM {schema_test}.utilisateur WHERE id_user = %(id_user)s AND
# nom = %(nom)s",
#                     {
#                         "id_user": utilisateur2_kwargs["id_user"],
#                         "nom": sounddeck_name,
#                     },  # Utiliser l'ID de l'utilisateur
#                 )
#                 result = cursor.fetchone()
#                 assert result is None, "Le sounddeck n'a pas été supprimé de la base de données."
#     finally:
#         user_dao.supprimer_user(utilisateur2_kwargs["id_user"], schema_test)
