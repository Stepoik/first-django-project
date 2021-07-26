from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.db import connection
from .models import Alias, Teams, Games, Words
from django.contrib.sessions.models import Session
from datetime import datetime, timedelta, timezone
import random
import string

def Monopoly(request, lobby):
    return render(request, 'games/monopoly.html')
# def getPlayer(lobby):
#      output = {}
#      for team in Teams.objects.filter(lobby = lobby):
#           output[team.Team] = 'team'
#      for player in Alias.objects.filter(lobby = lobby):
#           output[player.session] = [player.team,player.name]
#      game = Games.objects.get(lobby = lobby)
#      output['game'] = game.start
#      output['ready'] = game.round
#      return output
# def addContact(request):
#      controlSession(request)
#      if request.GET.get('getInfo'):
#           return getInfo(request, request.GET.get('url'))
#      url = request.GET.get('url')
#      if (Games.objects.filter(lobby = url)) == 0:
#           return HttpResponse('end')
#      name = request.GET.get('name')
#      if name == '':
#           name = 'name'
#
#      root = request.GET.get('root')
#      team = request.GET.get('team')
#      print(team)
#      session = request.session.get('self')
#      request.session['team'] = team
#      request.session['root'] = root
#      if len(Alias.objects.filter(session = session, lobby = url)) == 0:
#           new_user = Alias(name = name, root = root, team = team, session = session, lobby = url, ready = 'false')
#           new_user.save()
#      if len(Teams.objects.filter(lobby = url, Team = team)) == 0:
#           Team = Teams(Team = team, lobby = url, score = 0, player_quest = 0)
#           Team.save()
#      self_player = Alias.objects.get(session = session, lobby = url)
#      self_player.name = name
#      self_player.team = team
#      self_player.save()
#      delTeam(url)
#      return JsonResponse(getPlayer(url))
# def controlSession(request):
#      respounse = False
#      request.session.clear_expired()
#      if request.session.session_key == None:
#           request.session.save()
#           respounse = True
#      return JsonResponse({'answ':respounse})
# def getInfo(request, lobby):
#      root = request.session.get('root')
#      if len(Alias.objects.filter(lobby = lobby)) == 0:
#           root = 'true'
#           newGame(lobby)
#      if request.session.get('self','None') == 'None':
#           request.session['self'] = request.GET.get('session')
#      return JsonResponse({'session': request.session.get('self', 'None'), 'team':request.session.get('team', 'spect'), 'root':root, 'game':Games.objects.get(lobby = lobby).start})
# def delUser(request, lobby):
#      print('del')
#      session = request.session['self']
#      player = Alias.objects.get(session = session, lobby =lobby)
#      player.delete()
#      delTeam(lobby)
#      request.session.delete()
#      delGame(lobby)
#      for word in Words.objects.all():
#           word.delete()
#      return HttpResponse('end')
# def delTeam(lobby):
#      for team in Teams.objects.filter(lobby = lobby):
#           if len(Alias.objects.filter(lobby = lobby, team = team.Team)) == 0 and team.Team!='spect':
#                team.delete()
# def delGame(lobby):
#      if len(Alias.objects.filter(lobby = lobby)) == 0:
#           Teams.objects.get(lobby = lobby).delete()
#           game = Games.objects.get(lobby = lobby)
#           game.delete()
# def newGame(lobby):
#      game = Games(lobby = lobby, start = 'false',queue = 1, round = 'false')
#      game.save()
# def gameProcess(request):
#      lobby = request.GET.get('lobby')
#      game = Games.objects.get(lobby = lobby)
#      ready = 'false'
#      print(Games.objects.get(lobby = lobby).queue, Teams.objects.filter(lobby = lobby))
#      team = Teams.objects.filter(lobby = lobby)[Games.objects.get(lobby = lobby).queue].Team
#      if game.start == 'false':
#           game.start = 'true'
#      game.save()
#      index_questor = Teams.objects.get(lobby = lobby, Team = team).player_quest
#      questor = Alias.objects.filter(lobby = lobby,team = team)[index_questor]
#      if index_questor == len(Alias.objects.filter(lobby = lobby,team = team)) - 1:
#           answer = Alias.objects.filter(lobby = lobby,team = team)[0]
#      else:
#           answer = Alias.objects.filter(lobby = lobby,team = team)[index_questor+1]
#      game = Games.objects.get(lobby=lobby)
#      if questor.ready == 'true' and answer.ready == 'true' and game.round == 'false':
#           game.round = 'true'
#           ready = 'true'
#           questor.ready = 'false'
#           answer.ready = 'false'
#           print('lol')
#           game.roundend = datetime.now(timezone.utc)+timedelta(minutes=1)
#           if len(Words.objects.filter(lobby = lobby)) == 0:
#                appendWord(lobby)
#      if questor.session == request.session['self']:
#           questor.ready = request.GET.get('selfReady')
#      if answer.session == request.session['self']:
#           answer.ready = request.GET.get('selfReady')
#      game.save()
#      questor.save()
#      answer.save()
#      return JsonResponse({'questor':questor.session, 'answer':answer.session, 'ready':ready})
# def gameGo(request):
#      lobby = request.GET.get('lobby')
#      if request.GET.get('next') == 'true':
#           appendWord(lobby)
#      team = Teams.objects.filter(lobby=lobby)[Games.objects.get(lobby=lobby).queue].Team
#      index_questor = Teams.objects.get(lobby=lobby, Team=team).player_quest
#      questor = Alias.objects.filter(lobby=lobby, team=team)[index_questor].session
#      if questor == request.session.get('self'):
#           print('here')
#           words = Words.objects.filter(lobby = lobby)
#      else:
#           words = Words.objects.filter(lobby = lobby)
#           words = words[:len(words)-1]
#      words = list(map(lambda x: x.word, words))
#      time = int((Games.objects.get(lobby = lobby).roundend - datetime.now(timezone.utc)).total_seconds())
#      print(int(time))
#      return JsonResponse({'time': time,'words':words})
# def appendWord(lobby):
#      cursor = connection.cursor()
#      cursor.execute('''
#                          select * from words''')
#      word = random.choice(cursor.fetchall())
#      Words(word=word, lobby=lobby).save()
def send(request,lobby):
     if request.is_ajax():
          game = Games.objects.get(lobby = lobby)
          team = Teams.objects.filter(lobby=lobby)[game.queue]
          team.score += len(Words.objects.filter(lobby = lobby, status = 'true'))
          roundNext(lobby, game)
          team.save()
          return HttpResponse('scoring')
