import pytest
from unittest.mock import patch, MagicMock
from dao.sd_dao import SDDAO
from business_object.sd import SD
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


def test_ajouter_sd(mock_db_connection, sd_kwargs):
    # Mock the cursor's fetchone to return an ID for the inserted sd
    mock_db_connection.fetchone.return_value = {"id_sd": 1}

    # Initialize DAO and call ajouter_scene
    dao = SDDAO()
    Sd_ajoute = SD(**sd_kwargs)
    returned_sd = dao.ajouter_sd(Sd_ajoute)

    # Assertions
    assert returned_sd.id == 1
    mock_db_connection.execute.assert_called_once_with(
        """
        INSERT INTO ProjetInfo.SoundDeck(nom, description, date_creation)
        VALUES (%(nom)s, %(description)s, %(date_creation)s)
        RETURNING id_sd;
        """,
        {
            "nom": Sd_ajoute.nom,
            "description": Sd_ajoute.description,
            "date_creation": Sd_ajoute.date_creation,
        },
    )

 @patch("dao.sd_dao.db_connection.DBConnection")
def test_ajouter_sd_succes(mock_db, sd_kwargs):

    # GIVEN un sd à ajouter et une base de données
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (1,)  # Le sd est ajoutée avec succès
    mock_db().connection.__enter__().cursor.return_value = mock_cursor

    sd_to_add = SD(**sd_kwargs)
    sd_dao = SDDAO()  # Create an instance of SDDAO

    # WHEN : on tente d'ajouter le sd
    res = sd_dao.ajouter_sd(sd_to_add)  # Use the instance to call the method

    # THEN
    assert res == sd_to_add
