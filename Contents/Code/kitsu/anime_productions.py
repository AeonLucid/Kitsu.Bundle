import requests

from .errors import *


class KitsuAnimeProductions:
    def __init__(self, api, header):
        self.apiurl = api
        self.header = header

    def get_producer(self, pid):
        """
        Get producer by producer id.

        :param int pid: ID of the producer.
        :return: Dictionary or None (for not found)
        :rtype: Dictionary or None
        :raises: :class:`errors.ServerError`
        """
        r = requests.get(self.apiurl + "/anime-productions/{}".format(pid) + "/producer", headers=self.header)

        if r.status_code != 200:
            if r.status_code == 404:
                return None
            else:
                raise ServerError
        
        return r.json()
