
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
     path('',views.home, name="home"),
     path('room/<str:pk>/',views.room, name="room"),
      path('login/',views.loginPage, name="login"),
      path('logout/',views.logoutPage, name="logout"),
       path('register/',views.registerPage, name="register"),
     path('create-room/',views.createRoom, name="create-room"),
     path('update-room/<str:pk>/',views.updateRoom, name="update-room"),
     path('delete-room/<str:pk>/',views.deleteRoom, name="delete-room"),
      path('user/<str:pk>/',views.profilePage, name="profile"),
       path('deletemessage/<str:pk>/',views.deleteMessage, name="delete-message"),
       path('update-user/',views.updateUser, name="update-user"),
        path('topics/',views.browsetopics, name="topics"),
         path('activity/',views.activity, name="activity"),
]
