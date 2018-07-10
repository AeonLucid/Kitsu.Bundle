import re
import requests
from kitsu import KitsuClient
from datetime import datetime

AGENT_NAME = 'Kitsu'
AGENT_LANGUAGES = [Locale.Language.English]
AGENT_PRIMARY_PROVIDER = True
AGENT_CONTRIBUTES_TO = [
    'com.plexapp.agents.thetvdb',
	'com.plexapp.agents.themoviedb'
]

kitsu = KitsuClient()

def Start():
    Log.Info("[" + AGENT_NAME + "] Starting Kitsu Agent")
    HTTP.CacheTime = CACHE_1WEEK
	
def ValidatePrefs():
    Log.Info('[' + AGENT_NAME + '] There is nothing to validate')

def cleanText(text):
    ''' Returns the string without non ASCII characters'''
    return re.sub(r'[^\x00-\x7F]+',' ', text)

def matchAnime(results, media, search_type):
    search_name = cleanText(media.show if search_type == 'tv' else media.name)
    search_year = media.year

    Log.Info('[' + AGENT_NAME + '] Searching for "' + search_name + ' (' + str(search_year) + ')"')

    search_results = kitsu.anime.search(search_name, search_year)

    for i, anime in enumerate(search_results['data']):
        match_score = 0
        anime_id = anime['id']
        anime_title = anime['attributes']['canonicalTitle']
        anime_titles = anime['attributes']['titles']
        anime_year = anime['attributes']['startDate'].split('-')[0]

        if 'en' in anime_titles and anime_titles['en'] is not None:
            anime_title = anime_titles['en']
        elif 'en_jp' in anime_titles and anime_titles['en_jp'] is not None:
            anime_title = anime_titles['en_jp']

        for title_key, title in anime_titles.iteritems():
            if title is not None:
                title_score = int(100 - abs(String.LevenshteinDistance(cleanText(title), search_name)))
                if title_score > match_score:
                    match_score = title_score

        # Substract points for later results from Kitsu
        match_score = match_score - i * 5

        results.Append(MetadataSearchResult(id = anime_id, name = anime_title, year = anime_year, score = match_score, lang = Locale.Language.English))

    Log.Info('[' + AGENT_NAME + '] Found ' + str(len(results)) + ' results for "' + search_name + ' (' + str(search_year) + ')"')

# Apply data of an anime object from kitsu to a metadata object.
# Can be a movie or tvshow.
def applyAnime(metadata, anime):
    if Prefs['apply_genres']:
        anime_genres = []
        search_genres = kitsu.anime.get_genres(metadata.id)
        if search_genres is not None:
            for genre_data in search_genres['data']:
                anime_genres.append(genre_data['attributes']['name'])

        metadata.genres = anime_genres

    if Prefs['apply_studio']
        anime_studio = None
        search_productions = kitsu.anime.get_productions(metadata.id)
        if search_productions is not None:
            for production_data in search_productions['data']:
                if production_data['attributes']['role'] == 'studio':
                    producer = kitsu.anime_productions.get_producer(production_data['id'])
                    if producer is not None:
                        anime_studio = producer['data']['attributes']['name']
        
        metadata.studio = anime_studio
    
    if Prefs['apply_summary']:
        summary_append = ''
        search_reactions = kitsu.media_reactions.get(metadata.id)
        if search_reactions is not None and search_reactions['data'][0] is not None:
            reaction = search_reactions['data'][0]
            user = kitsu.media_reactions.get_user(reaction['id'])
            summary_append = '\nReaction by Kitsu user {0} with {1} upvotes: "{2}".'.format(
                user['data']['attributes']['name'],
                reaction['attributes']['upVotesCount'],
                reaction['attributes']['reaction'])
        
        metadata.summary = anime['synopsis'] + summary_append
    
    if Prefs['apply_roles']:
        cast_members = []
        search_cast = kitsu.anime.get_characters(metadata.id)
        if search_cast is not None:
            # TODO: All cast members.
            for character in search_cast['data']:
                search_character = kitsu.anime_characters.get(character['id'])
                cast_members.append({
                    'name': search_character['data']['attributes']['canonicalName'],
                    'role': character['attributes']['role'].capitalize(),
                    'photo': search_character['data']['attributes']['image']['original']
                })
        
        metadata.roles.clear()
        if cast_members:
            for cast_member in cast_members:
                role = metadata.roles.new()
                role.name = cast_member['name']
                role.role = cast_member['name']
                role.photo = cast_member['photo']

    # metadata.tags = ?

    # metadata.collections = ?

    if Prefs['apply_duration']:
        metadata.duration = (int(anime['episodeLength']) * 60 * 1000) if anime['episodeLength'] is not None else None
    
    if Prefs['apply_rating']:
        metadata.rating = float(anime['averageRating']) / 10

    if Prefs['apply_title']:
        metadata.title = anime['canonicalTitle']

    if Prefs['apply_originally_available_at']:
        metadata.originally_available_at = datetime.strptime(str(anime['startDate']), '%Y-%m-%d')
    
    if Prefs['apply_content_rating']
        metadata.content_rating = anime['ageRating']

    # metadata.countries = ? Countries involved in production of the show

    if Prefs['apply_poster_image']:
        if anime['posterImage'] is not None:
            poster_url = anime['posterImage']['original']
            if poster_url not in metadata.posters:
                metadata.posters[poster_url] = Proxy.Preview(requests.get(poster_url).content)

    # metadata.banners ?

    if Prefs['apply_cover_image']:
        if anime['coverImage'] is not None:
            cover_image_url = anime['coverImage']['original']
            if cover_image_url not in metadata.art:
                metadata.art[cover_image_url] = Proxy.Preview(requests.get(cover_image_url).content)

    # metadata.themes = ? Theme music

def updateAnimeTV(metadata, media):
    Log.Info('[' + AGENT_NAME + '] Updating to kitsu id ' + metadata.id + '.')

    anime_result = kitsu.anime.get(metadata.id)['data']
    anime = anime_result['attributes']

    applyAnime(metadata, anime)

    Log.Info('[' + AGENT_NAME + '] Updated to kitsu title "' + metadata.title + '".')

class KitsuTV(Agent.TV_Shows):
    name = AGENT_NAME
    languages = AGENT_LANGUAGES
    primary_provider = AGENT_PRIMARY_PROVIDER
    contributes_to = AGENT_CONTRIBUTES_TO

    def search(self, results, media, lang, manual):
        Log.Info('[' + AGENT_NAME + '] Received a search for KitsuTV.')
        matchAnime(results, media, 'tv')
        return

    def update(self, metadata, media, lang, force):
        Log.Info('[' + AGENT_NAME + '] Received an update for KitsuTV.')
        updateAnimeTV(metadata, media)
        return

class KitsuMovie(Agent.Movies):
    name = AGENT_NAME
    languages = AGENT_LANGUAGES
    primary_provider = AGENT_PRIMARY_PROVIDER

    def search(self, results, media, lang, manual):
        Log.Info('Got a search for Movie.')
        return

    def update(self, metadata, media, lang, force):
        Log.Info('Got a update for Movie.')
        return
