from django.contrib import admin
from django.urls import path, include
import alias.views as views

urlpatterns = [
    path('', views.redirection),
    path('<str:lobby>/',views.main, name= 'main'),
    path('<str:lobby>/getInfo/', views.getInfo),
    path('<str:lobby>/changeTeam/', views.changeTeam),
    path('<str:lobby>/startGame/', views.startGame),
    path('<str:lobby>/createTeam/', views.createTeam),
    path('<str:lobby>/delplayer/',views.delPlayer),
    path('<str:lobby>/ready/', views.getReady),
    path('<str:lobby>/next/', views.nextWord),
    path('<str:lobby>/changeStatus/', views.changeStatus),
    path('<str:lobby>/send/', views.send)
]