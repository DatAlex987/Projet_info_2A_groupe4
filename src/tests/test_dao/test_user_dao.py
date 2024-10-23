import os
import pytest
from unittest.mock import MagicMock, patch
from business_object.user import User
from dao.user_dao import UserDAO
from datetime import date


@pytest.fixture
def mock_user_dao(mocker):
    """Fixture pour mocker UserDAO."""
    mock_dao = mocker.patch("dao.user_dao.UserDAO")
    mock_dao_instance = mock_dao.return_value

    mock_dao_instance.ajouter_user.return_value = 12345

    mock_dao_instance.supprimer_user.return_value = True

    mock_dao_instance.consulter_users.return_value = [
        {
            "id_user": "123",
            "nom": "Bocquet",
            "prenom": "Noémie",
            "date_naissance": date(2003, 8, 8),
            "mdp": "Mdpexemple2@",
        },
        {
            "id_user": "124",
            "nom": "Sanier",
            "prenom": "Theo",
            "date_naissance": date(2000, 5, 15),
            "mdp": "MotDePasse@2024",
        },
    ]

    mock_dao_instance.rechercher_par_id_user.return_value = {
        "id_user": "123",
        "nom": "Bocquet",
        "prenom": "Noémie",
        "date_naissance": date(2003, 8, 8),
        "mdp": "Mdpexemple2@",
    }

    mock_dao_instance.ajouter_sounddeck.return_value = None

    mock_dao_instance.consulter_sounddecks_par_user.return_value = [
        "Sounddeck 1",
        "Sounddeck 2",
    ]

    mock_dao_instance.supprimer_sounddeck.return_value = True
    mock_dao_instance.schema = "projetinfo"

    return mock_dao_instance


def test_ajouter_user(mock_user_dao):
    """Test l'ajout d'un utilisateur sans affecter la base de données."""

    # GIVEN
    user = User(
        nom="Bocquet",
        prenom="Noémie",
        date_naissance=date(2003, 8, 8),
        id_user="12345",
        mdp="Mdpexemple2@",
        SD_possedes=[],
    )

    # WHEN
    user_id = mock_user_dao.ajouter_user(user)

    # THEN
    assert user_id == 12345
    mock_user_dao.ajouter_user.assert_called_once_with(user)


def test_supprimer_user(mock_user_dao):
    """Test la suppression d'un utilisateur sans affecter la base de données."""

    # GIVEN
    user_id = 1234

    # WHEN
    result = mock_user_dao.supprimer_user(user_id)

    # THEN
    assert result is True
    mock_user_dao.supprimer_user.assert_called_once_with(user_id)


def test_consulter_users(mock_user_dao):
    """Test la consultation des utilisateurs sans affecter la base de données."""

    # WHEN
    users = mock_user_dao.consulter_users()

    # THEN
    assert len(users) == 2
    assert users[0]["nom"] == "Bocquet"
    assert users[1]["prenom"] == "Theo"
    mock_user_dao.consulter_users.assert_called_once()


def test_rechercher_par_id_user(mock_user_dao):
    """Test la recherche d'un utilisateur par son ID sans affecter la base de données."""

    # GIVEN
    user_id = "123"

    # WHEN
    user = mock_user_dao.rechercher_par_id_user(user_id)

    # THEN
    assert user["id_user"] == "123"
    assert user["nom"] == "Bocquet"
    assert user["prenom"] == "Noémie"
    mock_user_dao.rechercher_par_id_user.assert_called_once_with(user_id)


def test_ajouter_sounddeck(mock_user_dao):
    """Test l'ajout d'un sounddeck pour un utilisateur sans affecter la base de données."""

    # GIVEN
    id_user = 123
    nom_sounddeck = "Nouveau Sounddeck"

    # WHEN
    mock_user_dao.ajouter_sounddeck(id_user, nom_sounddeck)

    # THEN
    mock_user_dao.ajouter_sounddeck.assert_called_once_with(id_user, nom_sounddeck)


def test_consulter_sounddecks_par_user(mock_user_dao):
    """Test la consultation des sounddecks d'un utilisateur sans affecter la base de données."""

    # GIVEN
    user = User(
        id_user="123",
        nom="Bocquet",
        prenom="Noémie",
        date_naissance=date(2003, 8, 8),
        mdp="Mdpexemple2@",
        SD_possedes=[],
    )

    # WHEN
    sounddecks = mock_user_dao.consulter_sounddecks_par_user(user)

    # THEN
    assert len(sounddecks) == 2
    assert sounddecks[0] == "Sounddeck 1"

    mock_user_dao.consulter_sounddecks_par_user.assert_called_once_with(user)
