import pytest

####
from dao.sd_dao import SDDAO
from dao.user_dao import UserDAO
from dao.db_connection import DBConnection
from business_object.sd import SD
from business_object.user import User
from utils.reset_database import ResetDatabase


def test_ajouter_sd_succes(sd_kwargs, user1_kwargs):
    ResetDatabase().ResetTEST()
    # GIVEN: A sd object to add, a user owner creator of the sd already existing and the test schema
    schema = "SchemaTest"
    sd_to_add = SD(**sd_kwargs)
    user_owner = User(**user1_kwargs)
    UserDAO().ajouter_user(user=user_owner, schema="Schematest")
    # WHEN: Adding the sd to the database
    sd_dao = SDDAO()
    added_sd = sd_dao.ajouter_sd(sd_to_add, schema)

    # THEN: The returned sd should have the correct ID, and the data should match
    assert added_sd.id_sd == sd_kwargs["id_sd"]
    assert added_sd.nom == sd_kwargs["nom"]
    assert added_sd.scenes == sd_kwargs["scenes"]
    assert added_sd.description == sd_kwargs["description"]
    assert added_sd.date_creation == sd_kwargs["date_creation"]
    assert added_sd.id_createur == sd_kwargs["id_createur"]

    # THEN: Verify the sd was added to the database by querying it
    with DBConnection(schema=schema).connection as connection:
        with connection.cursor() as cursor:
            query = f"SELECT * FROM {schema}.SoundDeck WHERE id_sd = %(id_sd)s"
            cursor.execute(
                query,
                {"id_sd": added_sd.id_sd},
            )
            result = cursor.fetchone()

            assert result is not None
            assert result["id_sd"] == sd_kwargs["id_sd"]
            assert result["nom"] == sd_kwargs["nom"]
            assert result["description"] == sd_kwargs["description"]
            assert result["date_creation"] == sd_kwargs["date_creation"]
            assert result["id_createur"] == sd_kwargs["id_createur"]

    # Clean up the test data
    reseter = ResetDatabase()
    reseter.ResetTEST()


@pytest.mark.parametrize(
    "new_nom, new_desc",
    [
        ("NouveauNom", "NouvelleDescription"),
    ],
)
def test_modifier_sd_succes(sd_kwargs, user1_kwargs, new_nom, new_desc):
    ResetDatabase().ResetTEST()
    # GIVEN: A sd object already added in the test schema the test schema
    schema = "SchemaTest"
    sd_to_add = SD(**sd_kwargs)
    user_owner = User(**user1_kwargs)
    UserDAO().ajouter_user(user=user_owner, schema="Schematest")
    sd_dao = SDDAO()
    added_sd = sd_dao.ajouter_sd(sd=sd_to_add, schema=schema)
    # WHEN: Adding the sd modified to the database
    added_sd.nom = new_nom
    added_sd.description = new_desc
    modified_added_sd = sd_dao.modifier_sd(sd=added_sd, schema=schema)
    # THEN: The returned scene should have the correct ID, and the data should match
    assert modified_added_sd.id_sd == added_sd.id_sd
    assert modified_added_sd.nom == added_sd.nom
    assert modified_added_sd.scenes == added_sd.scenes
    assert modified_added_sd.description == added_sd.description
    assert modified_added_sd.date_creation == added_sd.date_creation
    assert modified_added_sd.id_createur == added_sd.id_createur

    # THEN: Verify the sd correctly modified in the database by querying it
    with DBConnection(schema=schema).connection as connection:
        with connection.cursor() as cursor:
            query = f"SELECT * FROM {schema}.SoundDeck WHERE id_sd = %(id_sd)s"
            cursor.execute(
                query,
                {"id_sd": modified_added_sd.id_sd},
            )
            result = cursor.fetchone()

            assert result is not None
            assert result["id_sd"] == modified_added_sd.id_sd
            assert result["nom"] == modified_added_sd.nom
            assert result["description"] == modified_added_sd.description
            assert result["date_creation"] == modified_added_sd.date_creation

    # Clean up the test data
    reseter = ResetDatabase()
    reseter.ResetTEST()


def test_supprimer_sd_succes(sd_kwargs, user1_kwargs):
    ResetDatabase().ResetTEST()
    # GIVEN: A sd object to add, a user owner creator of the sd already existing and the test schema
    schema = "SchemaTest"
    sd_to_add = SD(**sd_kwargs)
    user_owner = User(**user1_kwargs)
    UserDAO().ajouter_user(user=user_owner, schema="Schematest")
    sd_dao = SDDAO()
    added_sd = sd_dao.ajouter_sd(sd_to_add, schema)
    # WHEN: Deleting the sd from the database
    sd_dao.supprimer_sd(added_sd.id_sd, schema)

    # THEN: Verify the sd correctly removed from the database by querying it
    with DBConnection(schema=schema).connection as connection:
        with connection.cursor() as cursor:
            query = f"SELECT * FROM {schema}.SoundDeck WHERE id_sd = %(id_sd)s"
            cursor.execute(
                query,
                {"id_sd": added_sd.id_sd},
            )
            result = cursor.fetchall()

            assert len(result) == 0
    # Clean up the test data
    reseter = ResetDatabase()
    reseter.ResetTEST()


def test_consulter_sds_succes(sd_kwargs, user1_kwargs):
    ResetDatabase().ResetTEST()
    # GIVEN: A sd already added in the test schema
    schema = "SchemaTest"
    sd1_to_add = SD(**sd_kwargs)
    user_owner = User(**user1_kwargs)
    UserDAO().ajouter_user(user=user_owner, schema="Schematest")
    sd_dao = SDDAO()
    sd_dao.ajouter_sd(sd1_to_add, schema)

    # WHEN: Querying the sds in the database
    all_found_sds = sd_dao.consulter_sds(schema)
    # THEN: The returned sd should have the correct ID, and the data should match
    assert len(all_found_sds) == 1
    # Clean up the test data
    reseter = ResetDatabase()
    reseter.ResetTEST()


def test_rechercher_par_id_sd_succes(sd_kwargs, user1_kwargs):
    ResetDatabase().ResetTEST()
    # GIVEN: A Sd object already added in the test schema the test schema
    schema = "SchemaTest"
    sd_to_add = SD(**sd_kwargs)
    user_owner = User(**user1_kwargs)
    UserDAO().ajouter_user(user=user_owner, schema="Schematest")
    sd_dao = SDDAO()
    added_sd = sd_dao.ajouter_sd(sd_to_add, schema)
    # WHEN: Searching for the sd id in the database
    found_sd = sd_dao.rechercher_par_id_sd(added_sd.id_sd, schema)
    # THEN: The returned sd should have the correct ID, and the data should match
    assert found_sd["id_sd"] == added_sd.id_sd
    assert found_sd["nom"] == added_sd.nom
    assert found_sd["description"] == added_sd.description
    assert found_sd["date_creation"] == added_sd.date_creation
    assert found_sd["scenes"] == added_sd.scenes

    # Clean up the test data
    reseter = ResetDatabase()
    reseter.ResetTEST()
