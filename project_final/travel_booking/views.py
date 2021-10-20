# Now

import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, HttpResponseRedirect, render

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

# Imporar modelos

from .models import User, Country, City, Airport,  Flight, Hotel, Room, Qualification, Reserved

# Vistas de la aplicación

# Home


def index(request):
    # Obtener destinos y envíarlos al template Home
    destinos = get_cities()
    return render(request, "travel_booking/index.html", {"destinos": destinos})

# Login


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "travel_booking/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "travel_booking/login.html")

# Logout

# Cerrar sesión


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

# Registrar usuario


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "travel_booking/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "travel_booking/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "travel_booking/register.html")

# View City


def city(request, city_id):

    city = City.objects.get(pk=city_id)
    hoteles = city.hoteles.all()
    cantidad = len(hoteles)

    return render(request, "travel_booking/city.html", {"city": city, "hoteles": hoteles, "cantidad": cantidad})


def reserva(request):
    airports = Airport.objects.all()
    return render(request, "travel_booking/reserva.html", {"airports": airports})

# Return cities register in the data base


def get_cities():
    return City.objects.all()


@csrf_exempt
def filtro_vuelos_api(request):

    if request.method == 'POST':
        data = json.loads(request.body)
        origin = Airport.objects.get(pk=data.get("origin"))
        destination = Airport.objects.get(pk=data.get("destination"))

        if(data.get("filter")):
            vuelos_ida = Flight.objects.filter(
                origin=origin, destination=destination).all()
            return JsonResponse({"message": "Correcto", "vuelos_ida": [vuelo.serialize() for vuelo in vuelos_ida]}, status=201)
        else:
            vuelos_ida = Flight.objects.filter(
                origin=origin, destination=destination).all()
            vuelos_regreso = Flight.objects.filter(
                origin=destination, destination=origin).all()

            return JsonResponse({"vuelos_ida": [vuelo.serialize() for vuelo in vuelos_ida], "vuelos_regreso": [vuelo.serialize() for vuelo in vuelos_regreso]}, status=201)
