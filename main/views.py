from django.shortcuts import render
from .models import Games

def main(request):
    return render(request, 'main.html', {'games':Games.objects.all()})
