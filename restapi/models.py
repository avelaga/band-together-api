from django.db import models

# Create your models here.
class Concert(models.Model):
    artist = models.ForeignKey(Artist, on_delete=CASCADE, null=True)
    venue = models.ForeignKey(Venue, on_delete=CASCADE, null=True)
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    location = models.ForeignKey(Location)

class Artist(models.Model):
    name = models.CharField(max_length=50, null=True)
    popularity_score = models.IntegerField(null=True)
    genre = models.CharField(max_length=50, null=True)
    image = models.URLField(null=True)
    spotify_url = models.URLField(null=True)
    num_spotify_followers = models.IntegerField(null=True)
    website = models.URLField(null=True)
    twitter_url = models.URLField(null=True)
    wiki_url = models.URLField(null=True)

class Location(models.Model):
    city = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    population = models.IntegerField(null=True)
    timezone = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length = 100, null=True)
    area_code = models.CharField(max_length=3, null=True)
    elevation = models.IntegerField(null=True)
    image = models.URLField(null=True)


class Venue(models.Model):
    name = models.CharField(max_length=100, null=True)
    location = models.ForeignKey(Location, on_delete=CASCADE, null=True)
    capacity = models.IntegerField()
    venue_address = CharField(max_length=100, null=True)
    parking_info = CharField(max_length=500, null=True)

class Album(models.Model):
    name = models.CharField(max_length=100, null=True)
    year = models.CharField(max_length=4, null=True)
    artist = models.ForeignKey(Artist, on_delete=CASCADE, null=True)
