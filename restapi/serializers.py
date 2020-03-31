from rest_framework import serializers
from .models import Concert, Artist, Location, Venue

class ConcertSerializer(serializers.HyperlinkedModelSerializer):
  artistName = serializers.ReadOnlyField(source='artist.name')
  artistId = serializers.ReadOnlyField(source='artist.id')
  locationName = serializers.ReadOnlyField(source='location.city')
  locationId = serializers.ReadOnlyField(source='location.id')
  artistImage = serializers.ReadOnlyField(source='artist.image')
  venueImage = serializers.ReadOnlyField(source='venue.image')
  class Meta:
    model = Concert
    fields = ['id', 'artist', 'location', 'venue', 'date', 'time', 'ticket_min', 'ticket_max', 'artistName', 'locationName', 'artistId', 'locationId', 'artistImage', 'venueImage']

class ArtistListSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Artist
    fields = ['id', 'name', 'popularity_score', 'genre', 'image', 'spotify_url', 'num_spotify_followers', 'website', 'twitter_url', 'wiki_url']

class ArtistSerializer(serializers.HyperlinkedModelSerializer):
  nextVenueName = serializers.SerializerMethodField('get_venue_name')
  nextConcertId = serializers.SerializerMethodField('get_concert_id')
  nextLocationName = serializers.SerializerMethodField('get_location_name')
  nextLocationId = serializers.SerializerMethodField('get_location_id')

  def get_venue_name(self, obj):
    return self.context['nextVenueName']

  def get_concert_id(self, obj):
    return self.context['nextConcertId']
  
  def get_location_name(self, obj):
    return self.context['nextLocationName']

  def get_location_id(self, obj):
    return self.context['nextLocationId']

  class Meta:
    model = Artist
    fields = ['id', 'name', 'popularity_score', 'genre', 'image', 'spotify_url', 'num_spotify_followers', 'website', 'twitter_url', 'wiki_url', 'nextVenueName', 'nextConcertId', 'nextLocationName', 'nextLocationId']


class LocationListSerializer(serializers.HyperlinkedModelSerializer):

  class Meta:
    model = Location
    fields = ['id', 'city', 'country', 'population', 'timezone', 'region', 'area_code', 'elevation', 'image']


class LocationSerializer(serializers.HyperlinkedModelSerializer):
  nextVenueName = serializers.SerializerMethodField('get_venue_name')
  nextConcertId = serializers.SerializerMethodField('get_concert_id')
  nextArtistName = serializers.SerializerMethodField('get_artist_name')
  nextArtistId = serializers.SerializerMethodField('get_artist_id')

  def get_venue_name(self, obj):
    return self.context['nextVenueName']

  def get_concert_id(self, obj):
    return self.context['nextConcertId']
  
  def get_artist_name(self, obj):
    return self.context['nextArtistName']

  def get_artist_id(self, obj):
    return self.context['nextArtistId']
  class Meta:
    model = Location
    fields = ['id', 'city', 'country', 'population', 'timezone', 'region', 'area_code', 'elevation', 'image', 'nextVenueName', 'nextConcertId', 'nextArtistName', 'nextArtistId']

class VenueSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Venue
    fields = ['id', 'location', 'venue_address', 'parking_info', 'postal_code', 'image', 'venue_id']