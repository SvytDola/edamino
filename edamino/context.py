from .client import Client
from .objects import Message
from .api import Embed, LinkSnippet
from typing import (
    List,
    Optional
)
from contextlib import asynccontextmanager
from ujson import dumps

class Context:
    __slots__ = ('msg', 'client', 'ws')

    def __init__(self, msg: Message, client: Client, ws) -> None:
        self.msg = msg
        self.client = client
        self.ws = ws

    async def reply(self,
                    message: str,
                    message_type: int = 0,
                    ref_id: Optional[int] = None,
                    mentions: Optional[List[str]] = None,
                    embed: Optional[Embed] = None,
                    link_snippets_list: Optional[List[LinkSnippet]] = None):
        return await self.client.send_message(message=message,
                                              chat_id=self.msg.threadId,
                                              reply=self.msg.messageId,
                                              message_type=message_type,
                                              ref_id=ref_id,
                                              mentions=mentions,
                                              embed=embed,
                                              link_snippets_list=link_snippets_list)

    async def send_image(self, image: bytes):
        return await self.client.send_image(image, chat_id=self.msg.threadId)

    async def send_gif(self, gif: bytes):
        return await self.client.send_gif(gif, chat_id=self.msg.threadId)

    async def send_audio(self, audio: bytes):
        return await self.client.send_audio(audio, chat_id=self.msg.threadId)

    async def download_from_link(self, link: str):
        return await self.client.download_from_link(link)

    async def send(self,
                   message: str,
                   message_type: int = 0,
                   ref_id: Optional[int] = None,
                   mentions: Optional[List[str]] = None,
                   embed: Optional[Embed] = None,
                   link_snippets_list: Optional[List[LinkSnippet]] = None):
        return await self.client.send_message(message=message,
                                              chat_id=self.msg.threadId,
                                              message_type=message_type,
                                              ref_id=ref_id,
                                              mentions=mentions,
                                              embed=embed,
                                              link_snippets_list=link_snippets_list)

    async def get_user_info(self):
        return await self.client.get_user_info(self.msg.author.uid)

    async def invite(self, chat_id: str):
        return await self.client.invite_to_chat(uids=[self.msg.author.uid], chat_id=chat_id)

    async def follow(self):
        return await self.client.follow([self.msg.author.uid])

    async def unfollow(self):
        return await self.client.unfollow(self.msg.uid)

    async def delete_message(self, as_staff: bool = False, reason: Optional[str] = None):
        return self.client.delete_message(chat_id=self.msg.threadId,
                                          message_id=self.msg.messageId,
                                          reason=reason,
                                          as_staff=as_staff)

    async def kick(self, allow_rejoin: bool = True):
        return self.client.kick_from_chat(self.msg.threadId, self.msg.author.uid, allow_rejoin)

    async def join_community(self, code: Optional[str] = None):
        return await self.client.join_community(code)

    async def leave_community(self):
        return await self.client.leave_community()

    async def join_chat(self):
        return await self.client.join_chat(self.msg.threadId)

    async def leave_chat(self):
        return await self.client.leave_chat(self.msg.threadId)

    async def get_info_link(self, link: str):
        return await self.client.get_info_link(link)

    async def get_from_id(self, object_id: str, object_type: int = 0):
        return await self.client.get_from_id(object_id, object_type=object_type)

    async def get_user_blogs(self, start: int = 0, size: int = 25):
        return await self.client.get_user_blogs(self.msg.author.uid, start=start, size=size)
    
    @asynccontextmanager
    async def typing(self):
        try:    
            await self.ws.send_str(dumps({"o":{"actions":["Typing"],"target":f"ndc://x{self.msg.ndcId}/chat-thread/{self.msg.threadId}","ndcId": self.msg.ndcId,"params":{"threadType":2},"id":"2713103"},"t":304}))
            yield
        finally:    
            await self.ws.send_str(dumps({"o":{"actions":["Typing"],"target":f"ndc://x{self.msg.ndcId}/chat-thread/{self.msg.threadId}","ndcId": self.msg.ndcId,"params":{"threadType":2},"id":"2713103"},"t":306}))
