from .anime import *
from .anime_productions import *
from .anime_characters import *
from .media_reactions import *


class KitsuClient:
    """
    :type anime: KitsuAnime
    :type anime_productions: KitsuAnimeProductions
    """
    def __init__(self):
        """
        Initialize a new Kitsu API instance.
        """
        api = "https://kitsu.io/api/edge"
        header = {
            'User-Agent': 'Kitsu PlexAgent',
            'Accept': 'application/vnd.api+json',
            'Content-Type': 'application/vnd.api+json'
        }
        
        self.anime = KitsuAnime(api, header)
        self.anime_productions = KitsuAnimeProductions(api, header)
        self.anime_characters = KitsuAnimeCharacters(api, header)
        self.media_reactions = KitsuMediaReactions(api, header)
