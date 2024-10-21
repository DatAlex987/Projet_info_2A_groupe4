import os
import pytest
from unittest.mock import patch
from src.utils.reset_database import ResetDatabase
from src.utils.securite import hash_password

from src.dao.user_dao import UserDAO
from src.business_object.user import User


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Initialisation des données de test"""
    with patch.dict(os.environ, {"SCHEMA": "projet_test_dao"}):
        ResetDatabase().lancer(test_dao=True)
        yield


def test_ajouter_user_ok():
    """Création d'un utilisateur réussie"""

    # GIVEN
    user = User(
        pseudo="Noemie",
        mdp_hashe=hash_password("password", "Noemie"),
        age=21,
        nom="Bocquet",
        prenom="Noémie",
    )

    # WHEN
    user_id = UserDAO().ajouter_user(user.pseudo, user.mdp_hashe, user.age, user.nom, user.prenom)

    # THEN
    assert user_id is not None
    assert isinstance(user_id, int)


def test_ajouter_user_ko():
    """Création d'un utilisateur échouée (données invalides)"""

    # GIVEN
    user = User(pseudo="", mdp_hashe="password", age=-1, nom="Bocquet", prenom="Noémie")

    # WHEN
    user_id = UserDAO().ajouter_user(user.pseudo, user.mdp_hashe, user.age, user.nom, user.prenom)

    # THEN
    assert user_id is None


def test_rechercher_par_id_user_existant():
    """Recherche par ID d'un utilisateur existant"""

    # GIVEN
    id_user = "Noemie"

    # WHEN
    user = UserDAO().rechercher_par_id_user(id_user)

    # THEN
    assert user is not None


def test_rechercher_par_id_user_non_existant():
    """Recherche par ID d'un utilisateur n'existant pas"""

    # GIVEN
    id_user = 999999  # ID qui n'existe pas

    # WHEN
    user = UserDAO().rechercher_par_id_user(id_user)

    # THEN
    assert user is None


def test_supprimer_user_ok():
    """Suppression d'un utilisateur réussie"""

    # GIVEN
    user_id = "Noemie"

    # WHEN
    suppression_ok = UserDAO().supprimer_user(user_id)

    # THEN
    assert suppression_ok


def test_supprimer_user_ko():
    """Suppression d'un utilisateur échouée (ID inconnu)"""

    # GIVEN
    user_id = 999999  # ID qui n'existe pas

    # WHEN
    suppression_ok = UserDAO().supprimer_user(user_id)

    # THEN
    assert not suppression_ok


if __name__ == "__main__":
    pytest.main([__file__])
