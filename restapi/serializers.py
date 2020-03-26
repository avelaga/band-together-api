from rest_framework import serializers
from .models import Concert, Artist, Location, Album, Venue

class ConcertSerializer(serializers.ModelSerializer):
  class Meta:
    model = Concert
    fields = '__all__' #uses all fields

class ArtistSerializer(serializers.ModelSerializer):
  class Meta:
    model = Artist
    fields = '__all__' #uses all fields

class LocationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Location
    fields = '__all__' #uses all fields

class AlbumSerializer(serializers.ModelSerializer):
  class Meta:
    model = Album
    fields = '__all__' #uses all fields

class VenueSerializer(serializers.ModelSerializer):
  class Meta:
    model = Venue
    fields = '__all__' #uses all fields