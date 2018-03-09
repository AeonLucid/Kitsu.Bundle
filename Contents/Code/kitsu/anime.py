import requests

from .errors import *


class KitsuAnime:
    def __init__(self, api, header):
        self.apiurl = api
        self.header = header

    def search(self, term, year=None):
        """
        Search for anime by term.

        :param str term: What to search for.
        :return: The results as a SearchWrapper iterator.
        :rtype: SearchWrapper
        """
        request_params = {
            "filter[text]": term
        }

        if year is not None:
            request_params["filter[year]"] = year

        r = requests.get(self.apiurl + "/anime", params=request_params, headers=self.header)
        
        if r.status_code != 200:
            raise ServerError
        
        jsd = r.json()

        if jsd['meta']['count'] == 0:
            return None
        
        return jsd

    def get(self, aid):
        """
        Get anime information by id.

        :param int aid: ID of the anime.
        :return: Dictionary or None (for not found)
        :rtype: Dictionary or None
        :raises: :class:`errors.ServerError`
        """
        r = requests.get(self.apiurl + "/anime/{}".format(aid), headers=self.header)

        if r.status_code != 200:
            if r.status_code == 404:
                return None
            else:
                raise ServerError
        
        return r.json()

    def get_genres(self, aid):
        """
        Get genres by anime id.

        :param int aid: ID of the anime.
        :return: Dictionary or None (for not found)
        :rtype: Dictionary or None
        :raises: :class:`errors.ServerError`
        """
        r = requests.get(self.apiurl + "/anime/{}".format(aid) + "/genres", headers=self.header)

        if r.status_code != 200:
            if r.status_code == 404:
                return None
            else:
                raise ServerError
        
        return r.json()

    def get_productions(self, aid):
        """
        Get production data by anime id.

        :param int aid: ID of the anime.
        :return: Dictionary or None (for not found)
        :rtype: Dictionary or None
        :raises: :class:`errors.ServerError`
        """
        r = requests.get(self.apiurl + "/anime/{}".format(aid) + "/anime-productions", headers=self.header)

        if r.status_code != 200:
            if r.status_code == 404:
                return None
            else:
                raise ServerError
        
        return r.json()

    def get_characters(self, anime_id):
        """
        Get character data by anime id.

        :param int anime_id: ID of the anime.
        :return: Dictionary or None (for not found)
        :rtype: Dictionary or None
        :raises: :class:`errors.ServerError`
        """

        # Sort because we want main roles as first.
        r = requests.get(self.apiurl + "/anime/{}".format(anime_id) + "/anime-characters?sort=role", headers=self.header)

        if r.status_code != 200:
            if r.status_code == 404:
                return None
            else:
                raise ServerError
        
        return r.json()
