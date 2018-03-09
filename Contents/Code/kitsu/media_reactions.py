import requests

from .errors import *


class KitsuMediaReactions:
    def __init__(self, api, header):
        self.apiurl = api
        self.header = header
    
    def get(self, anime_id):
        """
        Get reaction data by anime id.

        :param int anime_id: ID of the anime.
        :return: Dictionary or None (for not found)
        :rtype: Dictionary or None
        :raises: :class:`errors.ServerError`
        """
        request_params = {
            'filter[anime_id]': anime_id,
            'sort': '-upVotesCount'
        }

        r = requests.get(self.apiurl + '/media-reactions', params=request_params, headers=self.header)

        if r.status_code != 200:
            if r.status_code == 404:
                return None
            else:
                raise ServerError
        
        return r.json()
    
    def get_user(self, media_reaction_id):
        """
        Get user data by media reaction id.

        :param int media_reaction_id: ID of the media reaction.
        :return: Dictionary or None (for not found)
        :rtype: Dictionary or None
        :raises: :class:`errors.ServerError`
        """
        r = requests.get(self.apiurl + "/media-reactions/{}".format(media_reaction_id) + "/user", headers=self.header)

        if r.status_code != 200:
            if r.status_code == 404:
                return None
            else:
                raise ServerError
        
        return r.json()
