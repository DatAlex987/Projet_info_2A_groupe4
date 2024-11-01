from unittest.mock import MagicMock, patch
import pytest
from business_object.son import Son
from business_object.son_continu import Son_Continu


@patch("pygame.mixer.Sound")
@patch.object(Son, "JouerSon")  # Mock de la méthode JouerSon dans la classe Son
def test_jouer_son_en_boucle(mock_jouer_son, mock_sound_class, son_continu1_kwargs):
    # Créer un mock pour l'objet Sound
    mock_sound = MagicMock()
    mock_sound_class.return_value = mock_sound  # retourne le mock pour Sound

    # Créer une instance de Son_Continu
    son_instance = Son_Continu(**son_continu1_kwargs)

    # Appeler la méthode jouer_son_en_boucle
    son_instance.jouer_son_en_boucle()

    # Vérifier que JouerSon a été appelée une fois
    mock_jouer_son.assert_called_once()

    # Vérifier que le son est configuré pour jouer en boucle avec loops=-1
    mock_sound.play.assert_called_once_with(loops=-1)
