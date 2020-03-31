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

class ArtistSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Artist
    fields = ['id', 'name', 'popularity_score', 'genre', 'image', 'spotify_url', 'num_spotify_followers', 'website', 'twitter_url', 'wiki_url']

class LocationSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Location
    fields = ['id', 'city', 'country', 'population', 'timezone', 'region', 'area_code', 'elevation', 'image']

class VenueSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Venue
    fields = ['id', 'location', 'venue_address', 'parking_info', 'postal_code', 'image', 'venue_id']