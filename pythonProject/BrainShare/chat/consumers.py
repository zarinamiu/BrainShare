import json
from datetime import datetime
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):
    """
    WebSocket Consumer для чата BrainShare.
    Поддерживает комнаты чата, системные сообщения и историю.
    """

    def connect(self):
        """Подключение к комнате чата"""
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Присоединяемся к группе комнаты
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        # Получаем информацию о пользователе
        user = self.scope.get('user')
        username = user.username if user and user.is_authenticated else 'Аноним'

        # Отправляем системное сообщение о подключении
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'system_message',
                'message': f'{username} подключился(ась) к комнате "{self.room_name}"',
                'timestamp': datetime.now().isoformat()
            }
        )

    def disconnect(self, close_code):
        """Отключение от комнаты чата"""
        # Получаем информацию о пользователе
        user = self.scope.get('user')
        username = user.username if user and user.is_authenticated else 'Аноним'

        # Отправляем системное сообщение об отключении
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'system_message',
                'message': f'{username} покинул(а) комнату "{self.room_name}"',
                'timestamp': datetime.now().isoformat()
            }
        )

        # Покидаем группу комнаты
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        """Получение сообщения от клиента"""
        if not text_data:
            return

        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return

        message = data.get('message', '').strip()

        if not message:
            return

        # Получаем информацию о пользователе
        user = self.scope.get('user')
        username = user.username if user and user.is_authenticated else 'Аноним'

        # Отправляем сообщение в группу комнаты
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': username,
                'timestamp': datetime.now().isoformat()
            }
        )

    def chat_message(self, event):
        """Отправка сообщения чата клиенту"""
        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': event['message'],
            'sender': event['sender'],
            'timestamp': event.get('timestamp', datetime.now().isoformat())
        }))

    def system_message(self, event):
        """Отправка системного сообщения клиенту"""
        self.send(text_data=json.dumps({
            'type': 'system',
            'message': event['message'],
            'timestamp': event.get('timestamp', datetime.now().isoformat())
        }))