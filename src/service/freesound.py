# -*- coding: utf-8 -*-

# For housekeeping
from typing import Optional, Dict, Any, Union
import os
from dotenv import load_dotenv

# For business code
import requests

# Loading env var (api key secret, url...)
load_dotenv()
URL: Optional[str] = os.getenv("URL_API")
KEY: Optional[str] = os.getenv("API_KEY")


# Defining the constant headers
headers = {
    "Content-type": "application/json",
}
payload: Dict[str, Union[str, int]] = {"token": f"{KEY}"}


def request_search(query_term: str) -> Dict:
    url_search = f"{URL}search/text/"
    payload_search = payload.copy()
    payload_search.update({"query": query_term, "limit": 10})
    req = requests.get(url_search, headers=headers, params=payload_search)
    results = req.json()
    return results["results"]


print(request_search("wind"))
# La sortie est une liste de dico des 10 sons liés au wind (id, name, tags, licence, username)
