from django.contrib.auth.models import AbstractUser
from django.db import models

# Estado de la habitacion
STATE_CHOICES = (
    ('RESERVED', 'RESERVED'),
    ('NOT_RESERVERD', 'NOT_RESERVED')

)

# Modelos para mi aplicación

# Entidad User


class User(AbstractUser):
    pass

# Entidad País


class Country(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.code} ({self.name})"

# Entidad Ciudad


class City(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=30)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="ciudades")
    imagen = models.ImageField(upload_to='destinos-image', null=True)
    description = models.CharField(max_length=300)

    def __str__(self):
        return f"[{self.name}] UBICADO EN:  [{self.country.name}]"

# Entidad Aeropuerto


class Airport(models.Model):
    code = models.CharField(max_length=6)
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name="ciudades_airport")

    def __str__(self):
        return f"{self.city.name} ({self.code})"

    def serialize(self):
        return {
            "id": self.code,
            "city_code": self.city.code,
            "city_name": self.city.name,
            "country": self.city.country.name
        }


# Entidad vuelo


class Flight(models.Model):
    price = models.FloatField()
    origin = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="arrivals")
    duration = models.IntegerField()
    capacity = models.IntegerField()

    def __str__(self):
        return f"{self.origin} TO {self.destination} -> {self.duration}"

    def serialize(self):
        return {
            "id": self.id,
            "origin": self.origin.serialize(),
            "destination": self.destination.serialize(),
            "price": self.price,
            "duration": self.duration,
            "capacity": self.capacity
        }

# Entidad Hotel


class Hotel(models.Model):

    city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name="hoteles")
    name = models.CharField(max_length=30)
    imagen = models.ImageField(upload_to='destinos-image', null=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} IN {self.city.name}"


# Entidad Calificacion


class Qualification(models.Model):
    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE, related_name="hoteles_calificados")
    usuario = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="calificados")
    qualification = models.IntegerField()
    description = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)

# Entidad Reserva


class Reserved(models.Model):
    usuario = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="reservas_usuario")
    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE, related_name="reservas_hotel")
    flight = models.ForeignKey(
        Flight, on_delete=models.CASCADE, related_name="reservas_vuelo")
    fecha = models.DateTimeField(auto_now_add=True)
    price = models.FloatField()

# Entidad Habitacion


class Room(models.Model):
    price = models.FloatField()
    beds = models.IntegerField()
    bathroom = models.IntegerField()
    state = models.CharField(
        max_length=20, choices=STATE_CHOICES, default='DISPO')
    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE, related_name="habitaciones_hotel")
    reserved_by = models.ForeignKey(
        Reserved, on_delete=models.CASCADE, blank=True, related_name="habitaciones_reserva")
