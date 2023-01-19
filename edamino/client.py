from contextlib import suppress
from copy import copy
from hashlib import sha1
from hmac import new

from edamino import objects, api
from ujson import dumps, loads
from aiohttp import (ClientSession, ClientWebSocketResponse,
                     WSServerHandshakeError, ContentTypeError)
from typing import (Optional, Dict, Tuple, List, Literal, Any, Union)
from time import time, timezone
from base64 import b64encode
from binascii import hexlify
from os import urandom
from uuid import UUID

__all__ = ['Client']


def get_timestamp() -> int:
    return int(time() * 1000)


class Client:
    __slots__ = ('ndc_id', 'session', 'headers', 'proxy')

    ndc_id: str
    proxy: Optional[str]
    session: ClientSession
    headers: Dict[str, str]

    @property
    def sid(self) -> str:
        return self.headers["NDCAUTH"][4:]

    @sid.setter
    def sid(self, sid: str) -> None:
        self.headers["NDCAUTH"] = f"sid={sid}"

    @property
    def uid(self) -> str:
        return self.headers["AUID"]

    @uid.setter
    def uid(self, uid: str) -> None:
        self.headers["AUID"] = uid

    @property
    def device_id(self) -> str:
        return self.headers["NDCDEVICEID"]

    @device_id.setter
    def device_id(self, device_id: str) -> None:
        self.headers["NDCDEVICEID"] = device_id

    def __init__(self,
                 device_id: Optional[str] = None,
                 com_id: int = 0,
                 proxy: Optional[str] = None,
                 session: Optional[ClientSession] = None) -> None:
        self.proxy = proxy
        self.set_ndc(com_id)
        self.headers = {
            "Content-Type": api.ContentType.APPLICATION_JSON,
            "User-Agent": "Apple iPhone14,2 iOS v16.2 Main/3.13.1",
            "NDCDEVICEID":
            device_id if device_id is not None else api.DEVICE_ID
        }
        self.session = session if session is not None else ClientSession(
            json_serialize=dumps)

    async def __aexit__(self, *args) -> None:
        await self.session.close()

    async def __aenter__(self) -> 'Client':
        return self

    def login_sid(self, sid: str, uid: str):
        self.sid = sid
        self.uid = uid

    def set_ndc(self, com_id: int) -> None:
        if com_id != 0:
            self.ndc_id = f"x{com_id}"
        else:
            self.ndc_id = "g"

    async def request(self,
                      method: Literal['POST', 'GET', 'DELETE', 'PUT'],
                      url: str,
                      json: Optional[Dict] = None,
                      full_url: bool = False,
                      data: Optional[Union[str, bytes]] = None,
                      content_type: Optional[str] = None) -> Dict:
        """
        Sending requests in amino.
        """

        headers = self.headers

        if not full_url:
            url = f"https://service.narvii.com/api/v1/{self.ndc_id}/s/{url}"
        if json is not None:
            json['timestamp'] = get_timestamp()
            data = dumps(json)
            headers['NDC-MSG-SIG'] = api.generate_signature(data)

        if content_type is not None:
            headers = copy(self.headers)
            headers['Content-Type'] = content_type

        async with self.session.request(method=method,
                                        url=url,
                                        headers=headers,
                                        data=data,
                                        proxy=self.proxy) as resp:
            try:
                response: Dict = await resp.json(loads=loads)
            except ContentTypeError:
                text = await resp.text()
                raise api.HtmlError(text)

        if resp.status != 200:
            raise api.InvalidRequest(response['api:message'],
                                     response['api:statuscode'], response)

        return response

    async def login(self, email: str, password: str) -> objects.Login:
        data = {
            "email": email,
            "v": 2,
            "secret": f"0 {password}",
            "deviceID": self.device_id,
            "clientType": 100,
            "action": "normal"
        }

        login = objects.Login(
            **await self.request('POST', 'auth/login', json=data))
        self.sid = login.sid
        self.uid = login.auid
        return login

    async def get_my_communities(
            self,
            start: int = 0,
            size: int = 25) -> Tuple[objects.Community, ...]:
        response = await self.request(
            'GET', f'community/joined?v=1&start={start}&size={size}')
        return tuple(
            map(lambda community: objects.Community(**community),
                response['communityList']))

    async def get_info_link(self, link: str) -> objects.LinkInfoExtensions:
        base = objects.BaseLinkInfo(
            **await self.request('GET', f'link-resolution?q={link}'))
        return base.linkInfoV2.extensions

    async def get_user_info(self, user_id: str) -> objects.UserProfile:
        response = await self.request('GET', f'user-profile/{user_id}')
        return objects.UserProfile(**response['userProfile'])

    async def get_link_identify(self, code: str) -> Dict:
        return await self.request(
            'GET',
            f'community/link-identify?q=http%3A%2F%2Faminoapps.com%2Finvite%2F{code}'
        )

    async def join_community(self,
                             invitation_code: Optional[str] = None) -> Dict:
        data = {}
        if invitation_code is not None:
            data["invitationId"] = await self.get_link_identify(invitation_code
                                                                )
        return await self.request('POST', 'community/join', data)

    async def leave_community(self):
        return await self.request('POST', 'community/leave')

    async def upload_media(self, data: bytes, content_type: str) -> str:
        response = await self.request('POST',
                                      "media/upload",
                                      data=data,
                                      content_type=content_type)
        return response['mediaValue']

    async def download_from_link(self, link: str) -> bytes:
        async with self.session.get(link) as response:
            f = await response.read()

        if response.status != 200:
            js_resp: Dict = loads(await response.text())
            raise api.InvalidRequest(js_resp['api:message'],
                                     js_resp['api:statuscode'], js_resp)

        return f

    async def send_image(self, image: bytes, chat_id: str) -> Dict:
        data = {
            "content": None,
            "mediaType": api.MediaType.GIF_AND_IMAGE,
            "mediaUploadValueContentType": "image/jpg",
            "mediaUhqEnabled": True,
            "mediaUploadValue": b64encode(image).decode()
        }
        return await self.request("POST",
                                  f"chat/thread/{chat_id}/message",
                                  json=data)

    async def send_audio(self, audio: bytes, chat_id: str) -> Dict:
        data = {
            "content": None,
            "type": 2,
            "mediaType": api.MediaType.AUDIO,
            "mediaUploadValue": b64encode(audio).decode()
        }
        return await self.request("POST",
                                  f"chat/thread/{chat_id}/message",
                                  json=data)

    async def send_gif(self, image: bytes, chat_id: str) -> Dict:
        data = {
            "content": None,
            "mediaType": api.MediaType.GIF_AND_IMAGE,
            "mediaUploadValueContentType": "image/gif",
            "mediaUhqEnabled": True,
            "mediaUploadValue": b64encode(image).decode()
        }
        return await self.request("POST",
                                  f"chat/thread/{chat_id}/message",
                                  json=data)

    async def send_message(
        self,
        chat_id: str,
        message: Optional[str] = None,
        message_type: int = 0,
        ref_id: Optional[int] = None,
        reply: Optional[str] = None,
        mentions: Optional[List[str]] = None,
        embed: Optional[api.Embed] = None,
        link_snippets_list: Optional[List[api.LinkSnippet]] = None
    ) -> objects.Message:
        if ref_id is None:
            ref_id = int(time() / 10 % 1000000000)

        if mentions is not None:
            mentions = tuple(map(lambda mention: {"uid": mention}, mentions))

        if embed is not None:
            embed = embed.dict()

        if message is not None:
            message = message.replace("<$", "‎‏").replace("$>", "‬‭")

        if link_snippets_list:
            link_snippets_list = [
                snippet.dict() for snippet in link_snippets_list
            ]

        data = {
            "type": message_type,
            "content": message,
            "clientRefId": ref_id,
            "attachedObject": embed,
            "extensions": {
                "mentionedArray": mentions,
                "linkSnippetList": link_snippets_list
            },
        }
        if reply is not None:
            data["replyMessageId"] = reply

        response = await self.request("POST",
                                      f"chat/thread/{chat_id}/message",
                                      json=data)
        return objects.Message(**response['message'])

    async def get_chats(self,
                        start: int = 0,
                        size: int = 100) -> Tuple[objects.Chat, ...]:
        response = await self.request(
            'GET', f'chat/thread?type=joined-me&start={start}&size={size}')
        return tuple(
            map(lambda chat: objects.Chat(**chat), response['threadList']))

    async def ws_connect(self) -> ClientWebSocketResponse:
        timestamp = get_timestamp()
        url = f"{self.device_id}|{timestamp}"
        headers = {
            "NDCAUTH": f"sid={self.sid}",
            "NDCDEVICEID": self.device_id,
            "NDC-MSG-SIG": api.generate_signature(url)
        }
        for i in range(4, 0, -1):
            try:
                return await self.session.ws_connect(
                    f"wss://ws{i}.narvii.com/?signbody={self.device_id}%7C{timestamp}",
                    headers=headers,
                    proxy=self.proxy)
            except WSServerHandshakeError:
                continue

        raise api.WebSocketConnectError("Failed to connect to remote server.")

    async def receive_ws_message(self):
        timestamp = int(time())
        ws = await self.ws_connect()

        while True:
            with suppress(TypeError):
                if time() - timestamp >= 180:
                    ws = await self.ws_connect()
                    timestamp = int(time())

                yield await ws.receive_json(loads=loads)

    async def get_from_id(self,
                          object_id: str,
                          object_type: int = 0) -> objects.LinkInfo:
        data = {
            "objectId": object_id,
            "targetCode": 1,
            "objectType": object_type
        }

        if self.ndc_id == "g":
            url = "https://service.narvii.com/api/v1/g/s/link-resolution"
        else:
            url = f'https://service.narvii.com/api/v1/g/s-{self.ndc_id}/link-resolution'

        base = objects.BaseLinkInfo(
            **await self.request('POST', url, data, True))
        return base.linkInfoV2.extensions.linkInfo

    async def get_chat_info(self, chat_id) -> objects.Chat:
        response = await self.request('GET', f'chat/thread/{chat_id}')
        return objects.Chat(**response['thread'])

    async def get_chat_messages(
            self,
            chat_id: str,
            size: int = 25,
            page_token: Optional[str] = None) -> objects.Messages:
        url = f'chat/thread/{chat_id}/message?v=2&pagingType=t&size={size}'
        if page_token is not None:
            url += f"&pageToken={page_token}"
        response = await self.request('GET', url)

        return objects.Messages(**response)

    async def get_chat_messages_iter(self, chat_id: str, size: int = 100):
        ost: int = size % 100
        whole: int = size // 100
        page_token: Optional[str] = None
        for i in range(whole):
            messages = await self.get_chat_messages(chat_id,
                                                    size=100,
                                                    page_token=page_token)

            page_token = messages.paging.nextPageToken
            yield messages.messageList

        yield (await self.get_chat_messages(chat_id,
                                            size=ost,
                                            page_token=page_token)).messageList

    async def get_chat_users(
            self,
            chat_id: str,
            start: int = 0,
            size: int = 25) -> Tuple[objects.UserProfile, ...]:
        response = await self.request(
            'GET',
            f'chat/thread/{chat_id}/member?start={start}&size={size}&type=default&cv=1.2'
        )
        return tuple(
            map(lambda user: objects.UserProfile(**user),
                response['memberList']))

    async def get_message_info(self, chat_id: str,
                               message_id: str) -> objects.Message:
        response = await self.request(
            'GET', f'chat/thread/{chat_id}/message/{message_id}')
        return objects.Message(**response['message'])

    async def get_blog_info(self, blog_id: str) -> objects.Blog:
        response = await self.request('GET', f'blog/{blog_id}')
        return objects.Blog(**response['blog'])

    async def get_wiki_info(self, wiki_id: str) -> objects.Wiki:
        response = await self.request('GET', f'item/{wiki_id}')
        return objects.Wiki(**response['item'])

    async def check_in(self, tz: int = -timezone // 1000) -> Dict:
        data = {"timezone": tz}
        return await self.request('POST', 'check-in', data)

    async def lottery(self, tz: int = -timezone // 1000):
        data = {"timezone": tz}
        await self.request('POST', "check-in/lottery", data)

    async def edit_profile(self,
                           nickname: Optional[str] = None,
                           content: Optional[str] = None,
                           icon: Optional[str] = None,
                           chat_request_privilege: Optional[str] = None,
                           image_list: Optional[list] = None,
                           caption_list: Optional[list] = None,
                           background_image: Optional[str] = None,
                           background_color: Optional[str] = None,
                           titles: Optional[list] = None,
                           colors: Optional[list] = None,
                           default_bubble_id: Optional[str] = None) -> Dict:
        media_list = []
        data: Dict[str, Any] = {}

        if caption_list is not None:
            for image, caption in zip(image_list, caption_list):
                media_list.append([100, image, caption])
        else:
            if image_list is not None:
                for image in image_list:
                    media_list.append([100, image, None])
        if image_list is not None or caption_list is not None:
            data["mediaList"] = media_list
        if nickname:
            data["nickname"] = nickname
        if icon:
            data["icon"] = icon
        if content:
            data["content"] = content
        if chat_request_privilege:
            data["extensions"] = {
                "privilegeOfChatInviteRequest": chat_request_privilege
            }
        if background_image:
            data["extensions"] = {
                "style": {
                    "backgroundMediaList":
                    [[100, background_image, None, None, None]]
                }
            }
        if background_color:
            data["extensions"] = {
                "style": {
                    "backgroundColor": background_color
                }
            }
        if default_bubble_id:
            data["extensions"] = {"defaultBubbleId": default_bubble_id}
        if titles or colors:
            tlt = []
            for titles, colors in zip(titles, colors):
                tlt.append({"title": titles, "color": colors})

            data["extensions"] = {"customTitles": tlt}

        return await self.request('POST', f'user-profile/{self.uid}', data)

    async def comment_blog(self,
                           blog_id: str,
                           message: Optional[str] = None,
                           sticker_id: Optional[str] = None,
                           reply: Optional[str] = None) -> Dict:
        data = {
            "content": message,
            "stickerId": sticker_id,
            "type": 0,
            "eventSource": "PostDetailView"
        }
        if reply is not None:
            data["respondTo"] = reply
        return await self.request(
            'POST',
            f'blog/{blog_id}/{"comment" if self.ndc_id != "g" else "g-comment"}',
            data)

    async def comment_wiki(self,
                           wiki_id: str,
                           message: Optional[str] = None,
                           sticker_id: Optional[str] = None,
                           reply: Optional[str] = None) -> Dict:
        data = {
            "content": message,
            "stickerId": sticker_id,
            "type": 0,
            "eventSource": "UserProfileView"
        }
        if reply is not None:
            data["respondTo"] = reply
        return await self.request(
            'POST',
            f'item/{wiki_id}/{"comment" if self.ndc_id != "g" else "g-comment"}',
            data)

    async def comment_profile(self,
                              uid: str,
                              message: Optional[str] = None,
                              sticker_id: Optional[str] = None,
                              reply: Optional[str] = None) -> Dict:
        data = {
            "content": message,
            "stickerId": sticker_id,
            "type": 0,
            "eventSource": "UserProfileView"
        }
        if reply is not None:
            data["respondTo"] = reply
        return await self.request(
            'POST',
            f'user-profile/{uid}/{"comment" if self.ndc_id != "g" else "g-comment"}',
            data)

    async def send_active_object(
            self,
            opt_in_ads_flags: int = 2147483647,
            tz: int = -timezone // 1000,
            timers: Optional[Tuple[Dict[str, int], ...]] = None) -> Dict:
        data = {
            "userActiveTimeChunkList": timers,
            "optInAdsFlags": opt_in_ads_flags,
            "timezone": tz
        }

        return await self.request('POST', 'community/stats/user-active-time',
                                  data)

    async def like_blog(self, blog_id: str) -> Dict:
        data = {"value": 4, "eventSource": "UserProfileView"}
        return await self.request('POST',
                                  f"blog/{blog_id}/vote?cv=1.2",
                                  json=data)

    async def like_blogs(self, blog_ids: List[str]) -> Dict:
        data = {"value": 4, "targetIdList": blog_ids}
        return await self.request('POST', f"feed/vote", json=data)

    async def get_online_users(
            self,
            start: int = 0,
            size: int = 25) -> Tuple[objects.UserProfile, ...]:
        response = await self.request(
            "GET",
            f'live-layer?topic=ndtopic:{self.ndc_id}:online-members&start={start}&size={size}'
        )
        return tuple(
            map(lambda user: objects.UserProfile(**user),
                response["userProfileList"]))

    async def get_all_users(self,
                            users_type: Literal['recent', 'banned', 'featured',
                                                'leaders',
                                                'curators'] = "recent",
                            start: int = 0,
                            size: int = 25) -> Tuple[objects.UserProfile, ...]:
        response = await self.request(
            'GET', f'user-profile?type={users_type}&start={start}&size={size}')
        return tuple(
            map(lambda user: objects.UserProfile(**user),
                response['userProfileList']))

    async def activity(self):
        pass

    async def invite_to_chat(self, uids: List[str], chat_id: str) -> Dict:
        data = {"uids": uids}
        return await self.request('POST',
                                  f'chat/thread/{chat_id}/member/invite', data)

    async def send_coins(self,
                         coins: int,
                         blog_id: Optional[str] = None,
                         chat_id: Optional[str] = None,
                         object_id: Optional[str] = None,
                         transaction_id: Optional[str] = None) -> Dict:
        url: str = ""
        if transaction_id is None:
            transaction_id = str(UUID(hexlify(urandom(16)).decode('ascii')))

        data = {
            "coins": coins,
            "tippingContext": {
                "transactionId": transaction_id
            }
        }

        if blog_id is not None:
            url = f"blog/{blog_id}/tipping"

        if chat_id is not None:
            url = f"chat/thread/{chat_id}/tipping"

        if object_id is not None:
            data["objectId"] = object_id
            data["objectType"] = 2
            url = "tipping"

        return await self.request('POST', url, json=data)

    async def subscribe(
        self,
        user_id: str,
        auto_renew: bool = False,
        transaction_id: Optional[str] = None,
    ) -> Dict:
        if transaction_id is None:
            transaction_id = str(UUID(hexlify(urandom(16)).decode('ascii')))
        data = {
            "paymentContext": {
                "transactionId": transaction_id,
                "isAutoRenew": auto_renew
            }
        }
        return await self.request('POST',
                                  f'influencer/{user_id}/subscribe',
                                  json=data)

    async def get_wallet_info(self) -> objects.WalletInfo:
        response = await self.request('GET', 'wallet')
        return objects.WalletInfo(**response['wallet'])

    async def join_chat(self, chat_id: str) -> Dict:
        return await self.request('POST',
                                  f'chat/thread/{chat_id}/member/{self.uid}')

    async def delete_message(self,
                             chat_id: str,
                             message_id: str,
                             as_staff: bool = False,
                             reason: Optional[str] = None) -> Dict:
        data = {"adminOpName": 102}
        if as_staff and reason:
            data["adminOpNote"] = {"content": reason}

        if not as_staff:
            return await self.request(
                'DELETE', f'chat/thread/{chat_id}/message/{message_id}')
        else:
            return await self.request(
                'POST', f'chat/thread/{chat_id}/message/{message_id}/admin',
                data)

    async def follow(self, uids: List[str]) -> Dict:
        data = {"targetUidList": uids}
        return await self.request('POST', f'user-profile/{self.uid}/joined',
                                  data)

    async def unfollow(self, uid: str) -> Dict:
        return await self.request('DELETE',
                                  f'user-profile/{self.uid}/joined/{uid}')

    async def kick_from_chat(self,
                             chat_id: str,
                             uid: str,
                             allow_rejoin: bool = True) -> Dict:
        return await self.request(
            'DELETE',
            f'chat/thread/{chat_id}/member/{uid}?allowRejoin={1 if allow_rejoin else 0}'
        )

    async def get_user_blogs(self,
                             user_id: str,
                             start: int = 0,
                             size: int = 25) -> Tuple[objects.Blog]:
        response = await self.request(
            'GET', f'blog?type=user&q={user_id}&start={start}&size={size}')
        return tuple(
            map(lambda blog: objects.Blog(**blog), response['blogList']))

    async def pin_announcement_from_chat(
            self,
            chat_id: str,
            announcement: str,
            pin_announcement: bool = True) -> Dict:
        data = {
            "extensions": {
                "announcement": announcement,
                "pinAnnouncement": pin_announcement
            }
        }
        return await self.request('POST', f'chat/thread/{chat_id}', data)

    async def edit_chat(self,
                        chat_id: str,
                        title: Optional[str] = None,
                        icon: Optional[str] = None,
                        content: Optional[str] = None,
                        announcement: Optional[str] = None,
                        keywords: List = None,
                        pin_announcement: bool = True,
                        publish_to_global: bool = False,
                        fans_only: bool = None) -> Dict:
        data: Dict[str, Any] = {}

        if title:
            data["title"] = title
        if content:
            data["content"] = content
        if icon:
            data["icon"] = icon
        if keywords:
            data["keywords"] = keywords
        if announcement:
            data["extensions"] = {
                "announcement": announcement,
                "pinAnnouncement": pin_announcement
            }
        if fans_only:
            data["extensions"] = {"fansOnly": fans_only}

        data["publishToGlobal"] = 0 if not publish_to_global else 1

        return await self.request('POST', f'chat/thread/{chat_id}', data)

    async def set_view_only_chat(
            self, chat_id: str, view_only: Literal['enable',
                                                   'disable']) -> Dict:
        return await self.request(
            'POST', f'chat/thread/{chat_id}/view-only/{view_only}')

    async def set_background_chat(self,
                                  chat_id: str,
                                  background: Optional[bytes] = None):
        data = {
            "mediaType": api.MediaType.GIF_AND_IMAGE,
            "mediaUploadValue": b64encode(background).decode(),
            "mediaUploadValueContentType": api.ContentType.IMAGE_JPG
        }
        return await self.request(
            'POST', f'thread/{chat_id}/member/{self.uid}/background', data)

    async def set_default_background_chat(self,
                                          chat_id: str,
                                          background_number: int = 3):
        data = {
            "media": [
                100,
                f"http://static.narvii.com/default-chat-room-background/{background_number}_00.png",
                None
            ]
        }
        return await self.request(
            'POST', f'thread/{chat_id}/member/{self.uid}/background', data)

    async def leave_chat(self, chat_id: str):
        return await self.request('DELETE',
                                  f'chat/thread/{chat_id}/member/{self.uid}')

    async def get_bubbles(self,
                          start: int = 0,
                          size: int = 25) -> Tuple[objects.ChatBubble, ...]:
        response = await self.request(
            'GET',
            f'chat/chat-bubble?type=all-my-bubbles&start={start}&size={size}')
        return tuple(
            map(lambda b: objects.ChatBubble(**b), response["chatBubbleList"]))

    async def delete_bubble(self, bubble_id: str) -> Dict:
        return await self.request('DELETE', f'chat/chat-bubble/{bubble_id}')

    async def set_bubble(self,
                         chat_id: str,
                         bubble_id: str,
                         apply_to_all: bool = False) -> Dict:
        data = {
            "bubbleId": bubble_id,
            "applyToAll": 1 if apply_to_all else 0,
            "threadId": chat_id,
        }
        return await self.request('POST',
                                  'chat/thread/apply-bubble',
                                  json=data)

    async def get_templates(self):
        response = await self.request('GET', 'chat/chat-bubble/templates')
        return tuple(
            map(lambda t: objects.Template(**t), response['templateList']))

    async def create_bubble(self, template_id: str,
                            config) -> objects.ChatBubble:
        response = await self.request(
            'POST',
            f'chat/chat-bubble/templates/{template_id}/generate',
            data=config.get_zip(),
            content_type=api.ContentType.APPLICATION_OCTET_STREAM)
        return objects.ChatBubble(**response['chatBubble'])

    async def update_bubble(self, bubble_id: str, config):
        response = await self.request(
            'POST',
            f'chat/chat-bubble/{bubble_id}',
            data=config.get_zip(),
            content_type=api.ContentType.APPLICATION_OCTET_STREAM)
        return objects.ChatBubble(**response['chatBubble'])

    async def upload_image_bubble(self, image: bytes) -> str:
        response = await self.request(
            'POST',
            'media/upload/target/chat-bubble-thumbnail',
            data=image,
            content_type=api.ContentType.IMAGE_PNG)
        return response['mediaValue']

    async def delete_invite_code(self, invite_id: str) -> Dict:
        return await self.request('DELETE',
                                  f"community/invitation/{invite_id}")

    async def delete_blog(self, blog_id: str) -> Dict:
        return await self.request('DELETE', f"blog/{blog_id}")

    async def delete_wiki(self, wiki_id: str) -> Dict:
        return await self.request('DELETE', f"item/{wiki_id}")

    async def post_blog(self,
                        title: str,
                        content: str,
                        image_list: Optional[List[str]] = None,
                        caption_list: Optional[List] = None,
                        categories_list: Optional[List] = None,
                        backgroundColor: Optional[str] = None,
                        fansOnly: bool = False,
                        extensions: Optional[Dict] = None) -> objects.Blog:
        media_list: Optional[List] = None

        if caption_list and image_list:
            media_list = [[100, image, caption]
                          for image, caption in zip(image_list, caption_list)]

        elif image_list:
            media_list = [[100, image, None] for image in image_list]

        data = {
            "address": None,
            "content": content,
            "title": title,
            "mediaList": media_list,
            "extensions": extensions,
            "latitude": 0,
            "longitude": 0,
            "eventSource": api.SourceTypes.GLOBAL_COMPOSE
        }

        if fansOnly:
            data["extensions"] = {"fansOnly": fansOnly}
        if backgroundColor:
            data["extensions"] = {
                "style": {
                    "backgroundColor": backgroundColor
                }
            }
        if categories_list:
            data["taggedBlogCategoryIdList"] = categories_list

        response = await self.request('POST', f"blog", data)
        return objects.Blog(**response['blog'])

    async def post_wiki(self,
                        title: str,
                        content: Optional[str],
                        icon: Optional[str] = None,
                        image_list: Optional[List[str]] = None,
                        keywords: Optional[str] = None,
                        backgroundColor: Optional[str] = None,
                        fansOnly: bool = False) -> objects.Wiki:
        media_list = [[100, image, None] for image in image_list
                      ] if image_list is not None else None

        data: Dict[str, Any] = {
            "label": title,
            "content": content,
            "mediaList": media_list,
            "eventSource": api.SourceTypes.GLOBAL_COMPOSE
        }

        if icon:
            data["icon"] = icon
        if keywords:
            data["keywords"] = keywords
        if fansOnly:
            data["extensions"] = {"fansOnly": fansOnly}
        if backgroundColor:
            data["extensions"] = {
                "style": {
                    "backgroundColor": backgroundColor
                }
            }

        response = await self.request('POST', "item", data)
        return objects.Wiki(**response)

    async def edit_blog(self,
                        blog_id: str,
                        title: Optional[str] = None,
                        content: Optional[str] = None,
                        image_list: Optional[list] = None,
                        categories_list: Optional[list] = None,
                        background_color: Optional[str] = None,
                        fans_only: bool = False) -> Dict:
        media_list = [[100, image, None] for image in image_list]

        data: Dict[str, Any] = {
            "address": None,
            "mediaList": media_list,
            "latitude": 0,
            "longitude": 0,
            "eventSource": "PostDetailView"
        }

        if title:
            data["title"] = title
        if content:
            data["content"] = content
        if fans_only:
            data["extensions"] = {"fansOnly": fans_only}
        if background_color:
            data["extensions"] = {
                "style": {
                    "backgroundColor": background_color
                }
            }
        if categories_list:
            data["taggedBlogCategoryIdList"] = categories_list

        response = await self.request('POST', f"blog/{blog_id}", data)
        return response

    async def repost_blog(self,
                          content: Optional[str] = None,
                          blogId: Optional[str] = None,
                          wikiId: Optional[str] = None) -> objects.Blog:
        if blogId:
            refObjectId, refObjectType = blogId, api.ObjectTypes.BLOG
        elif wikiId:
            refObjectId, refObjectType = wikiId, api.ObjectTypes.ITEM
        else:
            raise api.SpecifyType()

        data = {
            "content": content,
            "refObjectId": refObjectId,
            "refObjectType": refObjectType,
            "type": 2
        }

        response = await self.request('POST', "blog", data)
        return objects.Blog(**response['blog'])

    async def get_public_chats(self,
                               start: int = 0,
                               size: int = 25) -> Tuple[objects.Chat]:
        response = await self.request(
            'GET', f"live-layer/public-chats?start={start}&size={size}")
        return tuple(map(lambda o: objects.Chat(**o), response["threadList"]))

    async def get_user_wikis(self,
                             user_id: str,
                             start: int = 0,
                             size: int = 25) -> Tuple[objects.Wiki]:
        response = await self.request(
            'GET',
            f"item?type=user-all&start={start}&size={size}&cv=1.2&uid={user_id}"
        )
        return tuple(map(lambda o: objects.Wiki(**o), response["itemList"]))

    async def ban(self,
                  user_id: str,
                  reason: str,
                  ban_type: int = None) -> Dict:
        data = {"reasonType": ban_type, "note": {"content": reason}}
        response = await self.request('POST', f"user-profile/{user_id}/ban",
                                      data)
        return response

    async def unban(self, user_id: str, reason: str) -> Dict:
        data = {"note": {"content": reason}}
        response = await self.request('POST', f"user-profile/{user_id}/unban",
                                      data)
        return response

    async def claim_reputation(self, chat_id: str):
        return await self.request('POST',
                                  f'chat/thread/{chat_id}/avchat-reputation')

    async def get_vc_reputation_info(self, chat_id: str):
        return await self.request('GET',
                                  f'chat/thread/{chat_id}/avchat-reputation')

    async def start_chat(self,
                         invitee_ids: List[str],
                         chat_type: int = 0,
                         content: Optional[str] = None,
                         title: Optional[str] = None,
                         is_global: bool = False,
                         publish_to_global: bool = False) -> objects.Chat:
        data = {
            "title": title,
            "type": chat_type,
            "inviteeUids": invitee_ids,
            "initialMessageContent": content,
            "publishToGlobal": 0 if publish_to_global is False else 1
        }
        if is_global is True:
            data["eventSource"] = "GlobalComposeMenu"

        response = await self.request("POST", url='chat/thread', json=data)
        return objects.Chat(**response["thread"])

    async def send_sticker(self, chat_id: str,
                           sticker_id: str) -> objects.Message:
        data = {
            'content': None,
            'stickerId': sticker_id,
            'type': api.MessageType.STICKER
        }

        response = await self.request('POST', f'chat/thread/{chat_id}/message',
                                      data)
        return objects.Message(**response['message'])

    async def get_user_following(self,
                                 user_id: str,
                                 start: int = 0,
                                 size: int = 25):
        response = await self.request(
            'GET', f'user-profile/{user_id}/joined?start={start}&size={size}')
        return tuple(
            map(lambda user: objects.UserProfile(**user),
                response['userProfileList']))

    async def get_user_followers(self,
                                 user_id: str,
                                 start: int = 0,
                                 size: int = 25):
        response = await self.request(
            'GET', f'user-profile/{user_id}/member?start={start}&size={size}')
        return tuple(
            map(lambda user: objects.UserProfile(**user),
                response['userProfileList']))
