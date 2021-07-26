from django.contrib import admin
from django.urls import path, include
import alias.views as views

urlpatterns = [
    path('alias/<str:lobby>',views.Monopoly, name= 'alias'),
    # path('addcontact/', views.addContact,name = 'add'),
    # path('sessionControl/', views.controlSession),
    # path('delContact/<str:lobby>', views.delUser),
    # path('gameStart', views.gameProcess),
    # path('gameGo/', views.gameGo)
    path('alias/getInfo/<str:lobby>', views.getInfo),
    path('alias/changeTeam/<str:lobby>', views.changeTeam),
    path('alias/startGame/<str:lobby>', views.startGame),
    path('alias/createTeam/<str:lobby>', views.createTeam),
    path('alias/delplayer/<str:lobby>',views.delPlayer),
    path('alias/ready/<str:lobby>', views.getReady),
    path('alias/next/<str:lobby>', views.nextWord),
    path('alias/changeStatus/<str:lobby>', views.changeStatus),
    path('alias/send/<str:lobby>', views.send)
]