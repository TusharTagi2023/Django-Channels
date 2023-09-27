from channels.consumer import SyncConsumer,AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync,sync_to_async
from .models import Chats,Group
from channels.db import database_sync_to_async

class MyCustomConsumer(SyncConsumer):

    def websocket_connect(self,event):
        async_to_sync(self.channel_layer.group_add)("personal", self.channel_name)
        self.send({
            "type": "websocket.accept",
        })

    def websocket_receive(self,event):
        name=event['text']
        async_to_sync(self.channel_layer.group_send)('personal', {
            'type':'chat.message',
            'message':name
        }
        )


    def chat_message(self, event):
        self.send({
            "type": "websocket.send",
            "text":event['message']
        })

    def websocket_disconnect(self,event):
        async_to_sync(self.channel_layer.group_discard)("personal", self.channel_name)
        raise StopConsumer()

class CustomAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        self.grpname=self.scope['url_route']['kwargs']['grpname']
        await self.channel_layer.group_add(self.grpname, self.channel_name)
        await self.send({
            "type": "websocket.accept",
        })
    async def websocket_receive(self,event):
        name=event['text']
        if self.scope['user'].is_authenticated:
            await self.setchat(name,self.grpname)
            await self.channel_layer.group_send(self.grpname, {
                'type':'chat.message',
                'message':f"{self.scope['user']}:-{name}",
            }
            )
        else:
            await self.channel_layer.group_send(self.grpname, {
                'type':'chat.message',
                'message':"You are not authenticated"
            }
            )
    @database_sync_to_async
    def setchat(self, data, group):
        group=Group.objects.filter(gpname=group).first()
        Chats.objects.create(group=group,txt=data,user=self.scope['user'])

    async def chat_message(self, event):
        await self.send({
            "type": "websocket.send",
            "text":event['message'],

        })
    async def websocket_disconnect(self,event):
        await self.channel_layer.group_discard(self.grpname, self.channel_name)
        raise StopConsumer()
    

