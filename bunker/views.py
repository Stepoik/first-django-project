from django.shortcuts import render

def getPlayers(request,lobby):
    return render(request, 'games/bunker.html')
