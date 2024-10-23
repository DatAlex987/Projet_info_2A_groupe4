from unittest.mock import MagicMock, patch
import pytest
import datetime
from dao.user_dao import UserDAO
from business_object.user import User


@pytest.fixture
def mock_db_connection(mocker):
    # Création d'un mock pour la connexion à la base de données
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
    mock_db = mocker.patch("dao.db_connection.DBConnection")
    mock_db().connection.__enter__.return_value = mock_connection
    return mock_cursor


def test_ajouter_user(mock_db_connection):
    # Simuler le comportement de la base de données
    mock_db_connection.fetchone.return_value = {"id_user": 1}

    # GIVEN
    user = User(
        nom="Bocquet",
        prenom="Noémie",
        date_naissance=datetime.date(2003, 8, 8),
        id_user="Noemie",
        mdp="passWord0@",
        SD_possedes=[],
    )

    # WHEN
    user_id = UserDAO().ajouter_user(user)

    # THEN
    assert user_id == 1
