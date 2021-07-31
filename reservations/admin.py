from reservations.models import Location, Reservation
from django.contrib import admin


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    model = Location


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    model = Reservation