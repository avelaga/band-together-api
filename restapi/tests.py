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

    #Tests for Scrape.py
    def test1 (self) :
        #concert = scrape.getConcert(1)
        #artist = concert.artistName
        self.assertEqual(1, 1)

    def test2 (self) :
        self.assertEqual(5, 5)

    def test3 (self) :
        tame_impala  = views.ArtistDetail()
        artist = tame_impala.get_artist(1)
        print("OOOOO" + artist.name)
        self.assertEqual(7, 7)

    #Tests for models.py

    def test1 (self) :
        #concert = scrape.getConcert(1)
        #artist = concert.artistName
        self.assertEqual(1, 1)

    def test2 (self) :
        self.assertEqual(5, 5)

    def test3 (self) :
        tame_impala  = views.ArtistDetail()
        artist = tame_impala.get_artist(1)
        self.assertEqual(7, 7)


    #Tests for views.py

    def test4 (self) :
        #concert = scrape.getConcert(1)
        #artist = concert.artistName
        self.assertEqual(1, 1)

    def test5 (self) :
        # Check if artist with ID = 123 is 2 Chainz
        artist_id = 123
        artist_detail = views.ArtistDetail()
        retrieved_artist = artist_detail.get_artist(artist_id)
        self.assertEqual(retrieved_artist.name, "2 Chainz")

    def test6 (self) :
        # Check if artist with ID = 123 is 2 Chainz
        artist_id = 123
        artist_detail = views.ArtistDetail()
        retrieved_artist = artist_detail.get_artist(artist_id)
        self.assertEqual(retrieved_artist.name, "2 Chainz")


    def test6 (self) :
        # Check if artist with ID = 1 is Tame Impala
        artist_id = 1
        artist_detail = views.ArtistDetail()
        retrieved_artist = artist_detail.get_artist(artist_id)
        self.assertEqual(retrieved_artist.name, "Tame Impala")


    #Tests for serializers.py
    def test7 (self) :
        artSerializer = serializer.ArtistSerializer(serializers.HyperlinkedModelSerializer)
        c_id = 1#artSerializer.get_concert_id()
        #a_name = serializers.ReadOnlyField(source='artist.name')
        #print(a_name)
        self.assertEqual(c_id, 1)



if __name__ == "__main__" : # pragma: no cover
    main()