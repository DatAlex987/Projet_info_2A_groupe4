import pytest
from dao.scene_dao import SceneDAO
from business_object.scene import Scene
from dao.db_connection import DBConnection
import datetime


def test_ajouter_scene_schema_test(scene1_kwargs):
    """Test that a scene is correctly added to the test schema."""
    # GIVEN: A Scene object to add and the test schema
    schema = "SchemaTest"
    scene_to_add = Scene(**scene1_kwargs)

    # WHEN: Adding the scene to the database
    scene_dao = SceneDAO()
    added_scene = scene_dao.ajouter_scene(scene_to_add, schema)

    # THEN: The returned scene should have the correct ID, and the data should match
    assert added_scene.id_scene == scene1_kwargs["id_scene"]
    assert added_scene.nom == scene1_kwargs["nom"]
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

    # (Optional) Clean up the test data
    with DBConnection(schema=schema).connection as connection:
        with connection.cursor() as cursor:
            query = f"DELETE FROM {schema}.Scene WHERE id_scene = %(id_scene)s"
            cursor.execute(
                query,
                {"id_scene": added_scene.id_scene},
            )
