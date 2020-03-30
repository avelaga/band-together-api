from rest_framework import serializers
from .models import Concert, Artist, Location, Venue

class ConcertSerializer(serializers.HyperlinkedModelSerializer):
  artistName = serializers.ReadOnlyField(source='artist.name')
  artistId = serializers.ReadOnlyField(source='artist.id')
  locationName = serializers.ReadOnlyField(source='location.city')
  locationId = serializers.ReadOnlyField(source='location.id')
  class Meta:
    model = Concert
    fields = ['artist', 'location', 'venue', 'date', 'time', 'ticket_min', 'ticket_max', 'artistName', 'locationName', 'artistId', 'locationId']

class ArtistSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Artist
    fields = '__all__' #uses all fields

class LocationSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Location
    fields = '__all__' #uses all fields

class VenueSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Venue
    fields = '__all__' #uses all fields
