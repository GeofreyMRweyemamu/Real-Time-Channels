from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
import cv2
import time
from django.views.decorators import gzip

# Create your views here.

def lobby(request):
    return render(request,"chat/index.html")

def room(request, room_name):
    return render(request,"chat/room.html", {"room_name": room_name})
