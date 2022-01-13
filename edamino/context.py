from typing import Optional

from edamino import Client
from edamino.objects import Message


class Context:

    __slots__ = ('msg', 'client')

    def __init__(self, msg: Message, client: Client) -> None:
        self.msg = msg
        self.client = client

    async def reply(self, message: Optional[str] = None, **kwargs):
        return await self.client.send_message(message=message, chat_id=self.msg.threadId, reply=self.msg.messageId, **kwargs)

    async def send_image(self, image: bytes):
        return await self.client.send_image(image, chat_id=self.msg.threadId)

    async def send_gif(self, gif: bytes):
        return await self.client.send_gif(gif, chat_id=self.msg.threadId)

    async def send_audio(self, audio: bytes):
        return await self.client.send_audio(audio, chat_id=self.msg.threadId)

    async def download_from_link(self, link: str):
        return await self.client.download_from_link(link)

    async def send(self, message: Optional[str] = None, **kwargs):
        return await self.client.send_message(message=message, chat_id=self.msg.threadId, **kwargs)

    async def get_user_info(self):
        return await self.client.get_user_info(self.msg.author.uid)
