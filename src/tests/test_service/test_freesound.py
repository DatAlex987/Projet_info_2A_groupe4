from unittest.mock import patch
import pytest
import re

####
from service.freesound import Freesound


"""@pytest.mark.parametrize(
    "tag, limit, expected_error, error_type",
    [
        (["wind"], 15, "L'argument tag n'est pas un str.", TypeError),
        ("wind", -4, "L'argument limit ne peut pas être négatif.", ValueError),
        ("wind", "15", "L'argument limit n'est pas un int.", TypeError),
    ],
)
# 1/ tests de recherche_par_tag : types incorrectes
def test_rechercher_par_tag_echec(tag, limit, expected_error, error_type):
    with pytest.raises(error_type, match=re.escape(expected_error)):
        Freesound.rechercher_par_tag(tag, limit)
"""


# 2/ pareil que 1/ mais avec mock
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


"""# 3/ tests de recherche_par_tag : vérifier que la recherche fonctionne
def test_rechercher_par_tag_success():
    with patch("requests.get") as mock_get:
        # Mocking a fake response
        mock_response = {
            "results": [
                {
                    "id": 1,
                    "name": "sound1",
                    "tags": ["wind"],
                    "licence": "Creative Commons",
                    "username": "user1",
                },
                {
                    "id": 2,
                    "name": "sound2",
                    "tags": ["wind"],
                    "licence": "Creative Commons",
                    "username": "user2",
                },
            ]
        }
        mock_get.return_value.json.return_value = mock_response

        # Test function
        result = Freesound.rechercher_par_tag("wind", 2)
        assert len(result) == 2
        assert result[0]["name"] == "sound1"
        assert result[1]["name"] == "sound2"


# 5/ Ce test vérifie que la méthode renvoie correctement les résultats lorsque le nombre de sons
# est inférieur à la limite demandée.
def test_rechercher_par_tag_limit_greater_than_results():
    with patch("requests.get") as mock_get:
        mock_response = {
            "results": [
                {
                    "id": 1,
                    "name": "sound1",
                    "tags": ["wind"],
                    "licence": "Creative Commons",
                    "username": "user1",
                }
            ]
        }
        mock_get.return_value.json.return_value = mock_response

        result = Freesound.rechercher_par_tag("wind", 5)
        assert len(result) == 1  # Seulement 1 son, même si la limite est 5


# 6/ Ce test vérifie comment la fonction gère le cas où aucun son n'est trouvé pour le tag donné.
def test_rechercher_par_tag_no_results():
    with patch("requests.get") as mock_get:
        # Mocking an empty result
        mock_response = {"results": []}
        mock_get.return_value.json.return_value = mock_response

        result = Freesound.rechercher_par_tag("nonexistent_tag", 5)
        assert result == []  # Pas de résultat"""


# 9/ Test : ajoute une condition pour gérer les cas où l'ID n'existe pas, puis renvoie le message
# pour prévenir l'utilisateur
def test_rechercher_par_id_not_found():
    with patch("requests.get") as mock_get:
        # Simuler une réponse où l'ID n'existe pas (réponse vide de l'API)
        mock_get.return_value.json.return_value = {}

        result = Freesound.rechercher_par_id("123456")  # Utiliser un ID valide de 6 chiffres
        assert result == "Aucun son ne porte cet identifiant"  # Vérification du message attendu
