# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from script.models import SpeechScript


class ChatConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.current_line = 0
        self.room_group_name = self.scope['url_route']['kwargs']['speech_script_id']
        self.content_instance = SpeechScript.objects.get(id=self.room_group_name).content.split('.')
        self.max_line = len(self.content_instance)

    async def connect(self):

        await self.channel_layer.group_add(
            self.room_group_name,  # 그룹 이름 = 방 이름
            self.channel_name  # 클라이언트의 고유 채널 이름
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'notification_message',
                'message': 'enter',
                'sender_channel_name': self.channel_name
            }
        )
        # 웹소켓에서 연결을 받아들임
        await self.accept()
        print(self.scope)
        print(self.channel_name)



    async def disconnect(self, close_code):

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'notification_message',
                'message': 'exit',
                'sender_channel_name': self.channel_name
            }
        )
        # 그룹을 떠남

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # 받는 역할
    async def receive(self, text_data):

        text_data_json = json.loads(text_data)  # dictionary로 변환

        if 'manual_control' in text_data_json['message']:
            self.current_line += int(text_data_json['message']['manual_control'])
            if self.current_line < 0:
                self.current_line = 0
            elif self.current_line > self.max_line:
                self.current_line = self.max_line
            message = self.current_line

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'manual_control_message',
                    'message': message,
                    'sender_channel_name': self.channel_name
                }
            )

        else:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'custom_message',
                    'message': text_data_json['message'],
                    'sender_channel_name': self.channel_name
                }
            )

    async def notification_message(self, event):
        message = event['message']
        # Send message to WebSocket
        if self.channel_name != event['sender_channel_name']:
            await self.send(text_data=json.dumps({  # json으로 변환
                'message': {'notification': message}
            }))

    async def manual_control_message(self, event):
        message = event['message']
        # Send message to WebSocket
        if self.channel_name != event['sender_channel_name']:
            await self.send(text_data=json.dumps({  # json으로 변환
                'message': {'current_line': message}
            }))

    async def custom_message(self, event):
        message = event['message']
        if self.channel_name != event['sender_channel_name']:
            await self.send(text_data=json.dumps({  # json으로 변환
                'message': message
            }))
