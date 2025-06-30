from django.db import models
from rooms.models import RoomType
from django.apps import apps  # Required for dynamic model lookup

class Meal(models.Model):
    date = models.DateField()
    meal_type = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('date', 'meal_type')

    def __str__(self):
        return f"{self.meal_type.capitalize()} on {self.date}"


class Booking(models.Model):
    category = models.ForeignKey(RoomType, null=True, on_delete=models.SET_NULL)

    check_in = models.DateField()
    check_out = models.DateField()

    meal_type = models.ForeignKey(Meal, null=True, on_delete=models.SET_NULL)
    no_of_days = models.IntegerField(null=True, blank=True, default=1)
    price_per_night = models.FloatField(default=0.0)
    no_of_room = models.IntegerField(default=1)

    # Use a string reference with proper related_name to avoid circular import & name clash
    payment = models.ForeignKey(
        'payment.Payment',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='booking_payment'
    )

    total_adults = models.IntegerField(default=1)
    total_children = models.IntegerField(default=0)

    def get_payment(self):
        Payment = apps.get_model('payment', 'Payment')
        return Payment.objects.filter(booking=self)

    def save(self, *args, **kwargs):
        self.no_of_days = (self.check_out - self.check_in).days
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking from {self.check_in} to {self.check_out}"
