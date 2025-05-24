# ad_generator_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('generate_ad/', views.generate_ad, name='generate_ad'),
    path('', views.home, name='home'),
]