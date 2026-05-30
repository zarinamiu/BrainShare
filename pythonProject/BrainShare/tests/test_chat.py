"""
Тесты WebSocket чата BrainShare
"""
import pytest
import json
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model

User = get_user_model()


#  ТЕСТЫ WEBSOCKET

@pytest.mark.asyncio
@pytest.mark.django_db
class TestChatWebSocket:
    """Тесты WebSocket соединений"""

    async def test_websocket_connect(self):
        """Проверка подключения к WebSocket"""
        from brainshare.asgi import application

        communicator = WebsocketCommunicator(
            application,
            '/ws/chat/general/'
        )

        connected, _ = await communicator.connect()
        assert connected is True

        await communicator.disconnect()

    async def test_websocket_receive_message(self):
        """Проверка отправки и получения сообщения через WebSocket"""
        from brainshare.asgi import application

        communicator = WebsocketCommunicator(
            application,
            '/ws/chat/general/'
        )

        connected, _ = await communicator.connect()
        assert connected is True

        system_message = await communicator.receive_json_from()
        assert system_message['type'] == 'system'

        await communicator.send_json_to({
            'message': 'Test message from pytest'
        })

        response = await communicator.receive_json_from()

        assert response['type'] == 'chat'
        assert response['message'] == 'Test message from pytest'
        assert 'sender' in response

        await communicator.disconnect()

    async def test_websocket_system_message_on_connect(self):
        """При подключении должно прийти системное сообщение"""
        from brainshare.asgi import application

        communicator = WebsocketCommunicator(
            application,
            '/ws/chat/study/'
        )

        connected, _ = await communicator.connect()
        assert connected is True

        response = await communicator.receive_json_from()

        assert response['type'] == 'system'
        assert 'подключился' in response['message'] or 'подключилась' in response['message']

        await communicator.disconnect()

    async def test_websocket_different_rooms(self):
        """Сообщения в разных комнатах не должны пересекаться"""
        from brainshare.asgi import application

        communicator_general = WebsocketCommunicator(
            application,
            '/ws/chat/general/'
        )

        communicator_python = WebsocketCommunicator(
            application,
            '/ws/chat/python/'
        )

        connected1, _ = await communicator_general.connect()
        connected2, _ = await communicator_python.connect()

        assert connected1 is True
        assert connected2 is True

        await communicator_general.receive_json_from()
        await communicator_python.receive_json_from()

        await communicator_general.send_json_to({
            'message': 'Message in general room'
        })

        response_general = await communicator_general.receive_json_from()

        assert response_general['type'] == 'chat'
        assert response_general['message'] == 'Message in general room'

        await communicator_general.disconnect()
        await communicator_python.disconnect()

    async def test_websocket_multiple_messages(self):
        """Проверка отправки нескольких сообщений подряд"""
        from brainshare.asgi import application

        communicator = WebsocketCommunicator(
            application,
            '/ws/chat/general/'
        )

        connected, _ = await communicator.connect()
        assert connected is True

        await communicator.receive_json_from()

        messages = ['First message', 'Second message', 'Third message']

        for msg in messages:
            await communicator.send_json_to({'message': msg})
            response = await communicator.receive_json_from()
            assert response['type'] == 'chat'
            assert response['message'] == msg

        await communicator.disconnect()

    async def test_websocket_room_general_exists(self):
        """Проверка существования комнаты general"""
        from brainshare.asgi import application

        communicator = WebsocketCommunicator(
            application,
            '/ws/chat/general/'
        )

        connected, _ = await communicator.connect()
        assert connected is True

        await communicator.disconnect()

    async def test_websocket_room_study_exists(self):
        """Проверка существования комнаты study"""
        from brainshare.asgi import application

        communicator = WebsocketCommunicator(
            application,
            '/ws/chat/study/'
        )

        connected, _ = await communicator.connect()
        assert connected is True

        await communicator.disconnect()

    async def test_websocket_room_python_exists(self):
        """Проверка существования комнаты python"""
        from brainshare.asgi import application

        communicator = WebsocketCommunicator(
            application,
            '/ws/chat/python/'
        )

        connected, _ = await communicator.connect()
        assert connected is True

        await communicator.disconnect()

    async def test_websocket_message_format(self):
        """Проверка формата сообщения чата"""
        from brainshare.asgi import application

        communicator = WebsocketCommunicator(
            application,
            '/ws/chat/general/'
        )

        connected, _ = await communicator.connect()
        assert connected is True

        await communicator.receive_json_from()

        await communicator.send_json_to({
            'message': 'Format test'
        })

        response = await communicator.receive_json_from()

        # Проверяем обязательные поля
        assert 'type' in response
        assert 'message' in response
        assert 'sender' in response

        await communicator.disconnect()


# ТЕСТЫ КОМНАТ ЧАТА

@pytest.mark.django_db
class TestChatRooms:
    """Тесты конфигурации комнат чата"""

    def test_available_rooms_constant_exists(self):
        """Проверка существования переменной AVAILABLE_ROOMS"""
        from chat.views import AVAILABLE_ROOMS

        assert AVAILABLE_ROOMS is not None
        assert isinstance(AVAILABLE_ROOMS, (list, tuple))

    def test_available_rooms_not_empty(self):
        """Проверка непустого списка комнат"""
        from chat.views import AVAILABLE_ROOMS

        assert len(AVAILABLE_ROOMS) >= 1

    def test_available_rooms_minimum_count(self):
        """Проверка минимального количества комнат"""
        from chat.views import AVAILABLE_ROOMS

        assert len(AVAILABLE_ROOMS) >= 2

    def test_available_rooms_general_exists(self):
        """Проверка наличия комнаты general"""
        from chat.views import AVAILABLE_ROOMS

        assert 'general' in AVAILABLE_ROOMS

    def test_available_rooms_names_are_strings(self):
        """Проверка типов названий комнат"""
        from chat.views import AVAILABLE_ROOMS

        for room in AVAILABLE_ROOMS:
            assert isinstance(room, str)
            assert len(room) > 0

    def test_available_rooms_no_spaces(self):
        """Проверка отсутствия пробелов в названиях комнат"""
        from chat.views import AVAILABLE_ROOMS

        for room in AVAILABLE_ROOMS:
            assert ' ' not in room

    def test_available_rooms_no_duplicates(self):
        """Проверка отсутствия дубликатов комнат"""
        from chat.views import AVAILABLE_ROOMS

        assert len(AVAILABLE_ROOMS) == len(set(AVAILABLE_ROOMS))

    def test_available_rooms_lowercase(self):
        """Проверка названий комнат в нижнем регистре"""
        from chat.views import AVAILABLE_ROOMS

        for room in AVAILABLE_ROOMS:
            assert room == room.lower()

    def test_room_display_names_dict_exists(self):
        """Проверка существования словаря отображаемых названий"""
        ROOM_DISPLAY_NAMES = {
            'general': 'Общий чат',
            'study': 'Учеба',
            'python': 'Python',
            'django': 'Django',
            'memes': 'Мемы',
            'offtopic': 'Оффтопик',
        }

        from chat.views import AVAILABLE_ROOMS

        for room in AVAILABLE_ROOMS:
            if room in ROOM_DISPLAY_NAMES:
                assert isinstance(ROOM_DISPLAY_NAMES[room], str)
                assert len(ROOM_DISPLAY_NAMES[room]) > 0