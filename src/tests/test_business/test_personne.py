import pytest
import re
from business_object.personne import Personne


def test_modifier_nom_personne_succes(personne1_kwargs):
    personne_test = Personne(**personne1_kwargs)
    personne_test.modifier_nom_personne("LastName")
    assert personne_test.nom == "LastName"


@pytest.mark.parametrize(
    "new_nom, expected_error, error_type",
    [(15, "Le nouveau nom doit être une instance de str.", TypeError)],
)
def test_modifier_nom_personne_echec(personne1_kwargs, new_nom, expected_error, error_type):
    with pytest.raises(error_type, match=re.escape(expected_error)):
        personne_test = Personne(**personne1_kwargs)
        personne_test.modifier_nom_personne(new_nom)


def test_modifier_prenom_personne_succes(personne1_kwargs):
    personne_test = Personne(**personne1_kwargs)
    personne_test.modifier_prenom_personne("David")
    assert personne_test.prenom == "David"


@pytest.mark.parametrize(
    "new_prenom, expected_error, error_type",
    [(15, "Le nouveau prenom doit être une instance de str.", TypeError)],
)
def test_modifier_prenom_personne_echec(personne1_kwargs, new_prenom, expected_error, error_type):
    with pytest.raises(error_type, match=re.escape(expected_error)):
        personne_test = Personne(**personne1_kwargs)
        personne_test.modifier_prenom_personne(new_prenom)
