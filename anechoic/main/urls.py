from django.urls import path
from . import views

urlpatterns = [
    path('getPositions/', views.getPositions, name='getPositions'),
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('hello/', views.hello, name='hello'),
    ]
