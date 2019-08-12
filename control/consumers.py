# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from script.models import SpeechScript
from rest_framework.authtoken.models import Token
from scriptslide.settings import CHANNEL_LAYERS
import json
import time


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

        if self.user_category == 'mobile':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'notification_message',
                    'message': {'event': "notification", "user_category": "mobile", "value": "exit"},
                    'sender_channel_name': self.channel_name
                }
            )
            CHANNEL_LAYERS.__delitem__("mobile" + self.room_group_name)
            print("mobile 정상 퇴장")

        elif self.user_category == 'web':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'notification_message',
                    'message': {'event': "notification", "user_category": "web", "value": "exit"},
                    'sender_channel_name': self.channel_name
                }
            )

        elif self.user_category == 'duplicate_fail':
            pass


        # web and mobile 그룹을 떠남
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # 받는 역할
    async def receive(self, text_data):

        text_data_json = json.loads(text_data)  # dictionary로 변환

        if 'notification' in text_data_json['message']['event']:
            if 'mobile' in text_data_json['message']['user_category'] and 'enter' in text_data_json['message']['value']:
                #정상입장
                if CHANNEL_LAYERS.get("mobile" + self.room_group_name) == None:
                    self.user_category = 'mobile'
                    print("mobile 정상 입장")
                    CHANNEL_LAYERS.setdefault("mobile" + self.room_group_name, 1)

                #강제퇴장
                elif CHANNEL_LAYERS.get("mobile" + self.room_group_name) == 1:
                    self.user_category = 'duplicate_fail'
                    print("mobile 강제 퇴장")
                    await self.send(text_data=json.dumps({
                        'message': {'event': "notification", "user_category": "mobile", "value": "duplicate_fail"}
                    }))
                    await self.close()

            #웹 입장
            elif 'web' in text_data_json['message']['user_category'] and 'enter' in text_data_json['message']['value']:
                self.user_category = 'web'


            #정상 입장된 user에 대한 알림
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'notification_message',
                    'message': text_data_json['message'],
                    'sender_channel_name': self.channel_name
                }
            )
            return

        elif 'mobile' in text_data_json['message']['user_category'] and 'button' in text_data_json['message']['event']:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'button_message',
                    'message': text_data_json['message'],
                    'sender_channel_name': self.channel_name
                }
            )
            return

        elif 'text' in text_data_json['message']['event']:
            return

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
