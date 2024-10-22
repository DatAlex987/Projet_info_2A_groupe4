import pytest
from unittest.mock import patch, MagicMock
from dao.scene_dao import SceneDAO
from business_object.scene import Scene
import datetime


@pytest.fixture
def mock_db_connection(mocker):
    # Mock the DBConnection and its connection and cursor
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
    mock_db = mocker.patch("dao.db_connection.DBConnection")
    mock_db().connection.__enter__.return_value = mock_connection
    return mock_cursor


def test_ajouter_scene(mock_db_connection, scene1_kwargs):
    # Mock the cursor's fetchone to return an ID for the inserted scene
    mock_db_connection.fetchone.return_value = {"id_scene": 1}

    # Initialize DAO and call ajouter_scene
    dao = SceneDAO()
    Scene_ajoute = Scene(**scene1_kwargs)
    returned_scene = dao.ajouter_scene(Scene_ajoute)

    # Assertions
    assert returned_scene.id == 1
    mock_db_connection.execute.assert_called_once_with(
        """
        INSERT INTO ProjetInfo.Scene(nom, description, date_creation)
        VALUES (%(nom)s, %(description)s, %(date_creation)s)
        RETURNING id_scene;
        """,
        {
            "nom": Scene_ajoute.nom,
            "description": Scene_ajoute.description,
            "date_creation": Scene_ajoute.date_creation,
        },
    )


@patch("dao.db_connection.DBConnection")
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
    assert res is True
