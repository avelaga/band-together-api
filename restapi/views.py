from django.shortcuts import render
from models import Concert, Artist, Location, Album, Venue
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests

# Calling this function will scrape the API's and load up our database
def web_scrape():
    cid = ''
    secret = ''
    ticketmaster_cid = ''
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    ticketmaster_base_url = 'https://app.ticketmaster.com/discovery/v2/'
    venue_url = ticketmaster_base_url + '/venues'
    base_params = {"apikey": ticketmaster_cid}
    venue_params = base_params.copy()
    venue_params.update({"keyword": "Frank Erwin Center", "limit": 1})
    event_url = ticketmaster_base_url + "/events"
    event_params = base_params.copy()
    event_params.update({"venueId": "KovZpZA7dE7A"})

    r = requests.get(url=event_url, params=event_params)

    events = r.json()['_embedded']['events']
    artistNames = []
    for event in events:
        if event['classifications'][0]['segment']['name'] == 'Music':
            name = event['name']
            splitName = name.split(" w/")
            artistNames.append(splitName[0])

    for artistName in artistNames:
        artist = sp.search(q=artistName, type='artist', limit=1, offset=0)
        name = artist['artists']['items'][0]['name']
        popularity = artist['artists']['items'][0]['popularity']

    for val in artists:
        event_params = base_params.copy()
        event_params.update({'keyword': val.name})
        r = requests.get(url=event_url, params=event_params)
        events = r.json()['_embedded']['events']
        for event in events:
            if 'name' in event['_embedded']['venues'][0].keys():
                venueName = event['_embedded']['venues'][0]['name']

