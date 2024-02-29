from django.urls import path

from . import views

urlpatterns = [
    path("MSM/login/", views.login, name="login"),
    path("MSM/logout/", views.logout, name="logout"),
]