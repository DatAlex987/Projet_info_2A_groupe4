from typing import Optional, Dict, Any, Union
import os
from dotenv import load_dotenv
import requests
from utils.singleton import Singleton
import re


class Freesound(metaclass=Singleton):
    """
    Classe intéragissant avec l'API Freesound
    """

    def rechercher_par_tag(tag: str, limit: int):
        """
        Envoie une requête à l'API pour récupérer des sons correspondants
        au tag renseigné.

        Param
        -----------------
        tag : str
            Mot clé pour orienter la recherche
        limit : int
            Nombre de sons à renvoyer

        Returns
        -----------------
        results : list
            Liste de longueur l = limit. Chaque élément est un
            dictionnaire qui contient les informations
            d'un son : id, nom, tags, licence, username
        """
        if not isinstance(tag, str):
            raise TypeError("L'argument tag n'est pas un str.")
        if not isinstance(limit, int):
            raise TypeError("L'argument limit n'est pas un int.")
        if limit < 0:
            raise ValueError("L'argument limit ne peut pas être négatif.")

        # mettre cette partie ci-dessous en paramètres init car c'est c
        load_dotenv()
        URL: Optional[str] = os.getenv("URL_API")
        KEY: Optional[str] = os.getenv("API_KEY")
        headers = {
            "Content-type": "application/json",
        }
        payload: Dict[str, Union[str, int]] = {"token": f"{KEY}"}
        url_search = f"{URL}search/text/"
        payload_search = payload.copy()
        payload_search.update({"query": tag, "page_size": limit})
        req = requests.get(url_search, headers=headers, params=payload_search)
        results = req.json()
        # La sortie est une liste de dico des 10 sons liés au
        # wind (id, name, tags, licence, username)
        return results["results"]  # [:limit]

    def rechercher_multi_filtres(
        dico_filtres: dict, limit: int
    ) -> list[dict[str, Union[str, int]]]:
        """
        Envoie une requête à l'API pour récupérer des sons correspondant
        aux filtres renseignés.

        Paramètres
        -----------------
        dico_filtres : dict
            Dictionnaire contenant les filtres à appliquer :
            - "query": (str) la recherche principale.
            - "min_duration": (float) durée minimale des sons.
            - "max_duration": (float) durée maximale des sons.

        limit : int
            Nombre maximum de résultats souhaités.

        Returns
        -----------------
        results : list
            Liste contenant des dictionnaires pour chaque son trouvé.
            Chaque dictionnaire contient des informations succintes sur un son.
        """
        if not isinstance(dico_filtres, dict):
            raise TypeError("L'argument dico_filtres n'est pas un dict.")
        if not isinstance(limit, int):
            raise TypeError("L'argument limit n'est pas un int.")
        if limit < 0:
            raise ValueError("L'argument limit ne peut pas être négatif.")

        load_dotenv()
        URL: Optional[str] = os.getenv("URL_API")
        KEY: Optional[str] = os.getenv("API_KEY")
        if not URL or not KEY:
            raise ValueError(
                "L'URL de l'API ou la clé API n'est pas définie dans les variables d'environnement."
            )

        headers = {
            "Content-type": "application/json",
        }

        # Construire le paramètre `filter` pour inclure les durées uniquement si elles sont valides
        filters = []
        if dico_filtres.get("min_duration") is not None:
            filters.append(f"duration:[{dico_filtres['min_duration']} TO *]")
        if dico_filtres.get("max_duration") is not None:
            filters.append(f"duration:[* TO {dico_filtres['max_duration']}]")

        # Fusionner les filtres en une chaîne unique
        filter_str = " ".join(filters) if filters else None

        # Préparer la requête
        payload_search: Dict[str, Union[str, int]] = {
            "token": KEY,
            "query": dico_filtres.get("query", ""),  # Utilise une chaîne vide par défaut
            "limit": limit,
        }
        if filter_str:
            payload_search["filter"] = filter_str

        # Faire la requête
        try:
            req = requests.get(f"{URL}search/text/", headers=headers, params=payload_search)
            req.raise_for_status()  # Lève une exception si le code HTTP indique une erreur
        except requests.RequestException as e:
            raise RuntimeError(f"Erreur lors de la requête à l'API : {e}")

        # Convertir la réponse en JSON
        response_json = req.json()
        if "results" not in response_json:
            raise ValueError("La réponse de l'API ne contient pas de champ 'results'.")

        # Extraire les données pertinentes
        results = [
            {
                "id": sound["id"],
                "name": sound["name"],
                "tags": sound.get("tags", []),
                "license": sound.get("license", "Unknown"),
                "username": sound.get("username", "Unknown"),
            }
            for sound in response_json["results"][:limit]
        ]

        return results

    def rechercher_par_id(id: str):
        """
        Envoie une requête à l'API pour récupérer les informations d'un son
        spécifique via son id.
        Param
        -----------------
        id : str
            Identifiant unique du son à rechercher (une suite de 6 chiffres).

        Returns
        -----------------
        result : dict | str
            Dictionnaire contenant les informations du son,
            ou un message d'erreur si l'ID n'existe pas ou est mal formé.
        """
        if not isinstance(id, str):
            raise TypeError("L'argument id n'est pas un str.")
        load_dotenv()
        URL: Optional[str] = os.getenv("URL_API")
        KEY: Optional[str] = os.getenv("API_KEY")
        headers = {
            "Content-type": "application/json",
        }
        payload: Dict[str, Union[str, int]] = {"token": f"{KEY}"}

        # Construire l'URL pour rechercher par ID
        url_search = f"{URL}sounds/{id}/"

        # Effectuer la requête
        req = requests.get(url_search, headers=headers, params=payload)

        # Vérifier la validité de la réponse JSON
        try:
            result = req.json()
            # Vérifier si le résultat est vide ou invalide
            if "id" not in result:
                return "Aucun son ne porte cet identifiant"
        except requests.exceptions.JSONDecodeError as e:
            print("Erreur de décodage JSON :", e)
            return {}

        return result

    # print(Freesound.rechercher_par_id(id="420320"))

    # a developper : on aurait aimé faire une recherche
    # par duree mais avec l'api on est limité à 3 requetes par seconde max

    # print(Freesound.rechercher_par_tag(tag="wind", limit=5))

    def rechercher_ids_par_tag(tag: str, limit: int):
        """
        Envoie une requête à l'API pour récupérer uniquement les IDs des sons
        correspondants au tag renseigné.

        Param
        -----------------
        tag : str
            Mot clé pour orienter la recherche
        limit : int
            Nombre maximum de sons à renvoyer

        Returns
        -----------------
        ids : list
            Liste d'IDs des sons correspondant au tag, longueur l = limit
        """
        if not isinstance(tag, str):
            raise TypeError("L'argument tag n'est pas un str.")
        if not isinstance(limit, int):
            raise TypeError("L'argument limit n'est pas un int.")
        if limit < 0:
            raise ValueError("L'argument limit ne peut pas être négatif.")

        load_dotenv()
        URL: Optional[str] = os.getenv("URL_API")
        KEY: Optional[str] = os.getenv("API_KEY")
        headers = {
            "Content-type": "application/json",
        }
        payload: Dict[str, Union[str, int]] = {"token": f"{KEY}"}
        url_search = f"{URL}search/text/"
        payload_search = payload.copy()
        payload_search.update({"query": tag})

        # Effectuer la requête
        req = requests.get(url_search, headers=headers, params=payload_search)

        # Vérifier la validité de la réponse JSON
        try:
            results = req.json()
        except requests.exceptions.JSONDecodeError as e:
            print("Erreur de décodage JSON :", e)
            return []

        # Récupérer uniquement les IDs des résultats
        ids = [result["id"] for result in results.get("results", [])]

        # Limiter le nombre d'IDs renvoyés à la valeur de `limit`
        return ids[:limit]

    def telecharger_son(self, id_freesound):
        # Modifier la méthode pour prendre en compte les autres formats.
        # Renommer les sons téléchargés au format précisé dans jouer_son (son.py)
        sound_data = Freesound.rechercher_par_id(id_freesound)
        mp3_url = sound_data["previews"]["preview-hq-mp3"]  # Lien du fichier MP3 haute qualité

        # Télécharger le fichier MP3
        print(f"Téléchargement du son à partir de {mp3_url}")
        mp3_response = requests.get(mp3_url)
        if mp3_response.status_code == 200:
            # Chemin complet vers le fichier dans le dossier Fichiers_audio
            dossier_sauvegarde: str = os.getenv("DOSSIER_SAUVEGARDE")
            chemin_fichier_mp3 = os.path.join(dossier_sauvegarde, f"{id_freesound}.mp3")
            with open(chemin_fichier_mp3, "wb") as f:
                f.write(mp3_response.content)
            print(f"Le fichier a été téléchargé sous le nom {chemin_fichier_mp3}")
        else:
            print(f"Erreur lors du téléchargement du fichier : {mp3_response.status_code}")


