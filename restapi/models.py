from django.db import models

# Create your models here.

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

    def __str__(self):
        return self.name

class Location(models.Model):
    city = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    population = models.IntegerField(null=True)
    timezone = models.CharField(max_length=100, null=True)
    region = models.CharField(max_length = 100, null=True)
    area_code = models.CharField(max_length=3, null=True)
    elevation = models.IntegerField(null=True)
    image = models.URLField(null=True)

    def __str__(self):
        return self.city

class Venue(models.Model):
    name = models.CharField(max_length=100, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    venue_address = models.CharField(max_length=100, null=True)
    parking_info = models.CharField(max_length=500, null=True)
    postal_code = models.CharField(max_length=5, null=True)
    image = models.URLField(null=True)
    venue_id = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Concert(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, null=True)
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    concert_id = models.CharField(max_length=50, null=True)
    ticket_min = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    ticket_max = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return self.artist.name + " at " + self.venue.name

class Album(models.Model):
    name = models.CharField(max_length=100, null=True)
    year = models.CharField(max_length=4, null=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
