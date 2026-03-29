#import models, user and storage
from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage


#model for a place
class Place(models.Model):
    #link each place to a user
    user = models.ForeignKey('auth.User', null=False, on_delete=models.CASCADE)
    
    #place name
    name = models.CharField(max_length=200)
    
    #whether the place was visited
    visited = models.BooleanField(default=False)
    
    #notes about the place
    notes = models.TextField(blank=True, null=True)
    
    #date when the place was visited
    date_visited = models.DateField(blank=True, null=True)
    
    #photo upload field
    photo = models.ImageField(upload_to='user_images/', blank=True, null=True)


    #override save method to handle photo updates
    def save(self, *args, **kwargs):
        #get previous version of this place
        old_place = Place.objects.filter(pk=self.pk).first()
        
        #if photo changed, delete old photo
        if old_place and old_place.photo:
            if old_place.photo != self.photo:
                self.delete_photo(old_place.photo)

        #save normally
        super().save(*args, **kwargs)
            

    #override delete method to remove photo from storage
    def delete(self, *args, **kwargs):
        #delete photo if exists
        if self.photo:
            self.delete_photo(self.photo)

        #delete object
        super().delete(*args, **kwargs)

    
    #helper function to delete photo file
    def delete_photo(self, photo):
        #check if file exists in storage
        if default_storage.exists(photo.name):
            default_storage.delete(photo.name)


    #string representation of object
    def __str__(self):
        photo_str = self.photo.url if self.photo else 'no photo'
        return f'{self.pk}: {self.name} visited? {self.visited} on {self.date_visited}\nPhoto {photo_str}'