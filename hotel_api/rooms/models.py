from django.db import models
from hotels.models import Hotel
# Create your models here.

class RoomType_Images(models.Model):
    image = models.ImageField(upload_to='room_images/')

class Amenity(models.Model):
    name = models.CharField(max_length=128, unique=True)
    image = models.ImageField(upload_to="amenity/", blank=True, null=True)
    is_available = models.BooleanField(default=True)
    availability_start = models.DateTimeField(null=True, blank=True)
    availability_end = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class RoomType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    capacity = models.IntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ManyToManyField(RoomType_Images)
    amenities = models.ManyToManyField(Amenity)

    def __str__(self):
        return f"{self.name}"

