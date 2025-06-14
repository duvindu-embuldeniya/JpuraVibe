from django.urls import path
from . views import *

urlpatterns = [
    path('', home, name = 'home'),

    path('login/', login, name = 'login'),
    path('logout/', logout, name = 'logout'),
    path('register/', register, name = 'register'),

    path('room/<int:pk>/', room, name = 'room'),
    path('create-room/', createRoom, name = 'create-room'),
    path('update-room/<int:pk>/', updateRoom, name = 'update-room'),
    path('delete-room/<int:pk>/', deleteRoom, name = 'delete-room'),

    # path('update-message/<int:pk>/', updateMessage, name = 'update-message'),
    path('delete-message/<int:pk>/', deleteMessage, name = 'delete-message'),

    path('profile/<str:username>/', profile, name = 'profile'),
    path('profile/<str:username>/update/', profileUpdate, name = 'profile-update'),
    path('profile/<str:username>/delete/', profileDelete, name = 'profile-delete'),

    path('topics/', topicView, name = 'topic-view'),
    path('activities/', activityView, name = 'activity-view'),
]