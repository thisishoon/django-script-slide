# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from script.models import SpeechScript
from rest_framework.authtoken.models import Token
from scriptslide.settings.base import CHANNEL_LAYERS
import json
import time
from control.check import *
import re


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
        # self.speech_script_instance = SpeechScript.objects.get(id=self.room_group_name)

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
            print("mobile exit")

        elif self.user_category == 'web':
            num_web = CHANNEL_LAYERS.get("web"+self.room_group_name)
            if num_web == 1:
                CHANNEL_LAYERS.__setitem__("web"+self.room_group_name, None)
            else:
                CHANNEL_LAYERS.__setitem__("web"+self.room_group_name, num_web-1)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'notification_message',
                    'message': {'event': "notification", "user_category": "web", "value": "exit"},
                    'sender_channel_name': self.channel_name
                }
            )

        elif self.user_category == 'mobile_fail':
            pass

        # web and mobile 그룹을 떠남
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # 받는 역할
    async def receive(self, text_data):

        text_data_json = json.loads(text_data)  # json형식을 dictionary로 변환

        if 'notification' in text_data_json['message']['event']:
            if 'mobile' in text_data_json['message']['user_category'] and 'enter' in text_data_json['message']['value']:

                if CHANNEL_LAYERS.get("web"+self.room_group_name) == None:
                    print("mobile unmatched_fail")
                    self.user_category = 'mobile_fail'
                    await self.send(text_data=json.dumps({
                        'message': {'event': "notification", "user_category": "mobile", "value": "unmatched_fail"}
                    }))
                    await self.close()
                    return

                # 정상입장
                if CHANNEL_LAYERS.get("mobile" + self.room_group_name) == None:
                    self.user_category = 'mobile'
                    self.buffer = ""
                    self.word = 0
                    print("mobile enter")
                    CHANNEL_LAYERS.setdefault("mobile" + self.room_group_name, 1)


                # 강제퇴장
                elif CHANNEL_LAYERS.get("mobile" + self.room_group_name) == 1:
                    self.user_category = 'mobile_fail'
                    print("mobile duplicate_fail")

                    await self.send(text_data=json.dumps({
                        'message': {'event': "notification", "user_category": "mobile", "value": "duplicate_fail"}
                    }))

                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'notification_message',
                            'message': {'event': "notification", "user_category": "mobile", "value": "duplicate_fail"},
                            'sender_channel_name': self.channel_name
                        }
                    )

                    await self.close()
                    return




            # 웹 입장
            elif 'web' in text_data_json['message']['user_category'] and 'enter' in text_data_json['message']['value']:

                self.user_category = 'web'
                num_web = CHANNEL_LAYERS.get("web" + self.room_group_name)
                if num_web is None:
                    CHANNEL_LAYERS.__setitem__("web"+self.room_group_name, 1)

                else:
                    CHANNEL_LAYERS.__setitem__("web"+self.room_group_name, num_web+1)



                # 계속 한글, 영어, 숫자를 제외한 나머지 모든 문자를 지우기위해 미리 컴파일하여 객체를 반환
                self.hangul = re.compile('[^가-힣a-z0-9]+')



            # 정상 입장된 user에 대한 알림
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'notification_message',
                    'message': text_data_json['message'],
                    'sender_channel_name': self.channel_name
                }
            )
            return

        elif 'custom' in text_data_json['message']['event']:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'custom_message',
                    'message': text_data_json['message'],
                    'sender_channel_name': self.channel_name
                }
            )
            return

        # manual control
        # mobile에서 UI를 통해 manual_control 시 동작
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

        # sentence
        elif 'sentence' in text_data_json['message']['event']:
            CHANNEL_LAYERS.__setitem__("sentence" + self.room_group_name, text_data_json['message']['value'])
            parse_sentence = self.hangul.sub('', text_data_json['message']['value'])  # 정규표현식으로 추출
            CHANNEL_LAYERS.__setitem__("parse_sentence" + self.room_group_name, parse_sentence)
            print("set  :" + parse_sentence)
            return

        # speech control
        # mobile에서 speech event를 통한 stt의 결과물인 text receive
        elif 'speech' in text_data_json['message']['event']:
            current_sentence = CHANNEL_LAYERS.get("sentence" + self.room_group_name)
            current_parse_sentence = CHANNEL_LAYERS.get("parse_sentence" + self.room_group_name)

            text = text_data_json['message']['value']
            speech_word = len(text.split(' '))
            print("current_parse_sentence : " + current_parse_sentence)
            print("speech_sentence : " + text)
            print("buffer_sentence :" + self.buffer)
            print("기존 어절 " + str(self.word))
            print("음성 어절 " + str(speech_word))

            if(text_data_json['message']['status']=="doing"):
                print("말하는 중"+text)

            elif(text_data_json['message']['status']=='done'):
                self.buffer += text
                print("말 끝"+text)

            # success
            if LCS(current_parse_sentence, self.buffer + text):
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'speech_message',
                        'message': {'event': "button", "user_category": "mobile", "value": 1},
                        'sender_channel_name': self.channel_name
                    }
                )
                self.buffer = ""
            return

    async def notification_message(self, event):
        message = event['message']
        # Send message to WebSocket
        if self.channel_name != event['sender_channel_name']:
            await self.send(text_data=json.dumps({
                'message': message
            }))

    async def button_message(self, event):
        message = event['message']
        if self.channel_name != event['sender_channel_name']:
            await self.send(text_data=json.dumps({
                'message': message
            }))

    async def speech_message(self, event):
        message = event['message']
        if self.channel_name != event['sender_channel_name']:
            await self.send(text_data=json.dumps({
                'message': message
            }))

    async def custom_message(self, event):
        message = event['message']
        if self.channel_name != event['sender_channel_name']:
            await self.send(text_data=json.dumps({
                'message': message
            }))