def changeStatus(request, lobby):
     if request.is_ajax():
          word = Words.objects.filter(lobby = lobby, word = request.GET.get('word'))[0]
          if word.status == 'false':
               word.status = 'true'
          else:
               word.status = 'false'
          word.save()
          return HttpResponse('changeWord')
def delWords(lobby):
     Words.objects.filter(lobby = lobby).delete()
def roundNext(lobby,game):
     game.round = 'false'
     team = Teams.objects.filter(lobby = lobby)[game.queue]
     team.player_quest += 1
     if team.player_quest == len(Alias.objects.filter(lobby = lobby, team = team.team)):
          team.player_quest = 0
     if game.queue == len(Teams.objects.filter(lobby = lobby))-1:
          game.queue = 0
     else:
          game.queue = game.queue +1
     team.save()
     game.save()
     delWords(lobby)
def nextWord(request, lobby):
     if request.is_ajax():
          cursor = connection.cursor()
          cursor.execute('''
          select * from words''')
          newWord =random.choice(cursor.fetchall())[0]
          print(newWord)
          Words(lobby = lobby, word = newWord, status = 'false').save()
          return HttpResponse('addWord')
def getReady(request, lobby):
     player = Alias.objects.get(lobby = lobby, session = request.session.get('self'))
     if player.ready == 'true':
          player.ready = 'false'
     else:
          player.ready ='true'
     player.save()
     return HttpResponse('ready')
def delTeam(lobby):
     for team in list(map(lambda x:x.team, Teams.objects.filter(lobby = lobby))):
          if len(Alias.objects.filter(lobby = lobby, team = team)) == 0:
               Teams.objects.get(lobby = lobby, team = team).delete()
def createTeam(request, lobby): #create new team
     if request.is_ajax():
          print(request.session.get('team'))
          if len(Alias.objects.filter(lobby = lobby, team = request.session.get('team'))) > 1 or request.session.get('team') == 'spect':
               team = getSessionTeam(formatpass=7)
               Teams(team = team, lobby = lobby,score = 0,player_quest = 0).save()
               player = Alias.objects.get(lobby = lobby, session = request.session.get('self'))
               player.team = team
               request.session['team'] = team
               player.save()
          return HttpResponse('create')
