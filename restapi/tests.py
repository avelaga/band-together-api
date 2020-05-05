from django.test import TestCase
import requests

# Create your tests here.
from unittest import main, TestCase
import restapi.scrape as scrape
import restapi.models as models
import restapi.views as views
from rest_framework.views import APIView
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


import restapi.serializers as serializer

from rest_framework import serializers


class MyUnitTests(TestCase):

    # Tests for models.py

    def test1(self):
        # create new Artist model
        test_artist = models.Artist()
        test_artist.name = "BandTogether"
        test_artist.popularity_score = 99
        test_artist.genre = "website"
        self.assertEqual(test_artist.popularity_score, 99)

    def test2(self):
        # Creat Concert Model
        test_concert = models.Concert()
        test_concert.artist = models.Artist()
        test_concert.ticket_min = 5.5
        test_concert.ticket_max = 10
        self.assert_(test_concert.ticket_min < test_concert.ticket_max)

    def test3(self):
        # create new location
        test_location = models.Location()
        test_location.city = "Austin"
        test_location.country = "United States"
        test_location.population = 0
        self.assertEquals(test_location.city, "Austin")

    def test4(self):
        # create new venue
        test_venue = models.Venue()
        test_venue.name = "Oscar's House"
        test_venue.location = models.Location()
        test_venue.venue_address = "123 Sesame Street"
        self.assert_(type(test_venue.location) is models.Location)

    # Tests for views.py

    def test5(self):
        # Check if artist with ID = 123 is 2 Chainz
        artist_id = 123
        artist_detail = views.ArtistDetail()
        retrieved_artist = artist_detail.get_artist(artist_id)
        self.assertEqual(retrieved_artist.name, "2 Chainz")

    def test6(self):
        # Check if 2 Chainz has correct genre
        artist_id = 123
        artist_detail = views.ArtistDetail()
        retrieved_artist = artist_detail.get_artist(artist_id)
        self.assert_("hip hop" in retrieved_artist.genre)

    def test7(self):
        # Check if 2 Chainz has a website available
        artist_id = 123
        artist_detail = views.ArtistDetail()
        retrieved_artist = artist_detail.get_artist(artist_id)
        self.assert_("www." and ".co" in retrieved_artist.website)

    def test8(self):
        # Check if artist with ID = 1 is Tame Impala
        artist_id = 1
        artist_detail = views.ArtistDetail()
        retrieved_artist = artist_detail.get_artist(artist_id)
        self.assertEqual(retrieved_artist.name, "Tame Impala")

    def test9(self):
        # Check if Tame Impala has correct genre
        artist_id = 1
        artist_detail = views.ArtistDetail()
        retrieved_artist = artist_detail.get_artist(artist_id)
        self.assert_("psych" in retrieved_artist.genre)

    def test10(self):
        # Check if Tame Impala has a website available
        artist_id = 1
        artist_detail = views.ArtistDetail()
        retrieved_artist = artist_detail.get_artist(artist_id)
        self.assert_("www." and ".co" in retrieved_artist.website)

    def test11(self):
        # Check if concert with ID = 123 is a Chicago concert
        concert_id = 123
        concert_detail = models.Concert.objects.get(pk=concert_id)
        self.assertEqual(concert_detail.artist.name, "Chicago")

    def test12(self):
        # Check if concert with ID = 123 is in Dallas
        concert_id = 123
        concert_detail = models.Concert.objects.get(pk=concert_id)
        self.assertEqual(concert_detail.location.city, "Dallas")

    def test13(self):
        # Check retrieval of concerts in city with pk 1
        location_id = 1
        location_detail = views.LocationDetail()
        retrieved_location = location_detail.get_location(location_id)
        retrieved_concerts = location_detail.get_concert(retrieved_location)
        self.assert_(type(retrieved_concerts) is models.Concert)

    def test14(self):
        # Check current number of concert instances
        concert_detail = views.ConcertDetail()
        retrieved_concerts = models.Concert.objects.all()
        self.assertEqual(len(retrieved_concerts), 877)

    def test15(self):
        # Check if Location with pk 12 is Miami
        location_id = 12
        location_detail = views.LocationDetail()
        retrieved_location = location_detail.get_location(location_id)
        self.assertEqual(retrieved_location.city, "Miami")

    def test16(self):
        # Check if next artist playing in Miami is correct
        location_id = 12
        location_detail = views.LocationDetail()
        retrieved_location = location_detail.get_location(location_id)
        views_timezone = retrieved_location.timezone
        direct_access_timezone = models.Location.objects.get(pk=location_id).timezone
        self.assertEqual(views_timezone, direct_access_timezone)

    def test17(self):
        # Check if genre from concert is correct
        concert_id = 123
        concert_detail = models.Concert.objects.get(pk=concert_id)
        concert_genre = concert_detail.artist.genre
        self.assertEqual(concert_genre, "adult standards")

    def test18(self):
        # check invalid artist
        cid = "15b2abfe5a754bdcb5e75cbf056f7985"
        secret = "596d5d4c5ee84749ae4e67de0f0dd079"
        client_credentials_manager = SpotifyClientCredentials(
            client_id=cid, client_secret=secret
        )
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        with self.assertRaises(Exception) as cm:
            scrape.getArtist(
                "SWE", sp, artistSet=set(), newArtistSet=set(), concert_items=set()
            )
        err = cm.exception
        self.assertEqual(str(err), "Bad Request")

    def test19(self):
        # check invalid loc

        with self.assertRaises(Exception) as cm:
            scrape.getLocation("sesame street", citySet=set())
        err = cm.exception
        self.assertEqual(str(err), "list index out of range")

    def test20(self):
        # Check invalid loc

        with self.assertRaises(Exception) as cm:
            scrape.getLocation("Abu Dhabi", citySet=set())
        err = cm.exception
        self.assertEqual(str(err), "Not in USA")

    def test21(self):
        # Check if venue lat long is correct
        venue_id = 13
        venue_detail = models.Venue.objects.get(pk=venue_id)
        venue_lat = venue_detail.lat
        venue_long = venue_detail.lon
        self.assertEqual((venue_lat, venue_long), (43.04228, -87.916896))

    def test22(self):
        # Check if venue addr is correct
        venue_id = 123
        venue_detail = models.Venue.objects.get(pk=venue_id)
        self.assertEqual(venue_detail.venue_address, "347 Don Shula Drive")


if __name__ == "__main__":  # pragma: no cover
    main()
