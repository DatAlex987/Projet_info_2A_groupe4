import hashlib
import os
import pytest
from business_object.user import User


@pytest.fixture
def utilisateur():
    return User("Bocquet", "Noémie", "2003-08-08", "noemie.b", "mdpex", ["sounddeck1, sounddeck2"])


def test_initialisation(utilisateur):
    assert utilisateur.nom == "Bocquet"
    assert utilisateur.prenom == "Noémie"
    assert utilisateur.date_naissance == "2003-08-08"
    assert utilisateur.id_user == "noemie.b"
    assert utilisateur.mot_de_passe_hash is not None
    assert utilisateur.salt is not None
    assert utilisateur.sounddecks == ["sounddeck1, sounddeck2"]


def test_mot_de_passe_hash(utilisateur):
    mdp_combine = "mdpex" + utilisateur.id_user
    hash_test = hashlib.pbkdf2_hmac("sha256", mdp_combine.encode("utf-8"), utilisateur.salt, 100000)
    assert utilisateur.mot_de_passe_hash() == hash_test


def test_verifier_mot_de_passe(utilisateur):
    assert utilisateur.verifier_mot_de_passe("mdpex") == True
    assert utilisateur.verifier_mot_de_passe("mdperroné") == False


def test_supprimer_utilisateur(utilisateur):
    utilisateur.supprimer_utilisateur()
    assert utilisateur.id_user is None
    assert utilisateur.mot_de_passe_hash is None
    assert utilisateur.salt is None
    assert utilisateur.sounddecks is None
