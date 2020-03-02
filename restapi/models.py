from django.db import models

# Create your models here.
class Concert(models.Model):
    artist = models.ForeignKey(Artist, on_delete=CASCADE)
    venue = models.ForeignKey(Venue, on_delete=CASCADE)
    date = models.DateField()
    time = models.TimeField()

class Artist(models.Model):
    name = models.CharField(max_length=50)
    year_started = models.CharField(max_length=4)
    genre = models.CharField(max_length=50)
    top_song = models.CharField(max_length=100)
    bio = models.TextField()

class Location(models.Model):
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    population = models.IntegerField()

class Venue(models.Model):
    name = models.CharField(max_length=100)
    location = models.ForeignKey
    indoor = models.BooleanField()
    capacity = models.IntegerField()

class Album(models.Model):
    name = models.CharField(max_length=100)
    year = models.CharField(max_length=4)
    artist = models.ForeignKey(Artist, on_delete=CASCADE)
