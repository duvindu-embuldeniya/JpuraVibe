from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import Topic,Room,Message
from . forms import (
    RoomForm, UserRegistrationForm, MessageForm, UserUpdateForm, 
    ProfileUpdateForm
    )
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required




def home(request):
    q = request.GET.get('q') if request.GET.get('q') else ''

    # mens = User.objects.filter(
    #     Q(username__icontains = q)
    # )

    rooms = Room.objects.distinct().filter(
        Q(topic__name__icontains = q)|
        # Q(host__username__icontains = q)|
        Q(name__icontains = q)
        # Q(participants__in = mens)
        # or
        # Q(participants__username__icontains = q)
        # Q(description__icontains = q)
    )

    rooms_count = rooms.count()

    # topics = Topic.objects.all()
    topics = Topic.objects.all()[:5]
    # topics = Topic.objects.filter(
    #     Q(name__icontains = q)
    # )[:5]

    activities = Message.objects.all()
    # activities = Message.objects.filter(
    #     Q(room__topic__name__icontains = q)|
    #     Q(user__username__icontains = q)|
    #     Q(room__name__icontains = q)|
    #     Q(room__description__icontains = q)|
    #     Q(body__icontains = q)
    # )

    context = {'rooms':rooms, 'topics':topics, 'rooms_count':rooms_count, 'activities':activities}
    return render(request, 'home/index.html', context)




def login(request):
    if request.user.is_authenticated:
        messages.info(request, "You Have Already Loged-In!")
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        auth_user = auth.authenticate(username = username, password = password)
        if auth_user is not None:
            auth.login(request, auth_user)
            messages.success(request, "Successfully Loged-In!")
            return redirect('home')
            # need to adjust this to his profile
        else:
            messages.error(request, "User Doesn't Exist!")
            return redirect('login')
    return render(request, 'home/login.html')




def logout(request):
    if not(request.user.is_authenticated):
        messages.info(request, "You Have Not Loged-In!")
        return redirect('home')
    auth.logout(request)
    messages.success(request, "Successfully Loged Out!")
    return redirect('home')




def register(request):
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # new_user = form.save(commit=False)
            # new_user.username = new_user.username.lower()
            # new_user.save()
            new_user = form.save()
            messages.success(request, "Account Created Successfully!")
            auth.login(request, new_user)
            return redirect('home')
            # need to adjust this to his profile
    context = {'form':form}
    return render(request, 'home/register.html', context)



@login_required
def room(request,pk):
    room = Room.objects.get(id = pk)
    room_messages = room.message_set.all().order_by('-created')
    members = room.participants.all()

    if request.method == 'POST':
        new_msg = request.POST.get('body')

        if new_msg != '':
            Message.objects.create(
                user = request.user,
                room = room,
                body = new_msg
            )
            room.participants.add(request.user)
        return redirect('room', pk = room.id)

    context = {'room':room, 'room_messages':room_messages, 'members':members}
    return render(request, 'home/room.html',context)




@login_required
def createRoom(request):
    topics = Topic.objects.all()
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            new_room = form.save(commit=False)
            new_room.host = request.user

            topic_name = request.POST.get('topic')
            topic,created = Topic.objects.get_or_create(name = topic_name)
            new_room.topic = topic

            new_room.save()
            messages.success(request, "Room Created Successfully!")
            return redirect('room', pk = new_room.pk)
    context = {'form':form, 'topics':topics}
    return render(request, 'home/room_create.html', context)




@login_required
def updateRoom(request,pk):
    topics = Topic.objects.all()
    room = Room.objects.get(id = pk)
    current_topic = room.topic

    if request.user != room.host:
        return HttpResponse("<h1>Forbidden 403!</h1>")
    
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            alt_room = form.save(commit=False)

            topic_name = request.POST.get('topic')
            topic,created = Topic.objects.get_or_create(name = topic_name)
            alt_room.topic = topic

            alt_room.save()

            count = current_topic.room_set.all().count()
            if count == 0:
                current_topic.delete()

            messages.success(request, "Room Updated Successfully!")
            return redirect('room', pk = room.pk)
    context = {'form':form, 'room':room, 'topics':topics}
    return render(request, 'home/room_update.html', context)




