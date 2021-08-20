import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
from .models import Players, Specifications, Game
import string
import random
from . import specif
from django.contrib.sessions.models import Session
from datetime import datetime, timedelta


class PlayerConsumer(WebsocketConsumer):
    def connect(self):
        self.lobby = self.scope['url_route']['kwargs']['lobby']
        self.lobby_group_name = 'lobby_{}'.format(self.lobby)
        async_to_sync(self.channel_layer.group_add)(
            self.lobby_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, code):
        player = Players.objects.get(session=self.session,
                                     lobby=self.lobby)
        player.online = False
        player.save()
        async_to_sync(self.channel_layer.group_discard)(
            self.lobby_group_name,
            self.channel_name
        )
        # async_to_sync(self.channel_layer.group_send)(
        #     self.lobby_group_name,
        #     {
        #         'type': 'send_player',
        #         'function':'delete',
        #         'name': player.name,
        #         'id': player.id_user,
        #         'play': player.play,
        #         'session':self.session,
        #         'specs':'none'
        #     }
        # )
        # for playerfor in Players.objects.filter(lobby=self.lobby, online = True):
        #     if playerfor.queue > player.queue:
        #         playerfor.queue -= 1
        #         playerfor.save()
        # if len(Players.objects.filter(lobby = self.lobby, online = True)) == 0:
        #     for pl in Players.objects.filter(lobby = self.lobby):
        #         pl.delete()
        #     Game.objects.get(lobby = self.lobby).delete()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if 'session' not in self.__dict__:
            self.session = text_data_json['session']
            print(self.session)
            if len(Players.objects.filter(lobby=self.lobby, session=self.session, online=True)) > 0:
                async_to_sync(self.channel_layer.group_send)(
                    self.lobby_group_name,
                    {
                        'type': 'offsocket',
                        'session': self.session,
                        'client': self.scope['client']
                    }
                )
        if 'new_player' in text_data_json.keys():
            if 'online' in text_data_json.keys():
                player = Players.objects.get(session = self.session, lobby = self.lobby)
                checker = self.session
            else:
                player = self.addPlayer(text_data_json)
                checker = 'none'
            async_to_sync(self.channel_layer.group_send)(
                self.lobby_group_name,
                {
                    'type': 'send_player',
                    'function': 'add_player',
                    'name': player.name,
                    'play': player.play,
                    'id': player.id_user,
                    'session':checker,
                    'specs': {spec.name_spec: {'spec':spec.spec,'player':spec.player.id_user} for spec in Specifications.objects.filter(player = player, open = True)}
                }
            )
        elif 'change' in text_data_json.keys():
            self.change_team(text_data_json)
        elif 'function' in text_data_json.keys() and text_data_json['function'] == 'start':
            self.start()
        elif 'open' in text_data_json.keys():
            self.open(text_data_json)
        elif 'kick' in text_data_json.keys():
            player = Players.objects.get(id_user=text_data_json['kick'], lobby = self.lobby)
            async_to_sync(self.channel_layer.group_send)(
                self.lobby_group_name,
                {
                    'type': 'kick',
                    'player': text_data_json['kick']
                }
            )

    def addPlayer(self, player):
        id = ''
        for i in range(6):
            inter = string.ascii_lowercase+string.ascii_uppercase
            if i != 0:
                inter+='1234567890'
            id+=random.choice(inter)
        session = Session.objects.get(session_key = self.session)
        if not player['root']:
            root = False
        else:
            root = True
        player = Players(lobby = self.lobby, id_user = id, name = player['new_player'], session = session,play = False, root = root,queue = 0, online = True)
        player.save()
        return player

    def send_player(self,event):
        if self.session != event['session']:
            self.send(json.dumps({
                'function':event['function'],
                'name': event['name'],
                'play': event['play'],
                'id': event['id'],
                'specs':event['specs']
            }))

    def change_team(self,data):
        session = Session.objects.get(session_key = self.session)
        player = Players.objects.get(session = session, lobby = self.lobby)
        if not Game.objects.get(lobby = self.lobby).start:
            send = False
            if not data['change'] and player.play:
                player.play = False
                for playerfor in Players.objects.filter(lobby = self.lobby, online = True):
                    if playerfor.queue > player.queue:
                        playerfor.queue -= 1
                        playerfor.save()
                player.queue = 0
                player.save()
                send = True
            elif data['change'] and not player.play:
                player.play = True
                player.queue = Players.objects.filter(lobby = self.lobby, online = True).order_by('-queue')[0].queue+1
                player.save()
                send = True
            if send:
                async_to_sync(self.channel_layer.group_send)(
                    self.lobby_group_name,
                    {
                        'type': 'send_player',
                        'function': 'change',
                        'name': player.name,
                        'play': player.play,
                        'id': player.id_user,
                        'session':'none',
                        'specs':'none'
                    }
                )

    def start(self):
        game = Game.objects.get(lobby = self.lobby)
        game.start = True
        game.bunker_size = 'Размер бункера '+random.choice(specif.Bunkerstats['Size'])
        game.bunker_kata = 'Катастрофа: '+random.choice(specif.Bunkerstats['Kata'])
        game.bunker_pop = 'Оставшееся населения: '+ str(random.randint(0,20))+'%'
        bunker_time = str(random.randint(3,48))
        if int(bunker_time[-1]) == 1 and int(bunker_time) != 11:
            bunker_time+=' месяц'
        elif 1< int(bunker_time[-1]) < 5 and int(bunker_time) not in [12,13,14]:
            bunker_time+=' месяца'
        else:
            bunker_time+=' месяцев'
        game.bunker_time = 'Время проведения в бункере: '+bunker_time
        game.save()
        async_to_sync(self.channel_layer.group_send)(
            self.lobby_group_name,
            {
                'type':'send_start',
                'bunker': {'size':game.bunker_size,
                'kata':game.bunker_kata,
                'pop':game.bunker_pop,
                'time':game.bunker_time}
            }
        )

    def send_start(self,event):
        prof = random.choice(specif.profs)
        age =random.choice(specif.ages)
        hobby = random.choice(specif.hobbys)
        sex = random.choice(specif.sexes)
        body = random.choice(specif.bodys)
        health = random.choice(specif.healths)
        personality = random.choice(specif.harakters)
        player =  Players.objects.get(lobby = self.lobby, session = self.session)
        for spec, spec_name, ru in zip([prof,age,hobby,sex,body,health,personality], ['Profession', 'Age', 'Hobby','Sex','Body','Health','Personality'],['Профессия: ','Возраст: ', 'Хобби: ', 'Пол: ', 'Телосложение: ','Здоровье: ', 'Черта характера: ']):
            Specifications(name_spec = spec_name, spec = ru+str(spec), open = False, lobby = self.lobby, player = player).save()
        self.send(json.dumps({
            'function':'get_spec',
            'self_specs':{'Profession':'Профессия: '+prof,
                'Age':'Возраст: '+str(age),
                'Hobby':'Хобби: '+hobby,
                'Sex':'Пол: '+sex,
                'Body': 'Телосложение: '+body,
                'Health':'Здоровье: ' + health,
                'Personality':'Черта характера: ' + personality},
            'bunker': event['bunker']
        }))

    def open(self, spec):
        player = Players.objects.get(session = self.session, lobby = self.lobby)
        spec = Specifications.objects.get(name_spec = spec['open'], player = player)
        if not spec.open:
            spec.open = True
            spec.save()
            async_to_sync(self.channel_layer.group_send)(
                self.lobby_group_name,
                {
                    'type':'send_open',
                    'player':player.id_user,
                    'spec':[spec.name_spec,spec.spec]
                }
            )

    def send_open(self,event):
        self.send(json.dumps({
            'function':'open',
            'player':event['player'],
            'spec':event['spec'][1]
        }))

    def offsocket(self, event):
        if event['session'] == self.session and event['client'] != self.scope['client']:
            self.websocket_disconnect(1)

    def kick(self, event):
        self.send(json.dumps({
            'function': 'kick',
            'player': event['player']
        }))