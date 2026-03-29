#imports for forms and widgets
from django import forms
from django.forms import FileInput, DateInput
from .models import Place

#form for adding a new place
class NewPlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('name', 'visited')


#create a custom date input field,otherwise would get a plain text field
#change input type from text to date
class DateInput(forms.DateInput):
    input_type = 'date'  #override default input type which is text


#form for trip review (notes,date and photo)
class TripReviewForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('notes', 'date_visited', 'photo')
        widgets = {
            'date_visited': DateInput()
        }