@login_required
def deleteRoom(request, pk):
    room = Room.objects.get(id = pk)
    current_topic = room.topic

    if request.user != room.host:
        return HttpResponse("<h1>Forbidden 403!</h1>")
    
    if request.method == 'POST':
        room.delete()

        count = current_topic.room_set.all().count()
        if count == 0:
            current_topic.delete()

        messages.success(request, "Room Deleted Successfully!")
        return redirect('home')
    context = {'room':room}
    return render(request, 'home/room_delete.html', context)




# @login_required
# def updateMessage(request, pk):
#     msg = Message.objects.get(id = pk)
#     room = msg.room
#     if request.user != msg.user:
#         return HttpResponse("<h1>Forbidden 403!</h1>")
#     form = MessageForm(instance=msg)
#     if request.method == 'POST':
#         form = MessageForm(request.POST, instance=msg)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Message Updated Successfully!")
#             return redirect('room', pk = room.pk)
#     context = {'msg':msg, 'room':room, 'form':form}
#     return render(request, 'home/message_update.html', context)




@login_required
def deleteMessage(request, pk):
    msg = Message.objects.get(id = pk)
    room = msg.room
    current_user = request.user

    if request.user != msg.user:
        return HttpResponse("<h1>Forbidden 403!</h1>")
    if request.method == 'POST':
        msg.delete()

        count = Message.objects.filter(room = room, user = current_user).count()
        if count == 0:
            room.participants.remove(current_user)

        messages.success(request, "Message Deleted Successfully!")
        return redirect('room', pk = room.pk)
    context = {'msg':msg, 'room':room}
    return render(request, 'home/message_delete.html', context)




def profile(request, username):
    current_user = User.objects.get(username = username)
    rooms = current_user.room_set.all()
    # activities = current_user.message_set.all()
    activities = Message.objects.all()
    topics = Topic.objects.all()
    context = {'current_user':current_user, 'rooms':rooms, 'activities':activities, 'topics':topics}
    return render(request, 'home/profile.html', context)




@login_required
def profileUpdate(request, username):
    current_user = User.objects.get(username = username)
    if current_user != request.user:
        return HttpResponse("<h1>Forbidden 403!</h1>")
    form = UserUpdateForm(instance = current_user)
    p_form = ProfileUpdateForm(instance = current_user.profile)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=current_user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance = current_user.profile)
        if form.is_valid():
            # alt_user = form.save(commit=False)
            # alt_user.username = alt_user.username.lower()
            # alt_user.save()
            alt_user = form.save()
            p_form.save()
            messages.success(request, "Profile Updated Successfully!")
            return redirect('profile', username = alt_user.username)
    context = {'current_user':current_user, 'form':form, 'p_form':p_form}
    return render(request, 'home/profile_update.html', context)



@login_required
def profileDelete(request, username):
    current_user = User.objects.get(username = username)
    if request.user != current_user:
        return HttpResponse("<h1>Forbidden 403!</h1>")
    if request.method == 'POST':
        current_user.delete()
        messages.success(request, "Account Deleted Successfully!")
        return redirect('home')
    context = {'current_user':current_user}
    return render(request, 'home/profile_delete.html', context)



def topicView(request):
    q = request.GET.get('q') if request.GET.get('q') else ''
    topics = Topic.objects.filter(
        Q(name__icontains = q)
    )[:5]
    context = {'topics':topics}
    return render(request, 'home/topics.html', context)



def activityView(request):
    activities = Message.objects.all()
    context = {'activities':activities}
    return render(request, 'home/activity.html', context)