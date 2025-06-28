from django.contrib import admin
from .models import RoomType,RoomType_Images,Amenity 
# Register your models here.

admin.site.register(RoomType_Images)
admin.site.register(RoomType)
admin.site.register(Amenity)