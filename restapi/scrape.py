from .models import Concert, Artist, Location, Album, Venue
from .models import Concert, Artist, Location, Album, Venue
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import time
import json
import sys

# Calling this function will scrape the API's and load up our database
def web_scrape():
    tik = time.perf_counter()
    citySet = set()
    venueSet = set()
    artistSet = set()
    concertSet = set()
    newArtistSet = set()
    newVenueSet = set()

    cid = "15b2abfe5a754bdcb5e75cbf056f7985"
    secret = "0b9d36d4daf941eb92b6d8559b25d949"
    ticketmaster_cid = "oBmSAafLPLFBbfAJFhN39CLjJcIHOP1N"
    client_credentials_manager = SpotifyClientCredentials(
        client_id=cid, client_secret=secret
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    ticketmaster_base_url = "https://app.ticketmaster.com/discovery/v2/"
    venue_url = ticketmaster_base_url + "/venues"
    base_params = {"apikey": ticketmaster_cid}
    venue_params = base_params.copy()
    venue_params.update({"keyword": "Frank Erwin Center", "limit": 1})
    event_url = ticketmaster_base_url + "/events"
    event_params = base_params.copy()
    event_params.update(
        {
            "venueId": "KovZpZA7dE7A",
            "classificationName": json.dumps(["music", "-festival"]),
        }
    )

    r = requests.get(url=event_url, params=event_params)

    events = r.json()["_embedded"]["events"]
    artistNames = []
    eventVals = []
    for event in events:
        name = event["_embedded"]["attractions"][0]["name"]
        eventVals.append(event)
        artistNames.append(name)

    for i in range(0, len(artistNames)):
        artistName = artistNames[i]
        concert_items = eventVals[i]
        newArtist = getArtist(
            artistName=artistName,
            sp=sp,
            artistSet=artistSet,
            newArtistSet=newArtistSet,
            concert_items=concert_items,
        )
    count = 0
    while len(newArtistSet) != 0 or len(newVenueSet) != 0:
        count = count + 1
        print(count)
        for artistName in artistSet:
            if artistName in newArtistSet:
                artist = Artist.objects.get(name=artistName)
                print(
                    "----------------------------"
                    + artist.name
                    + "--------------------------------"
                )
                event_params = base_params.copy()
                event_params.update({"keyword": artist.name})
                event_params.update(
                    {"classificationName": json.dumps(["music", "-festival"])}
                )
                r = requests.get(url=event_url, params=event_params)
                if "_embedded" in r.json():
                    events = r.json()["_embedded"]["events"]
                    for event in events:
                        if (
                            "name" in event["_embedded"]["venues"][0].keys()
                        ):  # We only want venues with names
                            print(event["_embedded"]["venues"][0]["name"])
                            getConcert(
                                event,
                                artist,
                                concertSet,
                                citySet,
                                venueSet,
                                newVenueSet,
                                artistSet,
                                newArtistSet,
                                True,
                                sp,
                            )
                newArtistSet.remove(artistName)

        print("Entering venue loop")
        for venueName in venueSet:
            if venueName in newVenueSet:
                venue = Venue.objects.get(name=venueName)
                event_params = base_params.copy()
                event_params.update({"venueId": venue.venue_id})
                event_params.update(
                    {"classificationName": json.dumps(["music", "-festival"])}
                )
                r = requests.get(url=event_url, params=event_params)
                events = r.json()["_embedded"]["events"]
                for event in events:
                    getConcert(
                        event,
                        venue,
                        concertSet,
                        citySet,
                        venueSet,
                        newVenueSet,
                        artistSet,
                        newArtistSet,
                        False,
                        sp,
                    )
                newVenueSet.remove(venueName)

    tok = time.perf_counter()
    print("Time in seconds: " + str(tok - tik))


# exec(open("script.py").read())


def getConcert(
    concert_items,
    given,
    concertSet,
    citySet,
    venueSet,
    newVenueSet,
    artistSet,
    newArtistSet,
    givenIsArtist,
    sp,
):
    try:
        concert_id = concert_items["id"]
        if concert_id in concertSet:
            return Concert.objects.get(concert_id=concert_id)
        cityName = concert_items["_embedded"]["venues"][0]["city"]["name"]
        location = getLocation(cityName, citySet)
        date = None
        if "localDate" in concert_items["dates"]["start"]:
            date = concert_items["dates"]["start"]["localDate"]
        time = None
        if "localTime" in concert_items["dates"]["start"]:
            time = concert_items["dates"]["start"]["localTime"]
        min_ticket = None
        max_ticket = None
        if "priceRanges" in concert_items.keys():
            min_ticket = concert_items["priceRanges"][0]["min"]
            max_ticket = concert_items["priceRanges"][0]["max"]
        newConcert = None
        if givenIsArtist:
            venue = None
            try:
                venue = getVenue(concert_items, location, venueSet, newVenueSet)
            except:
                pass
            newConcert = Concert(
                artist=given,
                location=location,
                venue=venue,
                date=date,
                time=time,
                concert_id=concert_id,
                ticket_min=min_ticket,
                ticket_max=max_ticket,
            )
        else:
            artistName = concert_items["_embedded"]["attractions"][0]["name"]
            print(artistName)
            artist = getArtist(artistName, sp, artistSet, newArtistSet, concert_items)
            newConcert = Concert(
                artist=artist,
                location=location,
                venue=given,
                date=date,
                time=time,
                concert_id=concert_id,
                ticket_min=min_ticket,
                ticket_max=max_ticket,
            )
        concertSet.add(concert_id)
        newConcert.save()
    except Exception as e:
        exc_type, exc_obj, tb = sys.exc_info()
        lineno = tb.tb_lineno
        print("Exception thrown: " + str(e.args) + " on " + str(lineno))


def getVenue(concert_items, location, venueSet, newVenueSet):
    name = concert_items["_embedded"]["venues"][0]["name"]
    if name in venueSet:
        return Venue.objects.get(name=name)
    location = location
    address = concert_items["_embedded"]["venues"][0]["address"]["line1"]
    parking_info = None
    if "parkingDetail" in concert_items["_embedded"]["venues"][0]:
        parking_info = concert_items["_embedded"]["venues"][0]["parkingDetail"]
    postalCode = None
    if "postalCode" in concert_items["_embedded"]["venues"][0]:
        postalCode = concert_items["_embedded"]["venues"][0]["postalCode"]
    image = None
    if "images" in concert_items["_embedded"]["venues"][0]:
        image = concert_items["_embedded"]["venues"][0]["images"][0]["url"]
    venue_id = concert_items["_embedded"]["venues"][0]["id"]
    lat = float(concert_items["_embedded"]["venues"][0]["location"]["latitude"])
    lon = float(concert_items["_embedded"]["venues"][0]["location"]["longitude"])
    newVenue = Venue(
        name=name,
        location=location,
        venue_address=address,
        parking_info=parking_info,
        postal_code=postalCode,
        venue_id=venue_id,
        image=image,
        lat=lat,
        lon=lon,
    )
    venueSet.add(name)
    newVenueSet.add(name)
    newVenue.save()
    return newVenue


def getLocation(cityName, citySet):
    if cityName in citySet:
        return Location.objects.get(city=cityName)
    params = {"limit": 1, "offset": 0, "namePrefix": cityName}
    city = requests.get(
        url="http://geodb-free-service.wirefreethought.com/v1/geo/cities", params=params
    )
    city_items = city.json()
    city_items = city_items["data"][0]
    city_id = city_items["id"]
    cityDetails = requests.get(
        url="http://geodb-free-service.wirefreethought.com/v1/geo/cities/"
        + str(city_id)
    )
    cityDetails = cityDetails.json()
    cityDetails = cityDetails["data"]
    city = city_items["city"]
    country = city_items["country"]
    if country != "United States of America":
        raise Exception("Not in USA")
    region = city_items["region"]
    population = cityDetails["population"]
    elevation = cityDetails["elevationMeters"]
    timezone = cityDetails["timezone"]
    rurl = "https://en.wikipedia.org/api/rest_v1/page/summary/" + city
    r = requests.get(rurl)
    cityInfo = r.json()
    image = cityInfo["thumbnail"]["source"]
    bio = cityInfo["extract"]
    lat = cityInfo["coordinates"]["lat"]
    lon = cityInfo["coordinates"]["lon"]
    newLocation = Location(
        city=city,
        country=country,
        population=population,
        timezone=timezone,
        region=region,
        elevation=elevation,
        image=image,
        bio=bio,
        lat=lat,
        lon=lon,
    )
    citySet.add(cityName)
    newLocation.save()
    return newLocation


def getArtist(artistName, sp, artistSet, newArtistSet, concert_items):
    artist = sp.search(q=artistName, type="artist", limit=1, offset=0)
    artist_items = artist["artists"]["items"][0]
    name = artist_items["name"]
    if name in artistSet:
        return Artist.objects.get(name=name)
    popularity = artist_items["popularity"]
    genre = artist_items["genres"][0]
    spotify_url = artist_items["external_urls"]["spotify"]
    followers = artist_items["followers"]["total"]
    image_url = artist_items["images"][0]["url"]
    twitter_url = None
    wiki_url = None
    website = None
    if "externalLinks" in concert_items["_embedded"]["attractions"][0]:
        if "twitter" in concert_items["_embedded"]["attractions"][0]["externalLinks"]:
            twitter_url = concert_items["_embedded"]["attractions"][0]["externalLinks"][
                "twitter"
            ][0]["url"]
        if "wiki" in concert_items["_embedded"]["attractions"][0]["externalLinks"]:
            wiki_url = concert_items["_embedded"]["attractions"][0]["externalLinks"][
                "wiki"
            ][0]["url"]
        if "homepage" in concert_items["_embedded"]["attractions"][0]["externalLinks"]:
            website = concert_items["_embedded"]["attractions"][0]["externalLinks"][
                "homepage"
            ][0]["url"]
    aurl = "https://en.wikipedia.org/api/rest_v1/page/summary/" + name.replace(" ", "_") + "_(band)"
    a = requests.get(aurl)
    aInfo = a.json()
    if aInfo['title'] == "Not found.":
        aurl = "https://en.wikipedia.org/api/rest_v1/page/summary/" + name.replace(" ", "_") + "_(musician)"
        a = requests.get(aurl)
        aInfo = a.json()
        if aInfo['title'] == "Not found.":
            aurl = "https://en.wikipedia.org/api/rest_v1/page/summary/" + name.replace(" ", "_")
            a = requests.get(aurl)
            aInfo = a.json()
    bio = None
    if 'extract' in aInfo:
        bio = aInfo["extract"]
    newArtist = Artist(
        name=name,
        popularity_score=popularity,
        genre=genre,
        image=image_url,
        spotify_url=spotify_url,
        num_spotify_followers=followers,
        twitter_url=twitter_url,
        wiki_url=wiki_url,
        website=website,
        bio=bio
    )
    artistSet.add(name)
    newArtistSet.add(name)
    newArtist.save()
    return newArtist

# exec(open("script.py").read())

def spotifyTest():
    cid = "15b2abfe5a754bdcb5e75cbf056f7985"
    secret = ""
    client_credentials_manager = SpotifyClientCredentials(
        client_id=cid, client_secret=secret
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    aid = '16oZKvXb6WkQlVAjwo2Wbg'
    artist = sp.search(q="The Lumineers", type="artist", limit=1, offset=0)
    print(artist)