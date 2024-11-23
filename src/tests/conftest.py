import datetime
import pytest

####
from business_object.son_aleatoire import Son_Aleatoire
from business_object.son_manuel import Son_Manuel
from business_object.son_continu import Son_Continu


@pytest.fixture
def personne1_kwargs():
    return {"nom": "Doe", "prenom": "John", "date_naissance": datetime.date(1990, 1, 1)}


@pytest.fixture
def personne2_kwargs():
    return {"nom": "TheRipper", "prenom": "Jack", "date_naissance": datetime.date(1962, 3, 5)}


@pytest.fixture
def user1_kwargs():
    """Mock data for User class."""
    return {
        "nom": "Doe",
        "prenom": "Jane",
        "date_naissance": datetime.date(1995, 5, 5),
        "id_user": "jdoe",
        "mdp": "Password!123",
        "SD_possedes": [],
        "pseudo": "JaneDoe01",
    }


@pytest.fixture
def utilisateur_kwargs():
    """Mock data for User class."""
    return {
        "nom": "Bocquet",
        "prenom": "Noémie",
        "date_naissance": datetime.date(2003, 8, 8),
        "id_user": "noemie.b",
        "mdp": "Mdpexample@1",
        "SD_possedes": [],
        "pseudo": "noemie.bocquet",
    }


@pytest.fixture
def utilisateur2_kwargs():
    """Mock data for User class."""
    return {
        "nom": "Bocquet",
        "prenom": "Noémie",
        "date_naissance": datetime.date(2003, 8, 8),
        "id_user": "123",
        "mdp": "Mdpexample@1",
        "SD_possedes": ["My Sounddeck"],
        "pseudo": "noemie.bocquet",
    }


@pytest.fixture
def son_vador_kwargs():
    return {
        "nom": "The Imperial March",
        "description": "Luke, I am your father",
        "duree": datetime.timedelta(seconds=45),
        "id_freesound": "039450",
        "id_son": "XkOfuYc8",
        "tags": ["starwars", "Vador", "JW"],
    }


@pytest.fixture
def son_aleatoire1_kwargs():
    return {
        "nom": "Ambiance de forêt",
        "description": "Son de fond de forêt calme",
        "duree": datetime.timedelta(seconds=60),
        "id_freesound": "787956",
        "id_son": "XkOoDuc8",
        "tags": ["nature", "calm", "forest"],
        "cooldown_min": 5,
        "cooldown_max": 10,
    }


@pytest.fixture
def son_aleatoire2_kwargs():
    return {
        "nom": "Manoir hanté",
        "description": "Son de fantome dans un manoir",
        "duree": datetime.timedelta(seconds=30),
        "id_freesound": "445936",
        "id_son": "pmUjYtf7",
        "tags": ["manoir", "fantome", "scary"],
        "cooldown_min": 3,
        "cooldown_max": 15,
    }


@pytest.fixture
def son_continu1_kwargs():
    return {
        "nom": "Ambiance de forêt",
        "description": "Son de fond de forêt calme",
        "duree": datetime.timedelta(seconds=46),
        "id_freesound": "forest_1234",
        "id_son": "p8Mu4HyE",
        "tags": ["nature", "calm", "forest"],
    }


@pytest.fixture
def son_continu2_kwargs():
    return {
        "nom": "Musique douce",
        "description": "Musique douce au piano",
        "duree": datetime.timedelta(minutes=15),
        "id_freesound": "125489",
        "id_son": "e6uKHU85",
        "tags": ["piano", "calm", "soft"],
    }


@pytest.fixture
def son_manuel1_kwargs():
    return {
        "nom": "Cloche",
        "description": "Cloche qui sonne",
        "duree": datetime.timedelta(seconds=52),
        "id_freesound": "bell_5678",
        "id_son": "p7E5d9Z5",
        "tags": ["bell", "chime"],
        "start_key": "c",
    }


@pytest.fixture
def son_manuel2_kwargs():
    return {
        "nom": "Bruits de pas",
        "description": "Bruits de pas qui s'approchent",
        "duree": datetime.timedelta(seconds=59),
        "id_freesound": "458726",
        "id_son": "8cDmPouX",
        "tags": ["step", "approaching"],
        "start_key": "p",
    }


@pytest.fixture
def scene1_kwargs(user1_kwargs, son_aleatoire1_kwargs, son_continu1_kwargs, son_manuel1_kwargs):
    return {
        "nom": "Forêt Mystique",
        "description": "Une scène calme dans une forêt mystérieuse",
        "id_scene": "987654",
        "sons_aleatoires": [Son_Aleatoire(**son_aleatoire1_kwargs)],
        "sons_manuels": [Son_Manuel(**son_manuel1_kwargs)],
        "sons_continus": [Son_Continu(**son_continu1_kwargs)],
        "date_creation": datetime.date(2024, 1, 1),
    }


@pytest.fixture
def scene2_kwargs(user1_kwargs, son_aleatoire2_kwargs, son_continu2_kwargs, son_manuel2_kwargs):
    return {
        "nom": "Forêt Mystique",
        "description": "Une scène calme dans une forêt mystérieuse",
        "id_scene": "234567",
        "sons_aleatoires": [Son_Aleatoire(**son_aleatoire2_kwargs)],
        "sons_manuels": [Son_Manuel(**son_manuel2_kwargs)],
        "sons_continus": [Son_Continu(**son_continu2_kwargs)],
        "date_creation": datetime.date(2023, 10, 9),
    }


@pytest.fixture
def sd_kwargs(scene1_kwargs):
    """Mock data for SD class."""
    return {
        "nom": "Aventure Mystique",
        "description": "Un sound-deck pour une aventure calme",
        "id_sd": "1",
        "scenes": [],
        "date_creation": datetime.date(2024, 1, 4),
        "id_createur": "jdoe",  # id de user1_kwargs
    }
