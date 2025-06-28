from django.db import models

# Create your models here.

class Hotel_Image(models.Model):
    image = models.ImageField(upload_to='hotel_images/')
    
class Hotel(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    images = models.ForeignKey(Hotel_Image,on_delete=models.SET_NULL,null=True)
    def __str__(self):
        return self.name

# class Guest(models.Model):
#     f_name = models.CharField(max_length=50,null=True,blank=True)
#     l_name = models.CharField(max_length=50,null=True,blank=True)
#     email = models.EmailField()
#     phone_no = models.CharField(max_length=12,null=True,blank=True)
#     created_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         verbose_name = 'GUEST'

#     def __str__(self):
#         return f"{self.f_name}Â {self.l_name}"