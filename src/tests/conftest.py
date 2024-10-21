from business_object.personne import Personne
from business_object.son import Son
from business_object.scene import Scene
from business_object.sd import SD
import pytest


# Substances chimiques


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
