import pytest
from unittest.mock import patch, MagicMock
from dao.scene_dao import SceneDAO
from business_object.scene import Scene
import datetime


@patch("dao.scene_dao.DBConnection")
def test_ajouter_scene_succes(mock_db, scene1_kwargs):

    # GIVEN une scène à ajouter et une base de données
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (1,)  # La scène est ajoutée avec succès
    mock_db().connection.__enter__().cursor.return_value = mock_cursor

    scene_to_add = Scene(**scene1_kwargs)
    scene_dao = SceneDAO()  # Create an instance of SceneDAO

    # WHEN : on tente d'ajouter la scène
    res = scene_dao.ajouter_scene(scene_to_add)  # Use the instance to call the method

    # THEN
    assert res == scene_to_add


@patch("dao.scene_dao.DBConnection")
def test_modifier_scene_succes(mock_db, scene1_kwargs, new_name):

    # GIVEN une scène à ajouter et une base de données
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (1,)  # La scène est ajoutée avec succès
    mock_db().connection.__enter__().cursor.return_value = mock_cursor

    scene_to_add = Scene(**scene1_kwargs)
    scene_dao = SceneDAO()  # Create an instance of SceneDAO
    scene_ajoutee = scene_dao.ajouter_scene(scene_to_add)
    # WHEN : on tente de modifier la scène ajoutée
    res = scene_dao.modifier_scene(scene_ajoutee, "NouveauNom")

    # THEN
    assert
