import pytest
from dao.scene_dao import SceneDAO
from business_object.scene import Scene
from dao.db_connection import DBConnection


def test_ajouter_scene_succes(scene1_kwargs):
    # GIVEN: A Scene object to add and the test schema
    schema = "SchemaTest"
    scene_to_add = Scene(**scene1_kwargs)

    # WHEN: Adding the scene to the database
    scene_dao = SceneDAO()
    added_scene = scene_dao.ajouter_scene(scene_to_add, schema)

    # THEN: The returned scene should have the correct ID, and the data should match
    assert added_scene.id_scene == scene1_kwargs["id_scene"]
    assert added_scene.nom == scene1_kwargs["nom"]
    assert added_scene.sons_aleatoires == scene1_kwargs["sons_aleatoires"]
    assert added_scene.sons_continus == scene1_kwargs["sons_continus"]
    assert added_scene.sons_manuels == scene1_kwargs["sons_manuels"]
    assert added_scene.description == scene1_kwargs["description"]
    assert added_scene.date_creation == scene1_kwargs["date_creation"]

    # THEN: Verify the scene was added to the database by querying it
    with DBConnection(schema=schema).connection as connection:
        with connection.cursor() as cursor:
            query = f"SELECT * FROM {schema}.Scene WHERE id_scene = %(id_scene)s"
            cursor.execute(
                query,
                {"id_scene": added_scene.id_scene},
            )
            result = cursor.fetchone()

            assert result is not None
            assert result["id_scene"] == int(scene1_kwargs["id_scene"])
            assert result["nom"] == scene1_kwargs["nom"]
            assert result["description"] == scene1_kwargs["description"]
            assert result["date_creation"] == scene1_kwargs["date_creation"]

    # Clean up the test data
    with DBConnection(schema=schema).connection as connection:
        with connection.cursor() as cursor:
            query = f"DELETE FROM {schema}.Scene WHERE id_scene = %(id_scene)s"
            cursor.execute(
                query,
                {"id_scene": added_scene.id_scene},
            )


@pytest.mark.parametrize(
    "new_nom, new_desc",
    [
        ("NouveauNom", "NouvelleDescription"),
    ],
)
def test_modifier_scene_succes(scene1_kwargs, new_nom, new_desc):
    # GIVEN: A Scene object already added in the test schema the test schema
    schema = "SchemaTest"
    scene_to_add = Scene(**scene1_kwargs)
    scene_dao = SceneDAO()
    added_scene = scene_dao.ajouter_scene(scene_to_add, schema)
    # WHEN: Adding the scene modified to the database
    added_scene.nom = new_nom
    added_scene.description = new_desc
    modified_added_scene = scene_dao.modifier_scene(added_scene, schema)
    # THEN: The returned scene should have the correct ID, and the data should match
    assert modified_added_scene.id_scene == scene1_kwargs["id_scene"]
    assert modified_added_scene.nom == added_scene.nom
    assert modified_added_scene.sons_aleatoires == added_scene.sons_aleatoires
    assert modified_added_scene.sons_continus == added_scene.sons_continus
    assert modified_added_scene.sons_manuels == added_scene.sons_manuels
    assert modified_added_scene.description == added_scene.description
    assert modified_added_scene.date_creation == added_scene.date_creation

    # THEN: Verify the scene correctly modified in the database by querying it
    with DBConnection(schema=schema).connection as connection:
        with connection.cursor() as cursor:
            query = f"SELECT * FROM {schema}.Scene WHERE id_scene = %(id_scene)s"
            cursor.execute(
                query,
                {"id_scene": modified_added_scene.id_scene},
            )
            result = cursor.fetchone()

            assert result is not None
            assert result["id_scene"] == int(modified_added_scene.id_scene)
            assert result["nom"] == modified_added_scene.nom
            assert result["description"] == modified_added_scene.description
            assert result["date_creation"] == modified_added_scene.date_creation

    # Clean up the test data
    with DBConnection(schema=schema).connection as connection:
        with connection.cursor() as cursor:
            query = f"DELETE FROM {schema}.Scene WHERE id_scene = %(id_scene)s"
            cursor.execute(
                query,
                {"id_scene": modified_added_scene.id_scene},
            )


def test_supprimer_scene_succes(scene1_kwargs):
    # GIVEN: A Scene object already added in the test schema
    schema = "SchemaTest"
    scene_to_add = Scene(**scene1_kwargs)
    scene_dao = SceneDAO()
    added_scene = scene_dao.ajouter_scene(scene_to_add, schema)
    # WHEN: Deleting the scene from the database
    scene_dao.supprimer_scene(added_scene.id_scene, schema)

    # THEN: Verify the scene is correctly removed from the database by querying it
    with DBConnection(schema=schema).connection as connection:
        with connection.cursor() as cursor:
            query = f"SELECT * FROM {schema}.Scene WHERE id_scene = %(id_scene)s"
            cursor.execute(
                query,
                {"id_scene": added_scene.id_scene},
            )
            result = cursor.fetchall()

            assert len(result) == 0


def test_consulter_scenes_succes(scene1_kwargs, scene2_kwargs):
    # GIVEN: 2 scenes already added in the test schema
    schema = "SchemaTest"
    scene1_to_add = Scene(**scene1_kwargs)
    scene2_to_add = Scene(**scene2_kwargs)
    scene_dao = SceneDAO()
    scene_dao.ajouter_scene(scene1_to_add, schema)
    scene_dao.ajouter_scene(scene2_to_add, schema)
    # WHEN: Querying the scenes in the database
    all_found_scenes = scene_dao.consulter_scenes(schema)
    # THEN: The returned list of scenes should have the correct length
    assert len(all_found_scenes) == 2
    # Clean up the test data
    for found_scene in all_found_scenes:
        with DBConnection(schema=schema).connection as connection:
            with connection.cursor() as cursor:
                query = f"DELETE FROM {schema}.Scene WHERE id_scene = %(id_scene)s"
                cursor.execute(
                    query,
                    {"id_scene": found_scene.id_scene},
                )


def test_rechercher_par_id_scenes_succes(scene1_kwargs):
    # GIVEN: A Scene object already added in the test schema the test schema
    schema = "SchemaTest"
    scene_to_add = Scene(**scene1_kwargs)
    scene_dao = SceneDAO()
    added_scene = scene_dao.ajouter_scene(scene_to_add, schema)
    # WHEN: Searching for the scene id in the database
    found_scene = scene_dao.rechercher_par_id_scenes(added_scene.id_scene, schema)
    # THEN: The returned scene should have the correct ID, and the data should match
    assert found_scene.id_scene == str(added_scene.id_scene)
    assert found_scene.nom == added_scene.nom
    # assert found_scene.sons_aleatoires == added_scene.sons_aleatoires
    # assert found_scene.sons_continus == added_scene.sons_continus
    # assert found_scene.sons_manuels == added_scene.sons_manuels
    assert found_scene.description == added_scene.description
    assert found_scene.date_creation == added_scene.date_creation

    # Clean up the test data
    with DBConnection(schema=schema).connection as connection:
        with connection.cursor() as cursor:
            query = f"DELETE FROM {schema}.Scene WHERE id_scene = %(id_scene)s"
            cursor.execute(
                query,
                {"id_scene": added_scene.id_scene},
            )
