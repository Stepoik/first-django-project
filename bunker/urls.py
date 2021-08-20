from django.urls import path
from . import views

urlpatterns = [
    path('<str:lobby>/', views.index),
    path('<str:lobby>/getplayers/', views.getplayers)
]