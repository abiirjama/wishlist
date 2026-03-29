#views for handling place actions
from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden


#view for listing places and adding a new place
@login_required
def place_list(request):

    #if form submitted (POST request)
    if request.method == 'POST':
        form = NewPlaceForm(request.POST)
        place = form.save(commit=False)

        #attach current user to the place
        place.user = request.user  

        #validate and save
        if form.is_valid():
            place.save()
            return redirect('place_list')

    #get unvisited places for current user
    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')

    #empty form for new place
    form = NewPlaceForm()

    return render(request, 'travel_wishlist/wishlist.html', {
        'places': places,
        'new_place_form': form
    })


#view for showing visited places
@login_required
def places_visited(request):
    visited = Place.objects.filter(user=request.user).filter(visited=True).order_by('name')
    return render(request, 'travel_wishlist/visited.html', {'visited': visited})


#mark a place as visited
@login_required
def place_was_visited(request, place_pk):
    if request.method == 'POST':
        place = get_object_or_404(Place, pk=place_pk)

        #only allow owner to update
        if place.user == request.user:
            place.visited = True   
            place.save()
        else:
            return HttpResponseForbidden()
    
    return redirect('place_list')


#delete a place
@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)

    #only allow owner to delete
    if place.user == request.user:
        place.delete()
        return redirect('place_list')
    else:
        return HttpResponseForbidden() 


#view for place details and updating review
@login_required
def place_details(request, place_pk):

    place = get_object_or_404(Place, pk=place_pk)

    #block access if not owner
    if place.user != request.user:
        return HttpResponseForbidden()

    #handle form submission
    if request.method == 'POST':
        form = TripReviewForm(request.POST, request.FILES, instance=place)

        #validate and save form
        if form.is_valid():
            form.save()
            messages.info(request, 'Trip information updated!')
        else:
            messages.error(request, form.errors)

        return redirect('place_details', place_pk=place_pk)

    else:
        #if place visited, show review form
        if place.visited:
            review_form = TripReviewForm(instance=place)
            return render(request, 'travel_wishlist/place_detail.html', {
                'place': place,
                'review_form': review_form
            })

        #if not visited, just show details
        else:
            return render(request, 'travel_wishlist/place_detail.html', {
                'place': place
            })