from django.shortcuts import render

#Calling this function will scrape the API's and load up our database
def web_scrape():
    import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests

class Artist:
    def __init__(self):
        name = ""
        popularity = -1

    def __str__(self):
        return self.name + ": " + str(self.popularity)

class Location:
    def __init__(self):
        city = ""
        country = ""

class Concert:
    def __init__(self):
        location = None
        artist = None
        venue = ""
        date = ""

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
artists = []
locations = []
concerts = []

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
    newArtist = Artist()
    newArtist.name = artist['artists']['items'][0]['name']
    newArtist.popularity = artist['artists']['items'][0]['popularity']
    artists.append(newArtist)

for val in artists:
    event_params = base_params.copy()
    event_params.update({'keyword': val.name})
    r = requests.get(url=event_url, params=event_params)
    events = r.json()['_embedded']['events']
    print()
    print()
    print(val.name)
    for event in events:
        if 'name' in event['_embedded']['venues'][0].keys():
            newConcert = Concert()
            newConcert.venue = event['_embedded']['venues'][0]['name']
            print(newConcert.venue)

