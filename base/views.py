from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate, login,  logout
from .models import Room,Topic, Message 
from django.contrib.auth.forms import UserCreationForm 
from .forms import RoomForm, LoginForm,UserForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q


""" 
rooms =[
    {'id': 1, 'name':'Lets learn Python'},
    {'id': 2, 'name':'Lets learn c++'},
    {'id': 3, 'name':'Lets learn javascript'}
] """


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            username = loginform.cleaned_data['username'].lower()
            password = loginform.cleaned_data['password']
            try:
                user = User.objects.get(username = username )
            except:
                 messages.error(request, 'Username does not exist exist')

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect ('home')
        else:
            messages.error(request, 'Username OR Password does not match')
    else:
        loginform = LoginForm()

    context = {'loginform': loginform, 'page':page }
    return render (request,'base/login_register.html', context)

def logoutPage(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            messages.success(request, "Registration succesful")
            return redirect('home')
        else:
            messages.error(request, "Registration Error ")
    return render(request, 'base/login_register.html',{'form': form})



def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None  else ''
    
    rooms = Room.objects.filter(Q(topic__name__icontains = q) | 
    Q(name__icontains = q )|
    Q(description__icontains = q)
    ) 
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()

    room_messages = Message.objects.filter(Q(room__topic__name__icontains= q))
    context ={'rooms':rooms,
    'topics':topics,
    'room_count': room_count, 
    'room_messages': room_messages }

    return render(request,'base/home.html', context)

def room(request,pk):
    room = Room.objects.get(id=pk) 
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.method  == "POST": 
        addmessage = Message.objects.create(
            user = request.user,
            room = room ,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room' , pk = room.id)
    context= {'room':room, 'room_messages': room_messages, 'participants': participants}
    return render(request,'base/room.html', context)

@login_required(login_url = 'login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description '),
            )

        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request,'base/room_form.html',context)
    
@login_required(login_url = 'login')
def updateRoom(request, pk ):
    room = Room.objects.get(id = pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    
    if request.user != room.host:
        return HttpResponse ('You are not allowed Here')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic 
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context ={'form': form,'topics': topics, 'room' : room}
    return render(request,'base/room_form.html', context)

@login_required(login_url = 'login')
def deleteRoom(request, pk ):
    room = Room.objects.get(id =pk)
    if request.user != room.host:
        return HttpResponse ('You are not allowed Here')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html',{'obj': room })
    

@login_required(login_url = 'login')
def deleteMessage(request, pk ):
    message  = Message.objects.get(id =pk)

    if request.user != message.user:
        return HttpResponse ('You dont own this')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html',{'obj': message })
    

def profilePage(request, pk):
    user = User.objects.get(id = pk )
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects. all()
    context = {'user':user, 'rooms': rooms,'topics':topics ,'room_messages': room_messages}
    return render(request,'base/profile.html', context)


@login_required(login_url='login')
def updateUser(request):
    user = request.user 
    form = UserForm(instance=user)

    if request.method =='POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect ('profile', pk=user.id)
    return render(request, 'base/update_user.html', {'form': form})


def browsetopics(request):
    q = request.GET.get('q') if request.GET.get('q') != None  else ''
    topics = Topic.objects.filter(name__icontains = q)

    return render(request, 'base/topics.html', {'topics':topics})


def activity(request):
    room_messages = Message.objects.all()[0:4]
    context = {'room_messages':room_messages}
    return render(request, 'base/activity.html', context)