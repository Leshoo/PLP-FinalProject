import pytest
from channels.testing import WebsocketCommunicator
from django.conf import settings
from django.contrib.auth.models import User
from django.test.client import Client

from chat.models import Room
from multichat.asgi import application


@pytest.fixture
async def user_communicator():
    user = User.objects.create_user(username='test_user')
    client = Client()
    client.force_login(user)
    scn = settings.SESSION_COOKIE_NAME
    cookies = (b'cookie', '{}={}'.format(scn, client.cookies[scn].value).encode())
    communicator = WebsocketCommunicator(application, "/chat/stream/", headers=[cookies])
    yield communicator
    await communicator.disconnect()


@pytest.mark.asyncio
async def test_connect_anonymous():
    communicator = WebsocketCommunicator(application, "/chat/stream/")
    connected, __ = await communicator.connect()

    assert not connected

    # Close
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_connect_logged_in(user_communicator):
    connected, __ = await user_communicator.connect()

    assert connected


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_connect_join_room(user_communicator):
    room = Room.objects.create(title='First Room')
    await user_communicator.connect()
    await user_communicator.send_json_to({'command': 'join', 'room': room.id})

    response = await user_communicator.receive_json_from()

    assert response == {'join': str(room.id), 'title': 'First Room'}


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_connect_join_not_existing_room(user_communicator):
    await user_communicator.connect()
    await user_communicator.send_json_to({'command': 'join', 'room': 1})

    response = await user_communicator.receive_json_from()

    assert response == {'error': 'ROOM_INVALID'}
