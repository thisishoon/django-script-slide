# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from script.models import SpeechScript
from rest_framework.authtoken.models import Token
#from scriptslide.settings.debug import CHANNEL_LAYERS
from scriptslide.settings.deploy import CHANNEL_LAYERS

import json
import time
from control.check import *
import re
import logging

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
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
                    logging.error("mobile unmatched_fail")
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
                    self.time = 0
                    self.similarity = 0
                    self.last_similarity = 0
                    self.last_end_point = 0
                    self.count = 0
                    print("mobile enter")
                    CHANNEL_LAYERS.setdefault("mobile" + self.room_group_name, 1)


                # 강제퇴장
                elif CHANNEL_LAYERS.get("mobile" + self.room_group_name) == 1:
                    self.user_category = 'mobile_fail'
                    logging.error("mobile duplicate_fail")

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
                self.buffer = ""
                self.time = 0
                self.similarity = 0
                self.last_similarity = 0
                self.last_end_point = 0
                self.count = 0

                num_web = CHANNEL_LAYERS.get("web" + self.room_group_name)
                if num_web is None:
                    CHANNEL_LAYERS.__setitem__("web"+self.room_group_name, 1)

                else:
                    CHANNEL_LAYERS.__setitem__("web"+self.room_group_name, num_web+1)



                # 계속 한글, 영어, 숫자를 제외한 나머지 모든 문자를 지우기위해 미리 컴파일하여 객체를 반환
                self.hangul = re.compile('[^가-힣a-zA-Z0-9]+')



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

            CHANNEL_LAYERS.__setitem__("current_sentence" + self.room_group_name, text_data_json['message']['value'])
            parse_current_sentence = self.hangul.sub('', text_data_json['message']['value'])  # 정규표현식으로 추출
            CHANNEL_LAYERS.__setitem__("parse_current_sentence" + self.room_group_name, parse_current_sentence)
            CHANNEL_LAYERS.__setitem__("current_index" + self.room_group_name,
                                       text_data_json['message']['index'])
            CHANNEL_LAYERS.__setitem__("current_sub_index" + self.room_group_name,
                                       text_data_json['message']['sub_index'])


            CHANNEL_LAYERS.__setitem__("next_sentence" + self.room_group_name,
                                       text_data_json['message']['value2'])
            parse_next_sentence = self.hangul.sub('', text_data_json['message']['value2'])  # 다음 문장 정규표현식으로 추출
            CHANNEL_LAYERS.__setitem__("parse_next_sentence" + self.room_group_name, parse_next_sentence)
            CHANNEL_LAYERS.__setitem__("next_index" + self.room_group_name,
                                       text_data_json['message']['index2'])
            #CHANNEL_LAYERS.__setitem__("next_sub_index" + self.room_group_name,
            #                           text_data_json['message']['sub_index2'])

            return

        # speech control
        # mobile에서 speech event를 통한 stt의 결과물인 text receive
        elif 'speech' in text_data_json['message']['event']:
            if time.time() - self.time < 0.01:
                return
            else:
                self.time = time.time()

            current_parse_sentence = CHANNEL_LAYERS.get("parse_current_sentence" + self.room_group_name)
            current_sentence = CHANNEL_LAYERS.get("current_sentence" + self.room_group_name)
            next_parse_sentence = CHANNEL_LAYERS.get("parse_next_sentence" + self.room_group_name)
            next_sentence = CHANNEL_LAYERS.get("next_sentence" + self.room_group_name)

            if current_parse_sentence=='' or current_parse_sentence == None:
                logging.error(current_sentence,"is None type!")
                return


            text = self.hangul.sub('', text_data_json['message']['value'])
            total_text = self.buffer + text

            if (text_data_json['message']['status'] == 'done'):
                self.buffer += text

            print(current_parse_sentence)
            print(total_text)

            similarity, start_point, end_point, cnt = LCS(current_sentence, current_parse_sentence, total_text)
            next_similarity = 0
            if next_parse_sentence != '' or next_parse_sentence != None:
                next_similarity, next_start_point, next_end_point, _ = LCS(next_sentence, next_parse_sentence, total_text)

            # success
            if similarity > 0.6:
                if cnt < 3:
                    self.count += 1
                    if self.count == 1: #첫 통과
                        await self.channel_layer.group_send(
                            self.room_group_name,
                            {
                                'type': 'speech_message',
                                'message': {'event': "speech", "user_category": "server", "value": 1,
                                            "similarity": similarity, "start_point": start_point, "end_point": end_point,
                                            "index": CHANNEL_LAYERS.get("current_index" + self.room_group_name),
                                            "sub_index": CHANNEL_LAYERS.get("current_sub_index" + self.room_group_name),
                                            "current_sentence": current_sentence, "speech": total_text},
                                'sender_channel_name': self.channel_name
                            }
                        )
                        self.last_similarity = similarity
                        self.last_end_point = end_point
                        print("success! execution time : ", time.time()-self.time)

                    else:   #두번 이상의 통과
                        if self.last_end_point < end_point:   #계속 증가하는 중 이라면
                            self.last_similarity = similarity
                            self.last_end_point = end_point
                            return

                        else:                                   #문장의 끝을 확인
                            self.count = 0
                            self.last_similarity = 0
                            await self.channel_layer.group_send(
                                self.room_group_name,
                                {
                                    'type': 'speech_message',
                                    'message': {'event': "speech", "user_category": "server", "value": 2,
                                                "similarity": similarity, "start_point": start_point,
                                                "end_point": end_point,
                                                "index": CHANNEL_LAYERS.get("current_index" + self.room_group_name),
                                                "sub_index": CHANNEL_LAYERS.get(
                                                    "current_sub_index" + self.room_group_name),
                                                "current_sentence": current_sentence, "speech": total_text},
                                    'sender_channel_name': self.channel_name
                                }
                            )
                            self.buffer = ""
                            return
                else:
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'speech_message',
                            'message': {'event': "speech", "user_category": "server", "value": 0,
                                        "similarity": similarity, "start_point": start_point, "end_point": end_point,
                                        "index": CHANNEL_LAYERS.get("current_index" + self.room_group_name),
                                        "sub_index": CHANNEL_LAYERS.get("current_sub_index" + self.room_group_name),
                                        "current_sentence": current_sentence, "speech": total_text},
                            'sender_channel_name': self.channel_name
                        }
                    )


            #유사도 fail
            else:
                if self.count==1:
                    return

                if next_similarity > 0.1 and similarity < next_similarity:
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'speech_message',
                            'message': {'event': "speech", "user_category": "server", "value": 3,
                                        "similarity": next_similarity,
                                        "index": CHANNEL_LAYERS.get("current_index" + self.room_group_name),
                                        "sub_index": CHANNEL_LAYERS.get("current_sub_index" + self.room_group_name),
                                        "current_sentence": current_sentence, "speech": total_text},
                            'sender_channel_name': self.channel_name
                        }
                    )
                    self.buffer = ""

                else:
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'speech_message',
                            'message': {'event': "speech", "user_category": "server", "value": 0,
                                        "similarity": similarity, "start_point": start_point, "end_point": end_point,
                                        "index": CHANNEL_LAYERS.get("current_index" + self.room_group_name),
                                        "sub_index": CHANNEL_LAYERS.get("current_sub_index" + self.room_group_name),
                                        "current_sentence": current_sentence, "speech": total_text},
                            'sender_channel_name': self.channel_name
                        }
                    )



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
        await self.send(text_data=json.dumps({
            'message': message
        }))


    async def custom_message(self, event):
        message = event['message']
        if self.channel_name != event['sender_channel_name']:
            await self.send(text_data=json.dumps({
                'message': message
            }))
