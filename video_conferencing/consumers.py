from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

class ConnectConsumer(WebsocketConsumer):
    def connect(self):
        print("HERE")
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        async_to_sync(self.channel_layer.group_add)(
            self.room_id,
            self.channel_name
        )
        async_to_sync(self.channel_layer.group_send)(
            self.room_id,
            {
                'type': 'connection_message',
                'obj': {'id':self.user_id,'type':1}
            }
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_send)(
            self.room_id,
            {
                'type': 'connection_message',
                'obj': {'id':self.user_id,'type':0}
            }
        )
        async_to_sync(self.channel_layer.group_discard)(
            self.room_id,
            self.channel_name
        )

    def connection_message(self, event):
        self.send(text_data=json.dumps({
            'obj': event['obj'],
        }))