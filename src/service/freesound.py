# -*- coding: utf-8 -*-


from typing import Optional, Dict, Any, Union
import os
from dotenv import load_dotenv
import requests
from service.singleton import Singleton


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

        load_dotenv()
        URL: Optional[str] = os.getenv("URL_API")
        KEY: Optional[str] = os.getenv("API_KEY")
        headers = {
            "Content-type": "application/json",
        }
        payload: Dict[str, Union[str, int]] = {"token": f"{KEY}"}
        url_search = f"{URL}search/text/"
        payload_search = payload.copy()
        payload_search.update({"query": tag, "limit": limit})
        req = requests.get(url_search, headers=headers, params=payload_search)
        results = req.json()
        # La sortie est une liste de dico des 10 sons liés au
        # wind (id, name, tags, licence, username)
        return results["results"]

    def rechercher_par_nom():
        pass

    def rechercher_par_duree():
        pass

    def rechercher_par_id():
        pass

    def rechercher_multi_filtres(dico_filtres: dict, limit: int):  # NOT DONE YET
        """
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
        headers = {
            "Content-type": "application/json",
        }
        payload: Dict[str, Union[str, int]] = {"token": f"{KEY}"}
        url_search = f"{URL}search/text/"
        payload_search = payload.copy()
        payload_search.update({"query": tag, "limit": limit})
        req = requests.get(url_search, headers=headers, params=payload_search)
        results = req.json()
        # La sortie est une liste de dico des 10 sons liés au
        # wind (id, name, tags, licence, username)
        return results["results"]


print(Freesound.rechercher_par_tag("wind", limit=10))
