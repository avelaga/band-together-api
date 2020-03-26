from django.shortcuts import render
from rest_framework import generics
from .models import Concert, Artist, Location, Album, Venue
from .serializers import ConcertSerializer, ArtistSerializer, LocationSerializer, AlbumSerializer, VenueSerializer
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests

class ArtistList(generics.ListAPIView):
  queryset = Artist.objects.all() # where data is coming from
  serializer_class = ArtistSerializer

class LocationList(generics.ListAPIView):
  queryset = Location.objects.all() # where data is coming from
  serializer_class = LocationSerializer

class VenueList(generics.ListAPIView):
  queryset = Venue.objects.all() # where data is coming from
  serializer_class = VenueSerializer

class ConcertList(generics.ListAPIView):
  queryset = Concert.objects.all() # where data is coming from
  serializer_class = ConcertSerializer

class AlbumList(generics.ListAPIView):
  queryset = Album.objects.all() # where data is coming from
  serializer_class = AlbumSerializer

# Calling this function will scrape the API's and load up our database
def web_scrape():
    cid = '15b2abfe5a754bdcb5e75cbf056f7985'
    secret = '439b829d6d084631b09d4a9773adc80c'
    ticketmaster_cid = 'oBmSAafLPLFBbfAJFhN39CLjJcIHOP1N'
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

