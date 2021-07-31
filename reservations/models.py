from django.core.exceptions import ValidationError
from reservations.constants import CITIES
from django.db import models
from django.utils.translation import gettext_lazy as _


class Location(models.Model):
    flat = models.CharField(max_length=200, )
    city = models.CharField(max_length=200, choices=CITIES)

    def __str__(self):
        return f"{self.flat} in {self.get_city_display()}"

    class Meta:
        ordering = ['city', 'flat']
        unique_together = ['flat', 'city']


class Reservation(models.Model):
    reservation = models.CharField(primary_key=True, max_length=7)
    checkin = models.DateField()
    checkout = models.DateField()
    income = models.FloatField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.reservation} - {self.checkin} to {self.checkout} at {self.location}. Total income: {self.income}"

    def clean(self):
        if self.checkin >= self.checkout:
            raise ValidationError(
                _("Checkout date must be higher than checkin date"))
        if self.income <= 0:
            raise ValidationError(
                _("Income must be higher than 0")
            )
            
    class Meta:
        ordering = ['checkin']
