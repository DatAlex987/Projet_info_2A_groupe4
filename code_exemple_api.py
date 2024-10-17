# -*- coding: utf-8 -*-

# For housekeeping
from typing import Optional, Dict, Any, Union
import os
from dotenv import load_dotenv

# For business code
import requests
import wget

# Loading env var (api key secret, url...)
load_dotenv()
URL: Optional[str] = os.getenv("URL_API")
KEY: Optional[str] = os.getenv("API_KEY")


# Defining the constant headers
headers = {
    "Content-type": "application/json",
}
payload: Dict[str, Union[str, int]] = {"token": f"{KEY}"}


def run_func(func, file_scret):
    key = file_secret.read()
    func(key)
    del key


def request_search(query_term: str) -> Dict:
    url_search = f"{URL}search/text/"
    payload_search = payload.copy()
    payload_search.update({"query": query_term, "limit": 10})
    req = requests.get(url_search, headers=headers, params=payload_search)
    results = req.json()
    return results["results"]


def request_download_url_by_id(id_to_find: str) -> str:
    url_sound = f"{URL}sounds/{id_to_find}"
    req = requests.get(url_sound, headers=headers, params=payload)
    results = req.json()
    print(results)
    return results["previews"]["preview-hq-mp3"]


def download_by_url(url_of_file_to_download: str, path_where_to_download) -> None:
    filename = wget.download(url_of_file_to_download, out=path_where_to_download)
    print(filename)


if __name__ == "__main__":
    # define the search term
    search_term = "forest"

    # define where we will store the resulting mp3 file
    full_path = os.path.realpath(__file__)  # path of the current file, absolute
    path_folder = os.path.dirname(full_path)  # folder of the current file, absolute
    path_stored_music = os.path.join(path_folder, "stored_music/")
    path_downloaded_file = os.path.join(
        path_stored_music, f"{search_term}.mp3"
    )  # this is stupid and basic
    print(path_downloaded_file)

    # make the request for a list of sounds based on a query
    res = request_search(search_term)
    # print(res)

    # take first result (sorted by Freesound score) and get its preview url
    first_res = res[0]
    download_link = request_download_url_by_id(first_res["id"])
    print(download_link)

    # download the mp3 preview
    download_by_url(download_link, path_downloaded_file)
