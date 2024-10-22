import pytest
from business_object.personne import Personne

def test_modifier_nom_personne_succe(nom_personne_kwargs):
    """Test modifier_nom with valid input (string)"""
    nom_personne_kwargs_test = 
    modifier_nom_personne("Nouveau nom")
    assert  == "Nouveau nom"


def test_modifier_nom_echec(personne):
    """Test modifier_nom with invalid input (not a string)"""
    with pytest.raises(TypeError):
       modifier_nom_personne(12345)


def test_modifier_prenom_personne_succe(prenom_personne_kwargs):
    """Test modifier_nom with valid input (string)"""
    prenom_personne_kwargsnom_personne_kwargs_test = 
    modifier_prenom_personne("Nouveau prenom")
    assert  == "Nouveau prenom"


def test_modifier_prenom_echec(personne):
    """Test modifier_prenom with invalid input (not a string)"""
    with pytest.raises(TypeError):
       modifier_prenom_personne(12345)






    

