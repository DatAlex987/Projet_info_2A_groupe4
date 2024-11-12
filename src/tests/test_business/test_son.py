from unittest.mock import MagicMock, patch
import pytest
import datetime
import pygame
import os
from business_object.son import Son


def test_Son_creation(son_vador_kwargs):
    test = Son(**son_vador_kwargs)
    assert test.nom == "The Imperial March"
    assert test.description == "Luke, I am your father"
    assert test.duree == datetime.timedelta(seconds=45)
    assert test.id_freesound == "039450"
    assert test.tags == ["starwars", "Vador", "JW"]

@patch('pygame.mixer.Sound')
def test_jouer_son(mock_sound):
    mock_instance = mock_sound.return_value
    son = Son(id_freesound=123456)
    son.JouerSon()
    
    # Vérifier que le son est joué
    mock_instance.play.assert_called_once()

@patch('pygame.mixer.Sound')
def test_arret_son(mock_sound):
    mock_instance = mock_sound.return_value
    son = SONSound(id_freesound=123456)
    son.JouerSon()
    son.ArreterSon()
    
    # Vérifier que le son est arrêté
    mock_instance.stop.assert_called_once()
    pygame.mixer.quit()

"""
def test_JouerSon(setup_pygame, mocker):
    """Test de la méthode JouerSon pour un chargement réussi."""
    mock_sound = MagicMock()
    mocker.patch("pygame.mixer.Sound", return_value=mock_sound)

    son = Son(
        nom="BlOB",
        description="Blob blob blob",
        duree=datetime.timedelta(seconds=10),
        id_freesound="test_sound",
        tags=["test"],
    )

    # Simuler la variable d'environnement
    with patch.dict(os.environ, {"DOSSIER_SAUVEGARDE": os.path.normpath("/mock/path")}):
        son.JouerSon()

    # Vérifier que Sound a été appelé avec le bon chemin
    expected_path = os.path.normpath("/mock/path/test_sound.mp3")
    pygame.mixer.Sound.assert_called_once_with(expected_path)
    mock_sound.play.assert_called_once_with(loop=0)


def test_JouerSon_file_not_found(setup_pygame, mocker):
    """Test de la méthode JouerSon pour un fichier non trouvé."""
    mocker.patch("pygame.mixer.Sound", side_effect=FileNotFoundError)

    son = Son(
        nom="BLOB",
        description="blob blob blob",
        duree=datetime.timedelta(seconds=10),
        id_freesound="test_sound",
        tags=["test"],
    )

    with patch.dict(os.environ, {"DOSSIER_SAUVEGARDE": os.path.normpath("C:/mock/path")}):
        fichier_son = os.path.normpath(
            os.path.join(os.getenv("DOSSIER_SAUVEGARDE"), "test_sound.mp3")
        )
        with pytest.raises(
            FileNotFoundError,
            match=rf"Le fichier son {fichier_son} n'a pas été trouvé.",
        ):
            son.JouerSon()
"""
"""
def test_ArretSon(setup_pygame, mocker):
    """Test de la méthode Arret_Son."""
    mock_sound = MagicMock()
    mocker.patch("pygame.mixer.Sound", return_value=mock_sound)

    son = Son(
        nom="Blob",
        description="blob blob blob",
        duree=datetime.timedelta(seconds=10),
        id_freesound="test_sound",
        tags=["test"],
    )

    with patch.dict(os.environ, {"DOSSIER_SAUVEGARDE": os.path.normpath("/mock/path")}):
        son.JouerSon()

    assert son.charge is not None

    son.Arret_Son()
    mock_sound.stop.assert_called_once()
    assert son.charge is None
"""
