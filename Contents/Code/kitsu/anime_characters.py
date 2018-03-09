import requests

from .errors import *


class KitsuAnimeCharacters:
    def __init__(self, api, header):
        self.apiurl = api
        self.header = header

    def get(self, anime_character_id):
        """
        Get character by anime character id.

        :param int anime_character_id: ID of the character.
        :return: Dictionary or None (for not found)
        :rtype: Dictionary or None
        :raises: :class:`errors.ServerError`
        """
        r = requests.get(self.apiurl + "/anime-characters/{}".format(anime_character_id) + "/character", headers=self.header)

        if r.status_code != 200:
            if r.status_code == 404:
                return None
            else:
                raise ServerError
        
        return r.json()
