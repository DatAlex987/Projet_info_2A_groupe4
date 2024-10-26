import pytest
from unittest.mock import patch, MagicMock
from dao.scene_dao import SceneDAO
from business_object.scene import Scene
import pygame


@pytest.fixture
def scene1(scene1_kwargs):
    return Scene(**scene1_kwargs)


def test_ajouter_scene(scene1):
    with patch("dao.db_connection.DBConnection") as mock_db:
        mock_cursor = MagicMock()
        mock_db().connection.__enter__.return_value.cursor.return_value.__enter__.return_value = (
            mock_cursor
        )

        mock_cursor.fetchone.return_value = {"id_scene": 1}  # Simuler l'ID renvoyé après insertion

        dao = SceneDAO()
        result = dao.ajouter_scene(scene1)

        assert result.id == 1  # Vérifier que l'ID est correct
        mock_cursor.execute.assert_called_once()  # Vérifier que la méthode execute a été appelée


def test_modifier_scene(scene1):
    scene1.id_scene = 1  # Simuler que l'ID de la scène est 1
    with patch("dao.db_connection.DBConnection") as mock_db:
        mock_cursor = MagicMock()
        mock_db().connection.__enter__.return_value.cursor.return_value.__enter__.return_value = (
            mock_cursor
        )

        dao = SceneDAO()
        result = dao.modifier_scene(scene1)

        assert result == scene1  # Vérifier que la scène retournée est celle que nous avons modifiée
        mock_cursor.execute.assert_called_once()  # Vérifier que la méthode execute a été appelée


def test_supprimer_scene():
    scene_id = 1
    with patch("dao.db_connection.DBConnection") as mock_db:
        mock_cursor = MagicMock()
        mock_db().connection.__enter__.return_value.cursor.return_value.__enter__.return_value = (
            mock_cursor
        )

        dao = SceneDAO()
        dao.supprimer_scene(scene_id)

        mock_cursor.execute.assert_called_once_with(
            """
            DELETE FROM ProjetInfo.Scene
            WHERE id_scene = %(id_scene)s;
            """,
            {"id_scene": scene_id},
        )


def test_consulter_scenes(scene1):
    with patch("dao.db_connection.DBConnection") as mock_db:
        mock_cursor = MagicMock()
        mock_db().connection.__enter__.return_value.cursor.return_value.__enter__.return_value = (
            mock_cursor
        )

        mock_cursor.fetchall.return_value = [
            {
                "id_scene": 1,
                "nom": scene1.nom,
                "description": scene1.description,
                "date_creation": scene1.date_creation,
            },
        ]

        dao = SceneDAO()
        result = dao.consulter_scenes()

        assert len(result) == 1  # Vérifier qu'une scène est retournée
        assert result[0].nom == scene1.nom  # Vérifier que le nom est correct
        assert (
            result[0].description == scene1.description
        )  # Vérifier que la description est correcte


def test_rechercher_par_id_scenes(scene1):
    scene_id = 1
    scene1.id_scene = scene_id
    with patch("dao.db_connection.DBConnection") as mock_db:
        mock_cursor = MagicMock()
        mock_db().connection.__enter__.return_value.cursor.return_value.__enter__.return_value = (
            mock_cursor
        )

        mock_cursor.fetchone.return_value = {
            "id_scene": scene1.id_scene,
            "nom": scene1.nom,
            "description": scene1.description,
            "date_creation": scene1.date_creation,
        }

        dao = SceneDAO()
        result = dao.rechercher_par_id_scenes(scene_id)

        assert result.nom == scene1.nom  # Vérifier que le nom de la scène est correct
        assert result.description == scene1.description  # Vérifier que la description est correcte


def test_rechercher_par_id_scenes_not_found():
    scene_id = 999
    with patch("dao.db_connection.DBConnection") as mock_db:
        mock_cursor = MagicMock()
        mock_db().connection.__enter__.return_value.cursor.return_value.__enter__.return_value = (
            mock_cursor
        )

        mock_cursor.fetchone.return_value = None  # Simuler une recherche qui ne renvoie rien

        dao = SceneDAO()
        result = dao.rechercher_par_id_scenes(scene_id)

        assert result is None  # Vérifier que le résultat est None


# Exécute les tests avec pytest
if __name__ == "__main__":
    pytest.main()
