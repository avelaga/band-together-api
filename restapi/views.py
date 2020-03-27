from django.shortcuts import render
from .models import Concert, Artist, Location, Album, Venue
from rest_framework import generics
from .models import Concert, Artist, Location, Album, Venue
from .serializers import ConcertSerializer, ArtistSerializer, LocationSerializer
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import time

'''
API endpoint that lists all of the artists in the database
'''
class ArtistList(generics.ListAPIView):
  queryset = Artist.objects.all()
  serializer_class = ArtistSerializer

'''
API endpoint that lists all locations in the database
'''
class LocationList(generics.ListAPIView):
  queryset = Location.objects.all()
  serializer_class = LocationSerializer

'''
API endpoint that lists all concerts in the database
'''
class ConcertList(generics.ListAPIView):
  queryset = Concert.objects.all()
  serializer_class = ConcertSerializer

# Calling this function will scrape the API's and load up our database
def web_scrape():
    tik = time.perf_counter()
    try:
        citySet = set()
        venueSet = set()
        artistSet = set()
        concertSet = set()
        newArtistSet = set()
        newVenueSet = set()

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
        
        for artistName in newArtistSet:
                newArtist = getArtist(artistName=artistName, sp=sp, artistSet=artistSet, newArtistSet=newArtistSet)

        while len(newArtistSet) != 0 or len(newVenueSet) != 0
            for artistName in newArtistSet:
                artist = Artist.objects.get(name=artistName)
                event_params = base_params.copy()
                event_params.update({'keyword': artist.name})
                r = requests.get(url=event_url, params=event_params)
                events = r.json()['_embedded']['events']
                for event in events:
                    if 'name' in event['_embedded']['venues'][0].keys() and (not 'Festival' == event['_embedded']['classifications'][0]['subtype']['name']):
                        getConcert(event, artist, concertSet, citySet, venueSet, artistSet, newArtistSet True)
                newArtistSet.remove(artistName)

            for venueName in newVenueSet:
                venue = Venue.objects.get(name=venueName)
                event_params = base_params.copy()
                event_params.update({'venueId': venue.venue_id})
                r = requests.get(url=event_url, params=event_params)
                events = r.json()['_embedded']['events']
                for event in events:
                    if event['classifications'][0]['segment']['name'] == 'Music' and (not 'Festival' == event['_embedded']['classifications'][0]['subtype']['name']):
                        getConcert(event, venue, concertSet, citySet, venueSet, artistSet, newArtistSet True)
                newVenueSet.remove(venueName)

        tok = time.perf_counter()
        print("Time in seconds: " + str(tok - tik))
    except Exception as e:
        print(e.args)
        print("Dude it took " + str(tok-tik) " seconds to fuck up")

def getConcert(concert_items, given, concertSet, citySet, venueSet, newVenueSet, artistSet, newArtistSet, givenIsArtist):
    try:
        concert_id = concert_items['id']
        if concert_id in concertSet:
            return Concert.objects.get(concert_id=concert_id)
        cityName = concert_items['_embedded']['venues'][0]['city']['name']
        location = getLocation(cityName, citySet)
        
        date = concert_items['dates']['start']['localDate']
        time = concert_items['dates']['start']['localTime']
        min_ticket = concert_items['priceRanges'][0]['min']
        max_ticket = concert_items['priceRanges'][0]['max']
        newConcert = None
        if givenIsArtist:
            venue = getVenue(concert_items, location, venueSet)
            newConcert = Concert(artist=given, location=location, venue=venue, date=date, time=time, concert_id=concert_id, ticket_min=min_ticket, ticket_max=max_ticket)
        else:
            artist = 
        concertSet.add(concert_id)
        newConcert.save()
    except:
        pass

def getVenue(concert_items, location, venueSet, newVenueSet):
    name = concert_items['_embedded']['venues'][0]['name']
    if name in venueSet:
        return Venue.objects.get(name=name)
    location = location
    address = concert_items['_embedded']['venues'][0]['address']
    parking_info = concert_items['_embedded']['venues'][0]['parkingDetail']
    postalCode = concert_items['_embedded']['venues'][0]['postalCode']
    image = concert_items['_embedded']['venues'][0]['images'][0]
    venue_id = concert_items['_embedded']['venues'][0]['id']
    newVenue = Venue(name=name, location=location, venue_address=address, parking_info=parking_info, postal_code=postalCode, venue_id=venue_id)
    venueSet.add(name)
    newVenueSet.add(name)
    newVenue.save()
    return newVenue

def getLocation(cityName, citySet):
    if cityName in citySet:
        return Location.objects.get(city=cityName)
    params = {'limit': 1, 'offset': 0, 'namePrefix': cityName}
    city = requests.get(url='http://geodb-free-service.wirefreethought.com/v1/geo/cities', params=params)
    city_items = city.json()
    city_items = city_items['data'][0]
    city_id = city_items['id']
    cityDetails = requests.get(url='http://geodb-free-service.wirefreethought.com/v1/geo/cities/' + str(city_id))
    cityDetails = cityDetails.json()
    cityDetails = cityDetails['data']
    city = city_items['city']
    country = city_items['country']
    if country != "United States of America":
        raise Exception()
    region = city_items['region']
    population = cityDetails['population']
    elevation = cityDetails['elevationMeters']
    timezone = cityDetails['timezone']

    newLocation = Location(city=city, country=country, population=population, timezone=timezone, region=region, elevation=elevation)
    citySet.add(cityName)
    newLocation.save()
    return newLocation


def getArtist(artistName, sp, artistSet, newArtistSet):
    if artistName in artistSet:
        return Artist.objects.get(name=artistName)
    artist = sp.search(q=artistName, type='artist', limit=1, offset=0)
    artist_items = artist['artists']['items'][0]
    name = artist_items['name']
    popularity = artist_items['popularity']
    genre = artist_items['genres'][0]
    spotify_url = artist_items['external_urls']['spotify']
    followers = artist_items['followers']['total']
    image_url = artist_items['images'][0]['url']
    
    newArtist = Artist(name=name, popularity_score=popularity, genre=genre, image=image_url, spotify_url=spotify_url, num_spotify_followers=followers)
    artistSet.add(name)
    newArtistSet.add(name)
    newArtist.save()
    return newArtist

def spotifyTest():
    cid = ''
    secret = ''
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    artist = sp.search(q='John Mayer', type='artist', limit=1, offset=0)
    print(artist)