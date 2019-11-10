from asgiref.sync import async_to_sync
from django.test import TestCase
import pytest
import control
from control.consumers import ChatConsumer
from channels.testing import WebsocketCommunicator
from channels.testing import HttpCommunicator
from channels.testing import ApplicationCommunicator
import asyncio
from django.test import TestCase

@pytest.mark.asyncio
async def test_connect():
    communicator = WebsocketCommunicator(ChatConsumer, "/ws/control/1/")
    communicator.scope['url_route'] = {
        "kwargs": {"speech_script_id": "1"}
    }
    connected, subprotocol = await communicator.connect()
    assert connected

    communicator2 = WebsocketCommunicator(ChatConsumer, "/ws/control/1/")
    communicator2.scope['url_route'] = {
        "kwargs": {"speech_script_id": "1"}
    }

    connected2, subprotocol2 = await communicator2.connect()
    assert connected2

    await communicator.send_json_to(
        {
        "message": {
            "event": "notification",
            "user_category": "web",
            "value": "enter"
            }
        }
    )
    await asyncio.sleep(0)

    await communicator2.send_json_to(
        {
        "message": {
            "event": "notification",
            "user_category": "mobile",
            "value": "enter"
            }
        }
    )


    noti_response = await communicator.receive_json_from()
    print(noti_response)
    print(type(noti_response))
    assert noti_response == {"message": {
        "event": "notification",
        "user_category": "mobile",
        "value": "enter"}
        }

    noti2_response = await communicator2.receive_json_from()
    assert noti2_response =={"message": {
        "event": "notification",
        "user_category": "web",
        "value": "enter"}
    }

    await communicator.send_json_to(
        {
            "message": {
                "event": "sentence",
                "user_category": "web",
                "value": "안녕하세요 저는 강지훈입니다 이제부터 발표를 시작하겠습니다",
            }
        }
    )

    print(communicator.scope)

    await communicator.disconnect()
    await communicator2.disconnect()


