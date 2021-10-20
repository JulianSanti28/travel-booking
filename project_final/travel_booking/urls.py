from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("city/<int:city_id>", views.city, name="city"),
    path("reserva", views.reserva, name="reserva"),
    path("vuelos", views.filtro_vuelos_api, name="vuelos"),
]