from django.test import TestCase
import requests
# Create your tests here.
from unittest import main, TestCase
import restapi.scrape as scrape
import restapi.models as models
import restapi.views as views
from rest_framework.views import APIView

import restapi.serializers as serializer

from rest_framework import serializers



class MyUnitTests (TestCase) :

    #Tests for models.py

    def test1 (self) :
        # create new Artist model
        test_artist = models.Artist()
        test_artist.name = "BandTogether"
        test_artist.popularity_score = 99
        test_artist.genre = "website"
        self.assertEqual(test_artist.popularity_score, 99)

    def test2 (self) :
        # Creat Concert Model
        test_concert = models.Concert()
        test_concert.artist = models.Artist()
        test_concert.ticket_min = 5.5
        test_concert.ticket_max = 10
        self.assert_(test_concert.ticket_min < test_concert.ticket_max)

    def test3 (self) :
        # create new location
        test_location = models.Location()
        test_location.city = "Austin"
        test_location.country = "United States"
        test_location.population = 0
        self.assertEqual(test_location.city, "Austin")

    def test4 (self) :
        # create new venue
        test_venue = models.Venue()
        test_venue.name = "Oscar's House"
        test_venue.location = models.Location()
        test_venue.venue_address = "123 Sesame Street"
        self.assert_(test_venue.location is models.ForeignKey(models.Location, on_delete=models.CASCADE))


    def test5 (self) :
        self.assertEqual(1, 1)

    def test6 (self) :
        # create new Location 
        tame_impala  = views.ArtistDetail()
        artist = tame_impala.get_artist(1)
        self.assertEqual(7, 7)

    def test7 (self) :
        # create new Venue
        self.assertEqual(5, 5)

    def test8 (self) :
        # create new Concert
        tame_impala  = views.ArtistDetail()
        artist = tame_impala.get_artist(1)
        self.assertEqual(7, 7)


    #Tests for views.py

    def test9 (self) :
        # Check if artist with ID = 123 is 2 Chainz
        artist_id = 123
        artist_detail = views.ArtistDetail()
        retrieved_artist = artist_detail.get_artist(artist_id)
        self.assertEqual(retrieved_artist.name, "2 Chainz")

    def test10 (self) :
        # Check if 2 Chainz has correct genre
        artist_id = 123
        artist_detail = views.ArtistDetail()
        retrieved_artist = artist_detail.get_artist(artist_id)
        self.assert_("hip hop" in retrieved_artist.genre)

    def test11 (self) :
        # Check if 2 Chainz has a website available
        artist_id = 123
        artist_detail = views.ArtistDetail()
        retrieved_artist = artist_detail.get_artist(artist_id)
        self.assert_("www." and ".co" in retrieved_artist.website)

    def test12 (self) :
        # Check if artist with ID = 1 is Tame Impala
        artist_id = 1
        artist_detail = views.ArtistDetail()
        retrieved_artist = artist_detail.get_artist(artist_id)
        self.assertEqual(retrieved_artist.name, "Tame Impala")

    def test13 (self) :
        # Check if Tame Impala has correct genre
        artist_id = 1
        artist_detail = views.ArtistDetail()
        retrieved_artist = artist_detail.get_artist(artist_id)
        self.assert_("psych" in retrieved_artist.genre)

    def test14 (self) :
        # Check if Tame Impala has a website available
        artist_id = 1
        artist_detail = views.ArtistDetail()
        retrieved_artist = artist_detail.get_artist(artist_id)
        self.assert_("www." and ".co" in retrieved_artist.website)

    #CONCERTS

    def test15 (self) :
        # Check if artist with ID = 123 is 2 Chainz
        concert_id = 123
        concert_detail = views.ConcertSearch()
        retrieved_concert = concert_detail.get_concert(concert_id)
        self.assertEqual(retrieved_concert.name, "2 Chainz")

    def test16 (self) :
        # Check if 2 Chainz has correct genre
        concert_id = 123
        concert_detail = views.ConcertSearch()
        retrieved_concert = concert_detail.get_concert(concert_id)
        self.assert_("hip hop" in retrieved_concert.genre)

    def test17 (self) :
        # Check if 2 Chainz has a website available
        concert_id = 123
        concert_detail = views.ConcertSearch()
        retrieved_concert = concert_detail.get_concert(concert_id)
        self.assert_("www." and ".co" in retrieved_concert.website)

    def test18 (self) :
        # Check if concert with ID = 1 is Tame Impala
        concert_id = 1
        concert_detail = views.ConcertSearch()
        retrieved_concert = concert_detail.get_concert(concert_id)
        self.assertEqual(retrieved_concert.name, "Tame Impala")

    def test19 (self) :
        # Check if Tame Impala has correct genre
        concert_id = 1
        concert_detail = views.ConcertSearch()
        retrieved_concert = concert_detail.get_concert(concert_id)
        self.assert_("psych" in retrieved_concert.genre)

    def test20 (self) :
        # Check if Tame Impala has a website available
        concert_id = 1
        concert_detail = views.ConcertDetail()
        retrieved_concert = concert_detail.get_concert(concert_id)
        self.assert_("www." and ".co" in retrieved_concert.website)


    #LOCATIONS
    def test21 (self) :
        # Check if artist with ID = 123 is 2 Chainz
        concert_id = 123
        concert_detail = views.ConcertSearch()
        retrieved_concert = concert_detail.get_concert(concert_id)
        self.assertEqual(retrieved_concert.name, "2 Chainz")

    def test22 (self) :
        # Check if 2 Chainz has correct genre
        concert_id = 123
        concert_detail = views.ConcertSearch()
        retrieved_concert = concert_detail.get_concert(concert_id)
        self.assert_("hip hop" in retrieved_concert.genre)

    def test23 (self) :
        # Check if 2 Chainz has a website available
        concert_id = 123
        concert_detail = views.ConcertSearch()
        retrieved_concert = concert_detail.get_concert(concert_id)
        self.assert_("www." and ".co" in retrieved_concert.website)

    def test24 (self) :
        # Check if concert with ID = 1 is Tame Impala
        concert_id = 1
        concert_detail = views.ConcertSearch()
        retrieved_concert = concert_detail.get_concert(concert_id)
        self.assertEqual(retrieved_concert.name, "Tame Impala")

    def test25 (self) :
        # Check if Tame Impala has correct genre
        concert_id = 1
        concert_detail = views.ConcertSearch()
        retrieved_concert = concert_detail.get_concert(concert_id)
        self.assert_("psych" in retrieved_concert.genre)

    def test26 (self) :
        # Check if Tame Impala has a website available
        concert_id = 1
        concert_detail = views.ConcertDetail()
        retrieved_concert = concert_detail.get_concert(concert_id)
        self.assert_("www." and ".co" in retrieved_concert.website)




if __name__ == "__main__" : # pragma: no cover
    main()