import hashlib
import pytest
from business_object.user import User
from datetime import date


@pytest.mark.parametrize(
    "nom, prenom, date_naissance, id_user, mdp, SD_possedes, expected_error, error_type",
    [
        (
            123,
            "Noémie",
            date(2003, 8, 8),
            "noemie.b",
            "Mdpexample@1",
            [],
            "Le nom doit être une instance de str.",
            TypeError,
        ),
        (
            "Bocquet",
            456,
            date(2003, 8, 8),
            "noemie.b",
            "Mdpexample@1",
            [],
            "Le prénom doit être une instance de str.",
            TypeError,
        ),
        (
            "Bocquet",
            "Noémie",
            789,
            "noemie.b",
            "Mdpexample@1",
            [],
            "La date de naissance doit être une instance de datetime.",
            TypeError,
        ),
        (
            "Bocquet",
            "Noémie",
            date(2003, 8, 8),
            123,
            "Mdpexample@1",
            [],
            "Le nom d'utilisateur doit être une instance de str.",
            TypeError,
        ),
        (
            "Bocquet",
            "Noémie",
            date(2003, 8, 8),
            "noemie.b",
            456,
            [],
            "Le mot de passe doit être une instance de str.",
            TypeError,
        ),
        (
            "Bocquet",
            "Noémie",
            date(2003, 8, 8),
            "noemie.b",
            "Mdpexample@1",
            "not_a_list",
            "La liste des Sound-decks possédées doit être une instance de list.",
            TypeError,
        ),
        (
            "Bocquet",
            "Noémie",
            "invalid_date",
            "noemie.b",
            "Mdpexample@1",
            [],
            "La date de naissance doit être au format 'YYYY-MM-DD'.",
            ValueError,
        ),
    ],
)
def test_initialisation_erreurs(
    nom, prenom, date_naissance, id_user, mdp, SD_possedes, expected_error, error_type
):
    """Test les erreurs d'initialisation de l'utilisateur."""
    with pytest.raises(error_type, match=expected_error):
        User(nom, prenom, date_naissance, id_user, mdp, SD_possedes)


def test_initialisation_succes(nom, prenom, date_naissance, id_user, mdp, SD_possedes):
    """Test l'initialisation de l'utilisateur avec succès."""
    utilisateur = User(nom, prenom, date_naissance, id_user, mdp, SD_possedes)
    assert utilisateur.nom == nom
    assert utilisateur.prenom == prenom
    assert utilisateur.date_naissance == date_naissance
    assert utilisateur.id_user == id_user
    assert utilisateur.mot_de_passe_hash is not None
    assert utilisateur.SD_possedes == []


def test_supprimer_utilisateur(utilisateur_kwargs):
    """Test la suppression de l'utilisateur."""
    utilisateur = User(**utilisateur_kwargs)
    utilisateur.supprimer_utilisateur()
    assert utilisateur.id_user is None
    assert utilisateur.mot_de_passe_hash is None
    assert utilisateur.SD_possedes == []


def test_mot_de_passe_hash(utilisateur_kwargs):
    """Test le hachage du mot de passe."""
    utilisateur = User(**utilisateur_kwargs)
    mdp_combine = utilisateur_kwargs["mdp"] + utilisateur_kwargs["id_user"]
    hash_test = hashlib.pbkdf2_hmac(
        "sha256", mdp_combine.encode("utf-8"), utilisateur.nom.encode("utf-8"), 100000
    )
    assert utilisateur.mot_de_passe_hash == hash_test
