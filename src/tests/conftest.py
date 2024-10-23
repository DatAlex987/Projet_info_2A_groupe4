from business_object.personne import Personne
from business_object.user import User
from business_object.son import Son
from business_object.scene import Scene
from business_object.sd import SD
from business_object.son_aleatoire import Son_Aleatoire
from business_object.son_manuel import Son_Manuel
from business_object.son_continu import Son_Continu
import pytest
from business_object.son_aleatoire import Son_Aleatoire
from business_object.son_continu import Son_Continu
from business_object.son_manuel import Son_Manuel
from business_object.user import User
from business_object.scene import Scene
import datetime


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
    }


@pytest.fixture
def son_vador_kwargs():
    return {
        "nom": "The Imperial March",
        "description": "Luke, I am your father",
        "duree": datetime.timedelta(seconds=45),
        "id_freesound": "039450",
        "tags": ["starwars", "Vador", "JW"],
    }


@pytest.fixture
def son_aleatoire1_kwargs():
    return {
        "nom": "Ambiance de forêt",
        "description": "Son de fond de forêt calme",
        "duree": datetime.timedelta(seconds=60),
        "id_freesound": "787956",
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
        "tags": ["nature", "calm", "forest"],
    }


@pytest.fixture
def son_continu2_kwargs():
    return {
        "nom": "Musique douce",
        "description": "Musique douce au piano",
        "duree": datetime.timedelta(minutes=15),
        "id_freesound": "125489",
        "tags": ["piano", "calm", "soft"],
    }


@pytest.fixture
def son_manuel1_kwargs():
    return {
        "nom": "Cloche",
        "description": "Cloche qui sonne",
        "duree": datetime.timedelta(seconds=52),
        "id_freesound": "bell_5678",
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
        "scenes": [Scene(**scene1_kwargs)],
        "date_creation": datetime.date(2024, 1, 4),
    }


