from django.db import models
from payment.models import Payment
# Create your models here.

class Meal(models.Model):
    date = models.DateField()
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    class Meta:
        unique_together = ('date', 'meal_type')

    def __str__(self):
        return f"{self.meal_type.capitalize()} on {self.date}"

class Booking(models.Model):
    category = models.ForeignKey(
        'hotel.Room_Category', null=True, on_delete=models.SET_NULL)

    check_in = models.DateField()
    check_out = models.DateField()

    meal_type = models.ForeignKey(
        Meal_Type, null=True, on_delete=models.SET_NULL)
    no_of_days = models.IntegerField(null=True, blank=True, default=1)
    price_per_night = models.FloatField(default=0.0)
    no_of_room = models.IntegerField(default=1)
    payment = models.ForeignKey('payment.Payment', on_delete=models.SET_NULL,
                                null=True, blank=True, related_name='booking_payment')

    total_adults = models.IntegerField(default=1)
    total_children = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.no_of_days = (self.check_out-self.check_in).days
        # print(self.no_of_days)
        super().save(*args, **kwargs)

