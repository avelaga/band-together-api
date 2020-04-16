from django.shortcuts import render
from .models import Concert, Artist, Location, Album, Venue
from rest_framework import generics
from .models import Concert, Artist, Location, Album, Venue
from .serializers import (
    ConcertSerializer,
    ArtistSerializer,
    LocationSerializer,
    VenueSerializer,
    ArtistListSerializer,
    LocationListSerializer,
)
from django.core import serializers
import time
import json
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from rest_framework.settings import api_settings
from itertools import chain

def search_artist(query):
    return Q(name__icontains=query) | Q(genre__icontains=query) | Q(popularity_score__icontains=query) | Q(num_spotify_followers__icontains=query)

def search_concert(query):
    return Q(date__icontains=query) | Q(ticket_min__icontains=query) | Q(ticket_max__icontains=query)

def search_location(query):
    return Q(city__icontains=query) | Q(timezone__icontains=query) | Q(region__icontains=query) | Q(elevation__icontains=query) | Q(population__icontains=query)

def search_venue(query):
    return Q(name__icontains=query)

"""
API endpoints for artist
"""
class ArtistList(generics.ListAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistListSerializer


class ArtistSearch(generics.ListAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistListSerializer
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    def get(self, request, format=None):
        a = None
        if "query" in request.query_params:
            query = request.query_params["query"]
            qs = search_artist(query)
            a = Artist.objects.filter(qs)
        else:
            a = Artist.objects.all()
        serializer = self.serializer_class(a, many=True)
        return Response(serializer.data)

class ArtistDetail(APIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

    def get_artist(self, pk):
        try:
            return Artist.objects.get(pk=pk)
        except Artist.DoesNotExist:
            return "Not available"

    def get_concert(self, artist):
        concerts = Concert.objects.filter(artist=artist)
        return list(concerts.order_by("date")[:1])[0]

    def get(self, request, pk, format=None):
        artist = self.get_artist(pk)
        concert = self.get_concert(artist)
        venue = concert.venue
        location = concert.location
        context = {
            "nextVenueName": venue.name,
            "nextConcertId": concert.id,
            "nextConcertDate": concert.date,
            "nextConcertTime": concert.time,
            "nextLocationName": location.city,
            "nextLocationId": location.id,
        }

        serializer = self.serializer_class(artist, context=context)
        return Response(serializer.data)


"""
API endpoints for locations
"""
class LocationList(generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationListSerializer


class LocationDetail(generics.RetrieveAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def get_location(self, pk):
        return Location.objects.get(pk=pk)

    def get_concert(self, location):
        concerts = Concert.objects.filter(location=location)
        return list(concerts.order_by("date")[:1])[0]

    def get(self, request, pk, format=None):
        location = self.get_location(pk)
        concert = self.get_concert(location)
        venue = concert.venue
        artist = concert.artist
        context = {
            "nextVenueName": venue.name,
            "nextConcertId": concert.id,
            "nextConcertDate": concert.date,
            "nextConcertTime": concert.time,
            "nextArtistName": artist.name,
            "nextArtistId": artist.id,
        }

        serializer = self.serializer_class(location, context=context)
        return Response(serializer.data)

class LocationSearch(generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationListSerializer
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    def get(self, request, format=None):
        a = None
        if "query" in request.query_params:
            query = request.query_params["query"]
            qs = search_location(query)
            l = Location.objects.filter(qs)
        else:
            l = Location.objects.all()
        serializer = self.serializer_class(l, many=True)
        return Response(serializer.data)

"""
API endpoints for concerts
"""
class ConcertList(generics.ListAPIView):
    queryset = Concert.objects.all()
    serializer_class = ConcertSerializer


class ConcertDetail(generics.RetrieveAPIView):
    queryset = Concert.objects.all()
    serializer_class = ConcertSerializer

class ConcertSearch(generics.ListAPIView):
    queryset = Concert.objects.all()
    serializer_class = ConcertSerializer

    def get(self, request, format=None):
        c_results = None
        if 'query' in request.query_params:
            query = request.query_params['query']
            cqs = search_concert(query)
            c_results = Concert.objects.filter(cqs)
            aqs = search_artist(query)
            for a in Artist.objects.filter(aqs):
                c_results |= Concert.objects.filter(artist=a)
            lqs = search_location(query)
            for l in Location.objects.filter(lqs):
                c_results |= Concert.objects.filter(location=l)
            vqs = search_venue(query)
            for v in Venue.objects.filter(vqs):
                c_results |= Concert.objects.filter(venue=v)
        else:
            c_results = Concert.objects.all()
        serializer = self.serializer_class(c_results, many=True, context={'request': request})
        return Response(serializer.data)
        
"""
API endpoints for venues
"""
class VenueList(generics.ListAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer


class VenueDetail(generics.RetrieveAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer