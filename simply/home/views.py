from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import Topic,Room,Message
from . forms import RoomForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User, auth


def home(request):
    q = request.GET.get('q') if request.GET.get('q') else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains = q)|
        Q(host__username__icontains = q)|
        Q(name__icontains = q)
    )
    rooms_count = rooms.count()
    topics = Topic.objects.all()
    context = {'rooms':rooms, 'topics':topics, 'rooms_count':rooms_count}
    return render(request, 'home/index.html', context)


def room(request,pk):
    room = Room.objects.get(id = pk)
    context = {'room':room}
    return render(request, 'home/room.html',context)


def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            new_room = form.save()
            messages.success(request, "Room Created Successfully!")
            return redirect('room', pk = new_room.pk)
    context = {'form':form}
    return render(request, 'home/room_create.html', context)


def updateRoom(request,pk):
    room = Room.objects.get(id = pk)
    if request.user != room.host:
        return HttpResponse("<h1>Forbidden 403!</h1>")
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, "Room Updated Successfully!")
            return redirect('room', pk = room.pk)
    context = {'form':form}
    return render(request, 'home/room_update.html', context)


def deleteRoom(request, pk):
    room = Room.objects.get(id = pk)
    if request.user != room.host:
        return HttpResponse("<h1>Forbidden</h1>")
    if request.method == 'POST':
        room.delete()
        messages.success(request, "Room Deleted Successfully!")
        return redirect('home')
    context = {'room':room}
    return render(request, 'home/room_delete.html', context)