from .client import Client
from .objects import Message
from .api import Embed, LinkSnippet
from typing import (
    List,
    Optional,
    Literal, Callable
)
from contextlib import asynccontextmanager, contextmanager
from ujson import dumps
from aiohttp import ClientWebSocketResponse


class Context:
    __slots__ = ('msg', 'client', 'ws')

    def __init__(self, msg: Message, client: Client, ws: ClientWebSocketResponse) -> None:
        self.msg = msg
        self.client = client
        self.ws = ws

    async def reply(self,
                    message: Optional[str] = None,
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

    async def send_image(self, image: bytes, chat_id: str):
        return await self.client.send_image(image, chat_id=chat_id)

    async def send_gif(self, gif: bytes, chat_id: str):
        return await self.client.send_gif(gif, chat_id=chat_id)

    async def send_audio(self, audio: bytes, chat_id: str):
        return await self.client.send_audio(audio, chat_id=chat_id)

    async def download_from_link(self, link: str):
        return await self.client.download_from_link(link)

    async def send(self,
                   message: Optional[str] = None,
                   message_type: int = 0,
                   ref_id: Optional[int] = None,
                   mentions: Optional[List[str]] = None,
                   embed: Optional[Embed] = None,
                   link_snippets_list: Optional[List[LinkSnippet]] = None,
                   reply: Optional[str] = None):
        return await self.client.send_message(message=message,
                                              chat_id=self.msg.threadId,
                                              message_type=message_type,
                                              ref_id=ref_id,
                                              mentions=mentions,
                                              embed=embed,
                                              link_snippets_list=link_snippets_list,
                                              reply=reply)

    async def get_user_info(self, user_id: str):
        return await self.client.get_user_info(user_id)

    async def invite(self, chat_id: str):
        return await self.client.invite_to_chat(uids=[self.msg.uid], chat_id=chat_id)

    async def follow(self, user_id: str):
        return await self.client.follow([user_id])

    async def unfollow(self, user_id: str):
        return await self.client.unfollow(user_id)

    async def delete_message(self, chat_id: str, message_id: str, as_staff: bool = False, reason: Optional[str] = None):
        return self.client.delete_message(chat_id=chat_id,
                                          message_id=message_id,
                                          reason=reason,
                                          as_staff=as_staff)

    async def kick(self, chat_id: str, user_id: str, allow_rejoin: bool = True):
        return self.client.kick_from_chat(self.msg.threadId, self.msg.uid, allow_rejoin)

    async def join_community(self, code: Optional[str] = None):
        return await self.client.join_community(code)

    async def leave_community(self):
        return await self.client.leave_community()

    async def join_chat(self, chat_id: str):
        return await self.client.join_chat(chat_id)

    async def leave_chat(self, chat_id: str):
        return await self.client.leave_chat(chat_id)

    async def get_info_link(self, link: str):
        return await self.client.get_info_link(link)

    async def get_from_id(self, object_id: str, object_type: int = 0):
        return await self.client.get_from_id(object_id, object_type=object_type)

    async def get_user_blogs(self, user_id: str, start: int = 0, size: int = 25):
        return await self.client.get_user_blogs(user_id, start=start, size=size)

    @asynccontextmanager
    async def typing(self, chat_type: Literal[0, 1, 2] = 2):
        data = {
            "o": {
                "actions": ["Typing"],
                "target": f"ndc://x{self.msg.ndcId}/chat-thread/{self.msg.threadId}",
                "ndcId": self.msg.ndcId,
                "params": {"threadType": chat_type},
                "id": "2713213"
            },
            "t": 304
        }

        try:
            await self.ws.send_str(dumps(data))
            yield
        finally:
            data['t'] = 306
            await self.ws.send_str(dumps(data))

    @asynccontextmanager
    async def recording(self, chat_type: int = 2):
        data = {
            "o": {
                "actions": ["Recording"],
                "target": f"ndc://x{self.msg.ndcId}/chat-thread/{self.msg.threadId}",
                "ndcId": self.msg.ndcId,
                "params": {
                    "threadType": chat_type
                },
                "id": "161486614"
            },
            "t": 304
        }
        try:
            await self.ws.send_str(dumps(data))
            yield
        finally:
            data['t'] = 306
            await self.ws.send_str(dumps(data))

    async def get_chat_messages(self, size: int = 25, page_token: Optional[str] = None):
        return await self.client.get_chat_messages(self.msg.threadId, size, page_token)

    async def start_chat(self,
                         content: Optional[str] = None,
                         chat_type: int = 0,
                         is_global: bool = False,
                         publish_to_global: bool = False):
        return await self.client.start_chat(invitee_ids=[self.msg.uid],
                                            content=content,
                                            chat_type=chat_type,
                                            is_global=is_global,
                                            publish_to_global=publish_to_global)

    async def send_sticker(self, chat_id: str, sticker_id: str):
        return await self.client.send_sticker(chat_id, sticker_id)

    async def get_chat_info(self, chat_id: str):
        return await self.client.get_chat_info(chat_id)

    @contextmanager
    def set_ndc(self, ndc_id: int = 0):
        try:
            self.client.set_ndc(ndc_id)
            yield
        finally:
            self.client.set_ndc(self.msg.ndcId)

    async def get_message_info(self, chat_id: str, message_id: str):
        return await self.client.get_message_info(chat_id, message_id)

    async def actions(self, actions: List[str], thread_type: int, chat_id: Optional[str] = None,
                      ndc_id: Optional[int] = None):
        data = {
            "o": {
                "actions": actions,
                "target": f"ndc://x{self.msg.ndcId}/chat-thread/{self.msg.threadId if chat_id is None else chat_id}",
                "ndcId": self.msg.ndcId if ndc_id is None else ndc_id,
                "params": {
                    "duration": 12800,
                    "membershipStatus": 1,
                    "threadType": thread_type
                },
                "id": "1715976"
            },
            "t": 306
        }
        await self.ws.send_json(data)

    async def join_channel(self, channel_type: int, chat_id: Optional[str] = None, ndc_id: Optional[int] = None):
        data = {
            "o": {
                "ndcId": self.msg.ndcId if ndc_id is None else ndc_id,
                "threadId": self.msg.threadId if chat_id is None else chat_id,
                "channelType": channel_type,
                "id": "10335436"
            },
            "t": 108
        }
        await self.ws.send_json(data)

    async def create_channel(self,
                             chat_id: Optional[str] = None,
                             ndc_id: Optional[int] = None):
        data = {
            "o": {
                "id": "1300666754",
                "ndcId": self.msg.ndcId if ndc_id is None else ndc_id,
                "threadId": self.msg.threadId if chat_id is None else chat_id,
            },
            "t": 200
        }
        await self.ws.send_json(data)

    async def play_video(self,
                         background: str,
                         path: str,
                         title: str,
                         duration: float,
                         chat_id: Optional[str] = None,
                         ndc_id: Optional[int] = None):
        await self.create_channel(chat_id, ndc_id)
        data = {
            "o": {
                "ndcId": self.msg.ndcId if ndc_id is None else ndc_id,
                "threadId": self.msg.threadId if chat_id is None else chat_id,
                "playlist": {
                    "currentItemIndex": 0,
                    "currentItemStatus": 1,
                    "items": [{
                        "author": None,
                        "duration": duration,
                        "isDone": False,
                        "mediaList": [[100, background, None]],
                        "title": title,
                        "type": 1,
                        "url": f"file://{path}"
                    }]
                },
                "id": "3423239"
            },
            "t": 120
        }

        await self.ws.send_json(data)

    async def play_video_is_done(self,
                                 background: str,
                                 path: str,
                                 title: str,
                                 duration: float,
                                 chat_id: Optional[str] = None,
                                 ndc_id: Optional[int] = None):
        data = {
            "o": {
                "ndcId": self.msg.ndcId if ndc_id is None else ndc_id,
                "threadId": self.msg.threadId if chat_id is None else chat_id,
                "playlist": {
                    "currentItemIndex": 0,
                    "currentItemStatus": 2,
                    "items": [{
                        "author": None,
                        "duration": duration,
                        "isDone": True,
                        "mediaList": [[100, background, None]],
                        "title": title,
                        "type": 1,
                        "url": f"file://{path}"
                    }]
                },
                "id": "3423239"
            },
            "t": 120
        }
        await self.ws.send_json(data)

    async def join_thread(self, join_role: int = 1, chat_id: Optional[str] = None, ndc_id: Optional[int] = None):
        data = {
            "o": {
                "ndcId": self.msg.ndcId if ndc_id is None else ndc_id,
                "threadId": self.msg.threadId if chat_id is None else chat_id,
                "joinRole": join_role,
                "id": "10335106"
            },
            "t": 112
        }
        await self.ws.send_json(data)
