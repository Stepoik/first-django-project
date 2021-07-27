from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.db import connection
from .models import Alias, Teams, Lobbys, Words
from django.contrib.sessions.models import Session
from datetime import datetime, timedelta, timezone
import random
import string

def redirection(request):
     lobby = getSessionTeam(formatpass=6)
     return redirect(lobby+'/')

def main(request, lobby):
    return render(request, 'games/monopoly.html')

def send(request,lobby):
     if request.is_ajax():
          game = Lobbys.objects.get(lobby = lobby)
          roundNext(lobby, game)
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
     team.score += len(Words.objects.filter(lobby=lobby, status='true'))
     if team.player_quest+1 == len(Alias.objects.filter(lobby = lobby, team = team.team)):
          team.player_quest = 0
     else:
          team.player_quest +=1
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
          if len(Alias.objects.filter(lobby = lobby, team = request.session.get('team'))) > 1 or request.session.get('team') == 'spect':
               team = getSessionTeam(formatpass=7)
               Teams(team = team, lobby = lobby,score = 0,player_quest = 0).save()
               player = Alias.objects.get(lobby = lobby, session = request.session.get('self'))
               player.team = team
               request.session['team'] = team
               player.save()
          return HttpResponse('create')
def getWords(request, lobby,game): #Get all words and questor/answer
     teamIndex =Lobbys.objects.get(lobby=lobby).queue
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
          game = Lobbys.objects.get(lobby = lobby)
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
          Lobbys.objects.get(lobby = lobby).delete()
          delWords(lobby)
     return HttpResponse('delete')
def startGame(request,lobby): # start game
     game = Lobbys.objects.get(lobby = lobby)
     game.start = 'true'
     game.save()
     return HttpResponse('start')
def changeTeam(request, lobby): #change users team
     if request.is_ajax() and Lobbys.objects.get(lobby = lobby).start == 'false':
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
               game = Lobbys.objects.get(lobby = lobby)
          except:
               createGame(lobby)
               game = Lobbys.objects.get(lobby = lobby)
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
     Lobbys(lobby = lobby, start = 'false', queue =0, round = 'false').save()
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