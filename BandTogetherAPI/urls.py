"""BandTogetherAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from restapi import views as restapiviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('restapi/artist', restapiviews.ArtistList.as_view(), name='artist-list'),
    path('restapi/location', restapiviews.LocationList.as_view(), name='location-list'),
    path('restapi/concert', restapiviews.ConcertList.as_view(), name='concert-list'),
    path('restapi/venue', restapiviews.VenueList.as_view(), name='venue-list'),
    path('restapi/artist/<int:pk>', restapiviews.ArtistDetail.as_view(), name='artist-detail'),
    path('restapi/location/<int:pk>', restapiviews.LocationDetail.as_view(), name='location-detail'),
    path('restapi/concert/<int:pk>', restapiviews.ConcertDetail.as_view(), name='concert-detail'),
    path('restapi/venue/<int:pk>', restapiviews.VenueDetail.as_view(), name='venue-detail')
]
