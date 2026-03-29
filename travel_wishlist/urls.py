#url patterns for place-related views
from django.urls import path
from . import views

urlpatterns = [
    #home page - list all places
    path('', views.place_list, name='place_list'),

    #list of visited places
    path('visited', views.places_visited, name='places_visited'),

    #mark a place as visited
    path('place/<int:place_pk>/was_visited', views.place_was_visited, name='place_was_visited'),

    #show details of a specific place
    path('place/<int:place_pk>', views.place_details, name='place_details'),

    #delete a place
    path('place/<int:place_pk>/delete', views.delete_place, name='delete_place'),
]