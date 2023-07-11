import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User

from main.models import BasicUser, Image, Comment, Location
from chat.models import Thread, ChatMessage


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        self.thread_id = self.scope["url_route"]["kwargs"]["thread_id"]
        self.exception_thread_id = "12f2ccc9-fa41-4e15-bde0-a8e560391ea4"
        self.room_group_name = "chat_%s" % self.thread_id
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.send({"type": "websocket.accept"})

    async def websocket_receive(self, event):
        received_data = json.loads(event["text"])
        msg = received_data.get("message")
        sent_by_id = received_data.get("sent_by")
        send_to_id = received_data.get("send_to")
        thread_id = received_data.get("thread_id")
        images = received_data.get("images", [])
        location = received_data.get("coords")

        sent_by_user = await self.get_user_object(sent_by_id)
        if not sent_by_user:
            print("Error:: sent by user is incorrect")
            return
        if not send_to_id:
            print("sending message to public")
            thread_obj = await self.get_or_create_threads(
                thread_id=thread_id, user1=sent_by_user
            )
            message_obj = await self.create_chat_message(
                thread_obj, sent_by_user, msg, images
            )
            attached_images = message_obj["images"]
            message = message_obj["chat_message"]
            return await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": json.dumps(
                        {
                            "id": str(message.id),
                            "thread": str(message.thread.id),
                            "message": message.message,
                            "user": message.user.id,
                            "attached_images": attached_images,
                            "timestamp": str(message.timestamp),
                        }
                    ),
                },
            )

        send_to_user = await self.get_user_object(send_to_id)

        if not msg and not thread_id:
            print("creating thread")
            # try:
            thread_obj = await self.get_or_create_threads(
                sent_by_user, send_to_user, True
            )
            thread = thread_obj["thread"]
            return await self.send(
                {
                    "type": "websocket.send",
                    "text": json.dumps(
                        {
                            "action": "redirect_user_thread",
                            "id": str(thread.id),
                            "updated": str(thread.updated),
                            "timestamp": str(thread.timestamp),
                            "members": thread_obj["members"],
                        }
                    ),
                }
            )
            # except Exception as err:
            # print("ERRROR")
            # print(err)
            # return
        print("sending message")
        thread_obj = await self.get_or_create_threads(
            sent_by_user, send_to_user, thread_id=thread_id
        )
        print(thread_obj)

        message_obj = await self.create_chat_message(
            thread_obj, sent_by_user, msg, images, location=location
        )
        attached_images = message_obj["images"]
        message = message_obj["chat_message"]
        print(self.room_group_name)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": json.dumps(
                    {
                        "id": str(message.id),
                        "thread": str(message.thread.id),
                        "message": message.message,
                        "user": message.user.id,
                        "attached_images": attached_images,
                        "location": {
                            "id": message.location.id,
                            "latitude": message.location.latitude,
                            "longitude": message.location.longitude,
                        }
                        if message.location
                        else None,
                        "timestamp": str(message.timestamp),
                        "read": message.read,
                        "action": "sendMessage",
                    }
                ),
            },
        )

    async def websocket_disconnect(self, event):
        print("disconnect", event)

    async def chat_message(self, event):
        print("chat_message", event)
        await self.send({"type": "websocket.send", "text": event["message"]})

    @database_sync_to_async
    def get_user_object(self, user_id):
        print("USERID: ", user_id)
        print(BasicUser.objects.get(id=user_id))
        qs = BasicUser.objects.filter(id=user_id)
        print(qs)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj

    @database_sync_to_async
    def get_or_create_threads(
        self, user1=None, user2=None, members_list=False, thread_id=None
    ):
        if thread_id:
            print("WHAT DE HEIL", thread_id)
            try:
                thread = Thread.objects.get(id=thread_id)
                thread.members.add(user1)
                return thread
            except:
                return None
        thread = Thread.objects.exclude(id=self.exception_thread_id).filter(members=user1).filter(members=user2).first()
        print(user1, user2)
        if thread is None:
            thread = Thread.objects.create()
            thread.members.add(user1, user2)
            print(thread)
        if members_list:
            members = []
            for member in thread.members.all():
                members.append(member.id)
            print(members)
            return {"members": members, "thread": thread}
        return thread

    @database_sync_to_async
    def create_chat_message(self, thread, user, msg, images=[], location=None):
        chat_message = ChatMessage(thread=thread, user=user, message=msg)
        attached_images = []
        chat_message.save()
        for image_id in images:
            image_obj = Image.objects.get(id=image_id)
            chat_message.attached_images.add(image_obj)
            attached_images.append({"id": image_obj.id, "image": image_obj.image.url})
        chat_message.save()
        if location:
            location = Location.objects.create(
                latitude=location["latitude"], longitude=location["longitude"]
            )
            chat_message.location = location
            chat_message.save()
        else:
            pass
        return {"chat_message": chat_message, "images": attached_images}


class PostConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        # Connect to the websocket group
        await self.channel_layer.group_add("posts", self.channel_name)
        await self.send({"type": "websocket.accept"})

    async def websocket_receive(self, event):
        print("HELLO GUYS")
        print(event)
        # Handle incoming messages of type websocket.receive
        # You can process the received message here if needed
        await self.channel_layer.group_send(
            "posts", {"type": "send_signal", "message": event["text"]}
        )

    async def websocket_disconnect(self, event):
        # Leave the websocket group
        await self.channel_layer.group_discard("posts", self.channel_name)

    async def send_signal(self, event):
        # Receive a post update event and send it to the client
        await self.send({"type": "websocket.send", "text": event["message"]})


class UserConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        # Connect to the websocket group
        await self.channel_layer.group_add("users", self.channel_name)
        await self.send({"type": "websocket.accept"})

    async def websocket_receive(self, event):
        print("hi")
        data = json.loads(event["text"])
        event_type = data.get("type")
        print(data)
        if event_type == "send_comment":
            comment = data.get("comment")
            send_to_user_id = comment.get("sendToId")
            sent_by_user_id = comment.get("sentById")
            text = comment.get("text")
            print("SENDTO", send_to_user_id)
            print("FROM:", sent_by_user_id)
            sent_by_user = await self.get_user_object(sent_by_user_id)
            send_to_user = await self.get_user_object(send_to_user_id)
            comment = await self.create_comment(send_to_user, sent_by_user, text)
            print(comment)
            print("user is tryna send comment")
        # Handle incoming messages of type websocket.receive
        # You can process the received message here if needed
        await self.channel_layer.group_send(
            "users", {"type": "send_signal", "message": event["text"]}
        )

    async def websocket_disconnect(self, event):
        # Leave the websocket group
        await self.channel_layer.group_discard("users", self.channel_name)

    async def send_signal(self, event):
        # Receive a post update event and send it to the client
        print("SEND SIGNAL WORKING ")
        await self.send({"type": "websocket.send", "text": event["message"]})

    @database_sync_to_async
    def get_user_object(self, user_id):
        print("USERID: ", user_id)
        print(BasicUser.objects.get(id=user_id))
        qs = BasicUser.objects.filter(id=user_id)
        print(qs)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj

    @database_sync_to_async
    def create_comment(self, send_to, send_by, text):
        print("send_to: ", send_to)
        print("send_by ", send_by)
        comment = Comment(user=send_by, text=text)
        comment.save()
        send_to.comments.add(comment)
        return comment