"""def rechercher_multi_filtres(dico_filtres: dict, limit: int):  # NOT DONE YET
    "
    Envoie une requête à l'API pour récupérer des sons correspondants
    aux filtres renseignés.

    Param
    -----------------
    dico_filtres : dict
        Dictionnaire dont les clés sont les types de filtres et les valeurs
        les filtres souhaités (None si filtre non utilisé)

    Returns
    -----------------
    results : list
        Liste de longueur l = limit. Chaque élément est un
        dictionnaire qui contient les informations
        d'un son : id, nom, tags, licence, username
    "
    if not isinstance(dico_filtres, dict):
        raise TypeError("L'argument dico_filtres n'est pas un dict.")
    if not isinstance(limit, int):
        raise TypeError("L'argument limit n'est pas un int.")
    if limit < 0:
        raise ValueError("L'argument limit ne peut pas être négatif.")

    load_dotenv()
    URL: Optional[str] = os.getenv("URL_API")
    KEY: Optional[str] = os.getenv("API_KEY")
    headers = {
        "Content-type": "application/json",
    }
    payload: Dict[str, Union[str, int]] = {"token": f"{KEY}"}
    url_search = f"{URL}search/text/"
    payload_search = payload.copy()
    payload_search.update({"query": dict, "limit": limit})
    req = requests.get(url_search, headers=headers, params=payload_search)
    results = req.json()
    # La sortie est une liste de dico des 10 sons liés au
    # wind (id, name, tags, licence, username)
    return results["results"]"""
