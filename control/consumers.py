# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from script.models import SpeechScript
from rest_framework.authtoken.models import Token
from scriptslide.settings import CHANNEL_LAYERS
import json
import time
from collections import OrderedDict


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        '''
        print(self.scope['user'])
        temp= text_data_json['message']['token']
        print(temp)
        token= Token.objects.get(key=temp)
        self.scope['user']=token.user
        print(self.scope['user'])
        if self.speech_script_instance.user == token.user:
        print('ok')
        '''

        self.room_group_name = self.scope['url_route']['kwargs']['speech_script_id']
        self.speech_script_instance = SpeechScript.objects.get(id=self.room_group_name)

        await self.channel_layer.group_add(
            self.room_group_name,  # 그룹 이름 = 방 이름
            self.channel_name  # 클라이언트의 고유 채널 이름
        )
        # 웹소켓에서 연결을 받아들임
        await self.accept()

    async def disconnect(self, close_code):

        if self.user_categiry == 'mobile':
            self.file_data['log'] = self.temp
            self.file_data['sum_of_previous'] = self.previous
            self.file_data['sum_of_next'] = self.next
            self.file_data['sum_of_button'] = self.previous + self.next
            self.file_data["sum_of_runtime"] = time.time() - self.start
            if (time.time() - self.start) > 30:
                with open("usertest_log/" + self.speech_script_instance.title + "(" + self.day + ")" + ".json", 'w',
                          encoding="utf-8") as make_file:
                    json.dump(self.file_data, make_file, ensure_ascii=False, indent='\t')
                print("save log file")
            else:
                print("Do not save log file less than 30 seconds")


            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'notification_message',
                    'message': {'event': "notification", "user_category": "mobile", "value": "exit"},
                    'sender_channel_name': self.channel_name
                }
            )

        elif self.user_categiry == 'web':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'notification_message',
                    'message': {'event': "notification", "user_category": "web", "value": "exit"},
                    'sender_channel_name': self.channel_name
                }
            )

        #그룹을 떠남
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    # 받는 역할
    async def receive(self, text_data):

        text_data_json = json.loads(text_data)  # dictionary로 변환

        if 'notification' in text_data_json['message']['event']:
            if 'mobile' in text_data_json['message']['user_category'] and 'enter' in text_data_json['message']['value']:
                self.user_categiry='mobile'
                self.start = time.time()
                self.temp = []
                self.previous = 0
                self.next = 0
                self.file_data = OrderedDict()
                self.day = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
                self.file_data["speech_script_title"] = self.speech_script_instance.title

            elif 'web' in text_data_json['message']['user_category'] and 'enter' in text_data_json['message']['value']:
                self.user_categiry='web'

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'notification_message',
                    'message': text_data_json['message'],
                    'sender_channel_name': self.channel_name
                }
            )

        elif 'mobile' in text_data_json['message']['user_category'] and 'button' in text_data_json['message']['event']:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'button_message',
                    'message': text_data_json['message'],
                    'sender_channel_name': self.channel_name
                }
            )
            if text_data_json['message']['value'] == 1:
                self.temp.append("next")
                self.next += 1
            elif text_data_json['message']['value'] == -1:
                self.temp.append("previous")
                self.previous += 1

        elif 'text' in text_data_json['message']['event']:
            pass



    async def notification_message(self, event):
        message = event['message']
        # Send message to WebSocket
        if self.channel_name != event['sender_channel_name']:
            await self.send(text_data=json.dumps({  # json으로 변환
                'message': message
            }))

    async def button_message(self, event):
        message = event['message']
        if self.channel_name != event['sender_channel_name']:
            await self.send(text_data=json.dumps({  # json으로 변환
                'message': message
            }))

    async def text_message(self, event):
        message = event['message']
        if self.channel_name != event['sender_channel_name']:
            await self.send(text_data=json.dumps({  # json으로 변환
                'message': message
            }))