"""# Substances chimiques


@pytest.fixture
def gazole_kwargs():
    return dict(nom="gazole", numero_cas="68476-34-6", numero_ce="270-676-1")


@pytest.fixture
def essence_kwargs():
    return dict(nom="essence", numero_cas="86290-81-5", numero_ce="289-220-8")


@pytest.fixture
def octane_kwargs():
    return dict(nom="octane", numero_cas="111-65-9", numero_ce="203-892-1")


@pytest.fixture
def heptane_kwargs():
    return dict(nom="heptane", numero_cas="142-82-5", numero_ce="205-563-8")


@pytest.fixture
def ethanol_kwargs():
    return dict(nom="éthanol", numero_cas="64-17-5", numero_ce="200-578-6")


@pytest.fixture
def butane_kwargs():
    return dict(nom="butane", numero_cas="106-97-8", numero_ce="203-448-7")


@pytest.fixture
def propane_kwargs():
    return dict(nom="propane", numero_cas="74-98-6", numero_ce="200-827-9")


# Carburants


@pytest.fixture
def sp98_kwargs(octane_kwargs, heptane_kwargs):
    return {
        "nom": "SP98",
        "composition_chimique": {
            SubstanceChimique(**octane_kwargs): 0.98,
            SubstanceChimique(**heptane_kwargs): 0.02,
        },
    }


@pytest.fixture
def sp95_kwargs(octane_kwargs, heptane_kwargs):
    return {
        "nom": "SP95",
        "composition_chimique": {
            SubstanceChimique(**octane_kwargs): 0.95,
            SubstanceChimique(**heptane_kwargs): 0.05,
        },
    }


@pytest.fixture
def sp95_e10_kwargs(essence_kwargs, ethanol_kwargs):
    return {
        "nom": "E85",
        "composition_chimique": {
            SubstanceChimique(**ethanol_kwargs): 0.9,
            SubstanceChimique(**essence_kwargs): 0.1,
        },
    }


@pytest.fixture
def carburant_gazole_kwargs(gazole_kwargs):
    return {"nom": "Gazole", "composition_chimique": {SubstanceChimique(**gazole_kwargs): 1.0}}


@pytest.fixture
def e85_kwargs(essence_kwargs, ethanol_kwargs):
    return {
        "nom": "E85",
        "composition_chimique": {
            SubstanceChimique(**ethanol_kwargs): 0.85,
            SubstanceChimique(**essence_kwargs): 0.15,
        },
    }


@pytest.fixture
def gpl_kwargs(butane_kwargs, propane_kwargs):
    return {
        "nom": "E85",
        "composition_chimique": {
            SubstanceChimique(**butane_kwargs): 0.8,
            SubstanceChimique(**propane_kwargs): 0.2,
        },
    }


# Pompes


@pytest.fixture
def pompe_sp98_kwargs(sp98_kwargs):
    return {
        "carburant": Carburant(**sp98_kwargs),
        "volume_maximal": 2_000,
        "volume_disponible": 0,
    }


@pytest.fixture
def pompe_sp95_kwargs(sp95_kwargs):
    return {
        "carburant": Carburant(**sp95_kwargs),
        "volume_maximal": 2_500,
        "volume_disponible": 1_000,
    }


@pytest.fixture
def pompe_gazole_kwargs(carburant_gazole_kwargs):
    return {
        "carburant": Carburant(**carburant_gazole_kwargs),
        "volume_maximal": 4_000,
        "volume_disponible": 3_200,
    }


@pytest.fixture
def pompe_e85_kwargs(e85_kwargs):
    return {"carburant": Carburant(**e85_kwargs), "volume_maximal": 1_000, "volume_disponible": 0}


# Stations


@pytest.fixture
def station_kwargs(pompe_sp98_kwargs, pompe_sp95_kwargs, pompe_gazole_kwargs, pompe_e85_kwargs):
    return {
        "pompes": {
            "SP98": Pompe(**pompe_sp98_kwargs),
            "SP95": Pompe(**pompe_sp95_kwargs),
            "Gazole": Pompe(**pompe_gazole_kwargs),
            "E85": Pompe(**pompe_e85_kwargs),
        },
        "prix": {
            "SP98": 1.839,
            "SP95": 1.739,
            "Gazole": 1.699,
            "E85": 1.199,
        },
    }


# Configuration globale


def pytest_configure():

    # Substances chimiques

    pytest.butane = SubstanceChimique(nom="butane", numero_cas="106-97-8", numero_ce="203-448-7")

    pytest.essence = SubstanceChimique(
        nom="essence", numero_cas="86290-81-5", numero_ce="289-220-8"
    )

    pytest.ethanol = SubstanceChimique(nom="éthanol", numero_cas="64-17-5", numero_ce="200-578-6")

    pytest.gazole = SubstanceChimique(nom="gazole", numero_cas="68476-34-6", numero_ce="270-676-1")

    pytest.heptane = SubstanceChimique(nom="heptane", numero_cas="142-82-5", numero_ce="205-563-8")

    pytest.octane = SubstanceChimique(nom="octane", numero_cas="111-65-9", numero_ce="203-892-1")

    pytest.propane = SubstanceChimique(nom="propane", numero_cas="74-98-6", numero_ce="200-827-9")

    # Carburants

    pytest.sp98 = Carburant(
        nom="SP98", composition_chimique={pytest.octane: 0.98, pytest.heptane: 0.02}
    )

    # Pompes

    pytest.pompe_sp98 = Pompe(
        carburant=Carburant(
            nom="SP98", composition_chimique={pytest.octane: 0.98, pytest.heptane: 0.02}
        ),
        volume_maximal=2_000,
        volume_disponible=0,
    )

    pytest.pompe_sp95 = Pompe(
        carburant=Carburant(
            nom="SP95", composition_chimique={pytest.octane: 0.95, pytest.heptane: 0.05}
        ),
        volume_maximal=2_500,
        volume_disponible=1_000,
    )

    pytest.pompe_gazole = Pompe(
        carburant=Carburant(nom="Gazole", composition_chimique={pytest.gazole: 1.0}),
        volume_maximal=4_000,
        volume_disponible=3_200,
    )

    pytest.pompe_e85 = Pompe(
        carburant=Carburant(
            nom="E85", composition_chimique={pytest.ethanol: 0.85, pytest.essence: 0.15}
        ),
        volume_maximal=1_000,
        volume_disponible=0,
    )

    pytest.pompe_gpl = Pompe(
        carburant=Carburant(
            nom="GPL", composition_chimique={pytest.butane: 0.80, pytest.propane: 0.20}
        ),
        volume_maximal=1_000,
        volume_disponible=0,
    )
"""
