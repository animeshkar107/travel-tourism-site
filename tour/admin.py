from django.contrib import admin
from .models import Destination, Package, Booking

admin.site.register(Destination)
admin.site.register(Package)
admin.site.register(Booking)