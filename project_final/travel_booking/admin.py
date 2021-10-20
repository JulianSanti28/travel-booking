from django.contrib import admin

# Administrar los modelos de la base de datos

from .models import User, Country, City, Airport,  Flight, Hotel, Room, Qualification, Reserved

#Register your models here.
class FlightAdmin(admin.ModelAdmin):
    list_display = ("__str__", "duration")

admin.site.register(User)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Airport)
admin.site.register(Flight, FlightAdmin)
admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(Qualification)
admin.site.register(Reserved)
#JSMT0528
#admin2021



