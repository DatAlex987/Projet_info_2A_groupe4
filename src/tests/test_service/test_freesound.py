from unittest.mock import patch
import pytest
import re

####
from service.freesound import Freesound


# 1/
def test_rechercher_par_id_success():
    with patch("requests.get") as mock_get:
        # Mocking a fake response
        mock_response = {
            "id": "420320",
            "name": "sound_example",
            "tags": ["wind"],
            "licence": "Creative Commons",
            "username": "user1",
        }
        mock_get.return_value.json.return_value = mock_response

        # Test function
        result = Freesound.rechercher_par_id("420320")
        assert result["id"] == "420320"
        assert result["name"] == "sound_example"
        assert result["username"] == "user1"


# 2/ Test : ajoute une condition pour gérer les cas où l'ID n'existe pas, puis renvoie le message
# pour prévenir l'utilisateur
def test_rechercher_par_id_not_found():
    with patch("requests.get") as mock_get:
        # Simuler une réponse où l'ID n'existe pas (réponse vide de l'API)
        mock_get.return_value.json.return_value = {}

        result = Freesound.rechercher_par_id("123456")  # Utiliser un ID valide de 6 chiffres
        assert result == "Aucun son ne porte cet identifiant"  # Vérification du message attendu
