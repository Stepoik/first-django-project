import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
from .models import Players, Specifications
import string
import random
from . import specif


class PlayerConsumer(WebsocketConsumer):
    def connect(self):
        self.lobby = self.scope['url_route']['kwargs']['lobby']
        self.lobby_group_name = 'lobby_{}'.format(self.lobby)
        async_to_sync(self.channel_layer.group_add)(
            self.lobby_group_name,
            self.channel_name
        )
        if self.scope['session'].session_key == None:
            self.scope['session'].save()
        self.session = self.scope['session'].session_key
        self.accept()

    def disconnect(self, code):
        player = Players.objects.get(session=self.scope['session'].session_key,
                                     lobby=self.scope['url_route']['kwargs']['lobby'])
        async_to_sync(self.channel_layer.group_discard)(
            self.lobby_group_name,
            self.channel_name
        )
        async_to_sync(self.channel_layer.group_send)(
            self.lobby_group_name,
            {
                'type': 'receive_player',
                'function': 'delPlayer',
                'name': player.name,
                'id': player.id_user,
                'play': player.play
            }
        )
        player.delete()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json['function'] == 'GetPlayers':
            player = self.addPlayer(text_data_json)
            async_to_sync(self.channel_layer.group_send)(
                self.lobby_group_name,
                {
                    'type': 'receive_player',
                    'function': 'addPlayer',
                    'name': text_data_json['name'],
                    'play': player.play,
                    'id': player.id_user,
                }
            )
            self.send(text_data=json.dumps({
                'function': 'GetPlayers',
                'players': [{'id': playerfor.id_user, 'name': playerfor.name, 'play': playerfor.play} for playerfor in
                            Players.objects.filter(lobby=self.scope['url_route']['kwargs']['lobby']) if
                            player.id_user != playerfor.id_user],
                'root': player.root
            }))
        elif text_data_json['function'] == 'changeTeam':
            player = Players.objects.get(lobby=self.scope['url_route']['kwargs']['lobby'],
                                         session=self.scope['session'].session_key)
            player.play = text_data_json['play']
            player.save()
            async_to_sync(self.channel_layer.group_send)(
                self.lobby_group_name,
                {
                    'type': 'change',
                    'play': player.play,
                    'id': player.id_user
                }
            )
        elif text_data_json['function'] == 'start':
            async_to_sync(self.channel_layer.group_send)(
                self.lobby_group_name,
                {
                    'type': 'start',
                })
        elif text_data_json['function'] == 'open':
            player = Players.objects.get(lobby=self.lobby, session=self.session)
            spec = Specifications.objects.get(player=player.id, name_spec=text_data_json['spec'])
            if spec.open == 'false':
                spec.open = 'true'
                spec.save()
                async_to_sync(self.channel_layer.group_send)(
                    self.lobby_group_name,
                    {
                        'type': 'open',
                        'spec': spec.spec,
                        'player_id': player.id_user,
                    }
                )

    def receive_player(self, event):
        player_name = event['name']
        player_id = event['id']
        self.send(text_data=json.dumps({
            'function': event['function'],
            'name': player_name,
            'id': player_id,
            'play': event['play']
        }))

    def change(self, event):
        id = event['id']
        play = event['play']
        self.send(text_data=json.dumps({
            'function': 'changeTeam',
            'id': id,
            'play': play
        }))

    def addPlayer(self, player):
        id = ''
        for i in range(6):
            id += random.choice(string.ascii_lowercase + string.ascii_uppercase)
        if self.scope['session'].session_key == None:
            self.scope['session'].save()
        root = 'false'
        if len(Players.objects.filter(lobby=self.scope['url_route']['kwargs']['lobby'])) == 0:
            root = 'true'
        print(player['name'])
        new_player = Players(id_user=id, name=player['name'], lobby=self.lobby,
                             session=self.scope['session'].session_key, play='false', root=root)
        new_player.save()
        return new_player

    def start(self, event):
        player = Players.objects.get(session=self.scope['session'].session_key,
                                     lobby=self.scope['url_route']['kwargs']['lobby'])
        if player.play == 'true':
            prof = random.choice(specif.profs)
            age = random.choice(specif.ages)
            hobby = random.choice(specif.hobbys)
            for name, spec in zip(['hobby', 'age', 'prof'], [hobby, age, prof]):
                Specifications.objects.create(player=player, name_spec=name, spec=spec, open='false')
            self.send(text_data=json.dumps({
                'function': 'getspecif',
                'prof': prof,
                'age': age,
                'hobby': hobby
            }))

    def open(self, event):
        spec = event['spec']
        player = event['player_id']
        self.send(json.dumps({
            'function': 'open',
            'id': player,
            'spec': spec
        }))
