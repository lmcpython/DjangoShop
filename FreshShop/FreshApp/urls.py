from django.urls import path
from FreshApp.views import *
urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('index/', index),

]