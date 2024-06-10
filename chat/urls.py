from django.urls import path
from .views import  room, lobby


urlpatterns = [
    path('', lobby, name="lobby"),
    path("<str:room_name>/", room, name="room"),
]
