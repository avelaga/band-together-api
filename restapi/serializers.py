from rest_framework import serializers
from .models import Concert, Artist, Location, Venue

class ConcertSerializer(serializers.HyperlinkedModelSerializer):
  artistName = serializers.ReadOnlyField(source='artist.name')
  locationName = serializers.ReadOnlyField(source='location.city')
  class Meta:
    model = Concert
    fields = ['artist', 'location', 'venue', 'date', 'time', 'ticket_min', 'ticket_max', 'artistName', 'locationName']

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

    # artist = models.ForeignKey(Artist, on_delete=models.CASCADE, null=True)
    # location = models.ForeignKey(Location, on_delete=models.CASCADE)
    # venue = models.ForeignKey(Venue, on_delete=models.CASCADE, null=True)
    # date = models.DateField(null=True)
    # time = models.TimeField(null=True)
    # concert_id = models.CharField(max_length=50, null=True)
    # ticket_min = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    # ticket_max = models.DecimalField(max_digits=10, decimal_places=2, null=True)