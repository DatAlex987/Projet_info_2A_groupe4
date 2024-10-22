import os
import pytest
from unittest.mock import patch
from utils.reset_database import ResetDatabase
from utils.securite import hash_password

from dao.user_dao import UserDAO
from business_object.user import User


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Initialisation des données de test"""
    with patch.dict(os.environ, {"SCHEMA": "ProjetInfo"}):
        ResetDatabase().lancer(test_dao=True)
        yield


def test_ajouter_user_succes():
    """Création d'un utilisateur réussie"""

    # GIVEN
    user = User(
        nom="Bocquet",
        prenom="Noémie",
        date_naissance="2003-08-08",
        id_user="Noemie",
        mdp="password",
        SD_possedes=[],
    )

    # WHEN
    user_id = UserDAO().ajouter_user(user)

    # THEN
    assert user_id is not None
    assert isinstance(user_id, int)


def test_ajouter_user_echec():
    """Création d'un utilisateur échouée"""

    # GIVEN
    user = User(
        nom="Bocquet",
        prenom="Noémie",
        date_naissance="2003-08-08",
        id_user="",
        mdp="password",
        SD_possedes=[],
    )

    # WHEN
    user_id = UserDAO().ajouter_user(user)

    # THEN
    assert user_id is None


def test_rechercher_par_id_user_existant():
    """Recherche par ID d'un utilisateur existant"""

    # GIVEN
    user = User(
        nom="Bocquet",
        prenom="Noémie",
        date_naissance="2003-08-08",
        id_user="Noemie",
        mdp="password",
        SD_possedes=[],
    )
    user_id = UserDAO().ajouter_user(user)

    # WHEN
    found_user = UserDAO().rechercher_par_id_user(user_id)

    # THEN
    assert found_user is not None


def test_rechercher_par_id_user_non_existant():
    """Recherche par ID d'un utilisateur n'existant pas"""

    # GIVEN
    id_user = 999999

    # WHEN
    user = UserDAO().rechercher_par_id_user(id_user)

    # THEN
    assert user is None


def test_supprimer_user_succes():
    """Suppression d'un utilisateur réussie"""

    # GIVEN
    user = User(
        nom="Bocquet",
        prenom="Noémie",
        date_naissance="2003-08-08",
        id_user="Noemie",
        mdp="password",
        SD_possedes=[],
    )
    user_id = UserDAO().ajouter_user(user)

    # WHEN
    suppression_reussie = UserDAO().supprimer_user(user_id)

    # THEN
    assert suppression_reussie


def test_supprimer_user_echec():
    """Suppression d'un utilisateur échouée (ID inconnu)"""

    # GIVEN
    user_id = 999999  # ID qui n'existe pas

    # WHEN
    suppression_reussie = UserDAO().supprimer_user(user_id)

    # THEN
    assert not suppression_reussie


if __name__ == "__main__":
    pytest.main([__file__])
