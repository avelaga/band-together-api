from rest_framework import serializers
from .models import Concert, Artist, Location, Venue

class ConcertSerializer(serializers.HyperlinkedModelSerializer):
  artistName = serializers.ReadOnlyField(source='artist.name')
  artistGenre = serializers.ReadOnlyField(source='artist.genre')
  artistId = serializers.ReadOnlyField(source='artist.id')
  locationName = serializers.ReadOnlyField(source='location.city')
  locationId = serializers.ReadOnlyField(source='location.id')
  artistImage = serializers.ReadOnlyField(source='artist.image')
  venueImage = serializers.ReadOnlyField(source='venue.image')
  venueName = serializers.ReadOnlyField(source='venue.name')
  
  class Meta:
    model = Concert
    fields = ['id', 'object_type', 'artist', 'location', 'venue', 'date', 'time', 'ticket_min', 'ticket_max', 'artistName', 'artistGenre', 'locationName', 'artistId', 'locationId', 'artistImage', 'venueImage', 'venueName']

class ArtistListSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Artist
    fields = ['id', 'object_type', 'name', 'popularity_score', 'genre', 'image', 'spotify_url', 'num_spotify_followers', 'website', 'twitter_url', 'wiki_url']

class ArtistSerializer(serializers.HyperlinkedModelSerializer):
  nextVenueName = serializers.SerializerMethodField('get_venue_name')
  nextConcertId = serializers.SerializerMethodField('get_concert_id')
  nextConcertDate = serializers.SerializerMethodField('get_concert_date')
  nextConcertTime = serializers.SerializerMethodField('get_concert_time')
  nextLocationName = serializers.SerializerMethodField('get_location_name')
  nextLocationId = serializers.SerializerMethodField('get_location_id')

  def get_venue_name(self, obj):
    return self.context['nextVenueName']

  def get_concert_id(self, obj):
    return self.context['nextConcertId']

  def get_concert_date(self, obj):
    return self.context['nextConcertDate']

  def get_concert_time(self, obj):
    return self.context['nextConcertTime']
  
  def get_location_name(self, obj):
    return self.context['nextLocationName']

  def get_location_id(self, obj):
    return self.context['nextLocationId']

  class Meta:
    model = Artist
    fields = ['id', 'name', 'popularity_score', 'genre', 'image', 'spotify_url', 'num_spotify_followers', 'website', 'twitter_url', 'wiki_url', 'nextVenueName', 'nextConcertId', 'nextConcertDate', 'nextConcertTime', 'nextLocationName', 'nextLocationId']


class LocationListSerializer(serializers.HyperlinkedModelSerializer):

  class Meta:
    model = Location
    fields = ['id', 'object_type', 'city', 'country', 'population', 'timezone', 'region', 'area_code', 'elevation', 'image']


class LocationSerializer(serializers.HyperlinkedModelSerializer):
  nextVenueName = serializers.SerializerMethodField('get_venue_name')
  nextConcertId = serializers.SerializerMethodField('get_concert_id')
  nextConcertDate = serializers.SerializerMethodField('get_concert_date')
  nextConcertTime = serializers.SerializerMethodField('get_concert_time')
  nextArtistName = serializers.SerializerMethodField('get_artist_name')
  nextArtistId = serializers.SerializerMethodField('get_artist_id')

  def get_venue_name(self, obj):
    return self.context['nextVenueName']

  def get_concert_id(self, obj):
    return self.context['nextConcertId']
  
  def get_concert_date(self, obj):
    return self.context['nextConcertDate']

  def get_concert_time(self, obj):
    return self.context['nextConcertTime']

  def get_artist_name(self, obj):
    return self.context['nextArtistName']

  def get_artist_id(self, obj):
    return self.context['nextArtistId']

  class Meta:
    model = Location
    fields = ['id', 'city', 'country', 'population', 'timezone', 'region', 'area_code', 'elevation', 'image', 'bio', 'nextVenueName', 'nextConcertId', 'nextConcertDate', 'nextConcertTime', 'nextArtistName', 'nextArtistId', 'lat', 'lon']

class VenueSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Venue
    fields = ['id', 'location', 'venue_address', 'parking_info', 'postal_code', 'image', 'venue_id', 'lat', 'lon']