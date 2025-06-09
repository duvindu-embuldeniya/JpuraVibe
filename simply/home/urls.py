from django.urls import path
from . views import *

urlpatterns = [
    path('', home, name = 'home'),
    path('rooms/<int:pk>/', room, name = 'room'),
    path('create-room', createRoom, name = 'create-room'),
]