from django.urls import path
from . import views

urlpatterns = [
    path('u/<str:username>/getPositions/', views.getPositions, name='getPositions'),
    path('register/', views.register, name='register'),
    path('hello/', views.hello, name='hello'),
    ]
