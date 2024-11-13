import pytest
from dao.son_dao import SonDAO
from business_object.son import Son
from dao.db_connection import DBConnection
from utils.reset_database import ResetDatabase


def test_ajouter_son_succes(son_aleatoire1_kwargs):
    ResetDatabase().ResetTEST()
    schema = "SchemaTest"
    son_to_add = Son(**son_aleatoire1_kwargs)

    son_dao = SonDAO()
    added_son = son_dao.ajouter_son(son_to_add, schema)

    assert added_son.id_son == son_aleatoire1_kwargs["id_son"]
    assert added_son.nom == son_aleatoire1_kwargs["nom"]
    assert added_son.type == son_aleatoire1_kwargs["type"]
    assert added_son.duree == son_aleatoire1_kwargs["duree"]
    assert added_son.date_creation == son_aleatoire1_kwargs["date_creation"]

    with DBConnection(schema=schema).connection as connection:
        with connection.cursor() as cursor:
            query = f"SELECT * FROM {schema}.Son WHERE id_son = %(id_son)s"
            cursor.execute(query, {"id_son": added_son.id_son})
            result = cursor.fetchone()

            assert result is not None
            assert result["id_son"] == son_aleatoire1_kwargs["id_son"]
            assert result["nom"] == son_aleatoire1_kwargs["nom"]
            assert result["type"] == son_aleatoire1_kwargs["type"]
            assert result["duree"] == son_aleatoire1_kwargs["duree"]

    ResetDatabase().ResetTEST()


@pytest.mark.parametrize("new_nom, new_duree", [("NouveauNomSon", 300)])
def test_modifier_son_succes(son_aleatoire1_kwargs, new_nom, new_duree):
    ResetDatabase().ResetTEST()
    schema = "SchemaTest"
    son_to_add = Son(**son_aleatoire1_kwargs)
    son_dao = SonDAO()
    added_son = son_dao.ajouter_son(son_to_add, schema)

    added_son.nom = new_nom
    added_son.duree = new_duree
    modified_added_son = son_dao.modifier_son(added_son, schema)

    assert modified_added_son.id_son == added_son.id_son
    assert modified_added_son.nom == added_son.nom
    assert modified_added_son.type == added_son.type
    assert modified_added_son.duree == added_son.duree
    assert modified_added_son.date_creation == added_son.date_creation

    with DBConnection(schema=schema).connection as connection:
        with connection.cursor() as cursor:
            query = f"SELECT * FROM {schema}.Son WHERE id_son = %(id_son)s"
            cursor.execute(query, {"id_son": modified_added_son.id_son})
            result = cursor.fetchone()

            assert result is not None
            assert result["id_son"] == modified_added_son.id_son
            assert result["nom"] == modified_added_son.nom
            assert result["duree"] == modified_added_son.duree

    ResetDatabase().ResetTEST()


def test_supprimer_son_succes(son_aleatoire1_kwargs):
    ResetDatabase().ResetTEST()
    schema = "SchemaTest"
    son_to_add = Son(**son_aleatoire1_kwargs)
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
    son1_to_add = Son(**son_aleatoire1_kwargs)
    son2_to_add = Son(**son_aleatoire2_kwargs)
    son_dao = SonDAO()
    son_dao.ajouter_son(son1_to_add, schema)
    son_dao.ajouter_son(son2_to_add, schema)

    all_found_sons = son_dao.consulter_sons(schema)
    assert len(all_found_sons) == 2

    ResetDatabase().ResetTEST()


def test_rechercher_par_id_son_succes(son_aleatoire1_kwargs):
    ResetDatabase().ResetTEST()
    schema = "SchemaTest"
    son_to_add = Son(**son_aleatoire1_kwargs)
    son_dao = SonDAO()
    added_son = son_dao.ajouter_son(son_to_add, schema)

    found_son = son_dao.rechercher_par_id_son(added_son.id_son, schema)
    assert found_son["id_son"] == str(added_son.id_son)
    assert found_son["nom"] == added_son.nom
    assert found_son["type"] == added_son.type
    assert found_son["duree"] == added_son.duree

    ResetDatabase().ResetTEST()
