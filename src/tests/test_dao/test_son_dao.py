import pytest
import datetime

####
from business_object.son_aleatoire import Son_Aleatoire
from dao.son_dao import SonDAO
from dao.db_connection import DBConnection
from utils.reset_database import ResetDatabase


def test_ajouter_son_succes(son_aleatoire1_kwargs):
    ResetDatabase().ResetTEST()
    schema = "SchemaTest"
    son_to_add = Son_Aleatoire(**son_aleatoire1_kwargs)

    son_dao = SonDAO()
    added_son = son_dao.ajouter_son(son_to_add, schema)

    assert added_son.id_freesound == son_aleatoire1_kwargs["id_freesound"]
    assert added_son.id_son == son_aleatoire1_kwargs["id_son"]
    assert added_son.nom == son_aleatoire1_kwargs["nom"]
    assert added_son.description == son_aleatoire1_kwargs["description"]

    with DBConnection(schema=schema).connection as connection:
        with connection.cursor() as cursor:
            query = f"SELECT * FROM {schema}.Son WHERE id_son = %(id_son)s"
            cursor.execute(query, {"id_son": added_son.id_son})
            result = cursor.fetchone()

            assert result is not None
            assert result["id_freesound"] == son_aleatoire1_kwargs["id_freesound"]
            assert result["id_son"] == son_aleatoire1_kwargs["id_son"]
            assert result["description"] == son_aleatoire1_kwargs["description"]
            assert result["nom"] == son_aleatoire1_kwargs["nom"]

    ResetDatabase().ResetTEST()


@pytest.mark.parametrize("new_nom, new_desc", [("NouveauNomSon", "Nouvelle description")])
def test_modifier_son_succes(son_aleatoire1_kwargs, new_nom, new_desc):
    ResetDatabase().ResetTEST()
    schema = "SchemaTest"
    son_to_add = Son_Aleatoire(**son_aleatoire1_kwargs)
    son_dao = SonDAO()
    added_son = son_dao.ajouter_son(son_to_add, schema)

    added_son.nom = new_nom
    added_son.description = new_desc
    modified_added_son = son_dao.modifier_son(added_son, schema)

    assert modified_added_son.id_son == added_son.id_son
    assert modified_added_son.id_freesound == added_son.id_freesound
    assert modified_added_son.nom == added_son.nom
    assert modified_added_son.description == added_son.description

    with DBConnection(schema=schema).connection as connection:
        with connection.cursor() as cursor:
            query = f"SELECT * FROM {schema}.Son WHERE id_son = %(id_son)s"
            cursor.execute(query, {"id_son": modified_added_son.id_son})
            result = cursor.fetchone()

            assert result is not None
            assert result["id_son"] == modified_added_son.id_son
            assert result["id_freesound"] == modified_added_son.id_freesound
            assert result["nom"] == modified_added_son.nom
            assert result["description"] == modified_added_son.description

    ResetDatabase().ResetTEST()


def test_supprimer_son_succes(son_aleatoire1_kwargs):
    ResetDatabase().ResetTEST()
    schema = "SchemaTest"
    son_to_add = Son_Aleatoire(**son_aleatoire1_kwargs)
    son_dao = SonDAO()
    added_son = son_dao.ajouter_son(son_to_add, schema)

    son_dao.supprimer_son(added_son.id_son, schema)

    with DBConnection(schema=schema).connection as connection:
        with connection.cursor() as cursor:
            query = f"SELECT * FROM {schema}.Son WHERE id_son = %(id_son)s"
            cursor.execute(query, {"id_son": added_son.id_son})
            result = cursor.fetchall()
            assert len(result) == 0

    ResetDatabase().ResetTEST()


def test_consulter_sons_succes(son_aleatoire1_kwargs, son_aleatoire2_kwargs):
    ResetDatabase().ResetTEST()
    schema = "SchemaTest"
    son1_to_add = Son_Aleatoire(**son_aleatoire1_kwargs)
    son2_to_add = Son_Aleatoire(**son_aleatoire2_kwargs)
    son_dao = SonDAO()
    son_dao.ajouter_son(son1_to_add, schema)
    son_dao.ajouter_son(son2_to_add, schema)

    all_found_sons = son_dao.consulter_sons(schema)
    assert len(all_found_sons) == 2

    ResetDatabase().ResetTEST()


def test_rechercher_par_id_son_succes(son_aleatoire1_kwargs):
    ResetDatabase().ResetTEST()
    schema = "SchemaTest"
    son_to_add = Son_Aleatoire(**son_aleatoire1_kwargs)
    son_dao = SonDAO()
    added_son = son_dao.ajouter_son(son_to_add, schema)

    found_son = son_dao.rechercher_par_id_son(added_son.id_son, schema)
    assert found_son["id_freesound"] == str(added_son.id_freesound)
    assert found_son["id_son"] == str(added_son.id_son)
    assert found_son["nom"] == added_son.nom
    assert found_son["description"] == added_son.description

    ResetDatabase().ResetTEST()