def getWords(request, lobby,game): #Get all words and questor/answer
     teamIndex = Games.objects.get(lobby=lobby).queue
     questIndex = Teams.objects.filter(lobby = lobby)[teamIndex]
     questor = Alias.objects.filter(lobby = lobby, team = questIndex.team)[questIndex.player_quest] #get questor
     questorSes = questor.session
     questorReady = questor.ready
     if questIndex.player_quest == len(Alias.objects.filter(lobby = lobby, team = questIndex.team)) - 1: # get answer
          answer = Alias.objects.filter(lobby = lobby, team = questIndex.team)[0]
     else:
          answer = Alias.objects.filter(lobby = lobby, team = questIndex.team)[questIndex.player_quest+1]
     answerSes = answer.session
     answerReady = answer.ready
     words = list(map(lambda x: [x.word, x.status], Words.objects.filter(lobby=lobby))) #get words
     playerQuestor = 'false'
     playerAnsw = 'false'
     if request.session.get('self') == answerSes:
          playerAnsw = 'true'
     if request.session.get('self') != questorSes:
          words = words[:len(words)-1]
     else:
          playerQuestor = 'true'
     if questorReady == 'true' and answerReady == 'true': #gameready check
          game = Games.objects.get(lobby = lobby)
          questor.ready = 'false'
          answer.ready = 'false'
          game.round = 'true'
          game.roundend = datetime.now(timezone.utc)+timedelta(minutes=1)
          game.save()
     questor.save()
     answer.save()
     return words,[questorSes, questorReady, playerQuestor],[answerSes, answerReady, playerAnsw]
def delPlayer(request, lobby): #delete player
     Alias.objects.get(lobby = lobby, session = request.session.get('self')).delete()
     delTeam(lobby)
     if len(Teams.objects.filter(lobby = lobby)) == 0:
          Games.objects.get(lobby = lobby).delete()
          delWords(lobby)
     return HttpResponse('delete')
def startGame(request,lobby): # start game
     game = Games.objects.get(lobby = lobby)
     game.start = 'true'
     game.save()
     return HttpResponse('start')
def changeTeam(request, lobby): #change users team
     if request.is_ajax() and Games.objects.get(lobby = lobby).start == 'false':
          newTeam = request.GET.get('team')
          request.session['team'] = newTeam
          player = Alias.objects.get(lobby = lobby, session = request.session.get('self'))
          player.team = newTeam
          player.save()
          return HttpResponse('change')
def getInfo(request, lobby): #main function
     if request.is_ajax() and request.GET.get('close') == 'false':
          print(request.path)
          try:
               game = Games.objects.get(lobby = lobby)
          except:
               createGame(lobby)
               game = Games.objects.get(lobby = lobby)
          try:
               player = Alias.objects.get(lobby = lobby, session = request.session.get('self'))
          except:
               player = createPlayer(request, lobby)
          delTeam(lobby)
          name = request.GET.get('name')
          print(name)
          if name == '':
               name = 'name'
          player.name = name
          player.save()
          session = request.session.get('self')
          root = request.session.get('root')
          players = list(map(lambda x: [x.name, x.team,x.session],Alias.objects.filter(lobby = lobby)))
          teams = list(map(lambda x: x.team, Teams.objects.filter(lobby = lobby)))
          data = {'start': game.start, 'session':session,'players':players, 'teams':teams, 'ready':game.round, 'root':root}
          if game.round == 'true':
               timer = int((game.roundend - datetime.now(timezone.utc)).total_seconds())
               data['timer'] = timer
               if timer <= 0:
                    data['wordspress'] = 'true'
          if game.start == 'true':
               words = getWords(request, lobby,game)
               data['words'] = words[0]
               data['questor'] =words[1]
               data['answer'] = words[2]
          return JsonResponse(data)
def createGame(lobby): #create game
     Games(lobby = lobby, start = 'false', queue =0, round = 'false').save()
def createPlayer(request, lobby): #create player
     root = 'false'
     if len(Alias.objects.filter(lobby = lobby)) == 0:
          root = 'true'
     request.session['root'] = root
     request.session['self'] = getSessionTeam(formatpass=6)
     request.session['team'] = 'spect'
     player = Alias(name = request.GET.get('name', 'name'),root = root, lobby = lobby, team = request.session.get('team'),session = request.session.get('self'), ready = 'false')
     player.save()
     return player
def getSessionTeam(formatpass = 6): #get code
     cod = ''
     cod+=random.choice(list(string.ascii_lowercase))
     for i in range(formatpass-1):
          cod+=random.choice(list(string.ascii_lowercase+'123456789'))
     return cod