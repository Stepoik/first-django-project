from django.shortcuts import render
from django.http import JsonResponse
from .models import Players, Specifications, Game
from django.contrib.sessions.models import Session
import time

def index(request,lobby):
    print(request.session.session_key)
    if request.session.session_key == None:
        request.session.save()
    return render(request, 'games/bunker.html')


def getplayers(request, lobby):
    root = False
    players = Players.objects.filter(lobby = lobby,online = True)
    player = Players.objects.filter(lobby = lobby, session = request.session.session_key)
    if len(Game.objects.filter(lobby = lobby)) == 0:
        root = True
        game = Game(lobby = lobby, start = False)
        game.save()
    else:
        game = Game.objects.get(lobby = lobby)
    if len(player) > 0:
        if player[0].play == True:
            try:
                player[0].queue = players.order_by('-queue')[0].queue+1
            except:
                player[0].queue = 1
        root = player[0].root
        inlobby = True
        self_specs = {spec.name_spec: spec.spec for spec in Specifications.objects.filter(player = player[0])}
        play = player[0].play
        player[0].online = True
        player[0].save()
    else:
        inlobby = False
        play = False
        self_specs = None
    bunker = {'pop':game.bunker_pop,
              'kata':game.bunker_kata,
              'time':game.bunker_time,
              'size':game.bunker_size}
    return JsonResponse({'players': [{'id':playerfor.id_user, 'name':playerfor.name, 'play':playerfor.play} for playerfor in Players.objects.filter(lobby = lobby, online = True).order_by('queue')],
                         'self_specs': self_specs,
                         'all_specs': list({'spec':x.spec, 'player':x.player.id_user} for x in Specifications.objects.filter(lobby = lobby, open = True) if x.player.online),
                         'play':play,
                         'root': root,
                         'inlobby':inlobby,
                         'session':request.session.session_key,
                         'start': game.start,
                         'bunker':bunker})