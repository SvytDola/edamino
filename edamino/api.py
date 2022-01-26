from base64 import b64encode
from typing import Optional, Dict, Tuple, Union, TypeVar
from zipfile import ZipFile, ZIP_DEFLATED
from io import BytesIO
from ujson import dumps

DEVICE_ID = "3298A71AFE0EA0B7EDDAFA2337B38488E23D8060A98946A75EAE99EBE7FA2F0B4D4212428CB8B2253D"


class ContentType:
    AUDIO_AAC: str = "audio/aac"
    IMAGE_JPG: str = "image/jpg"
    IMAGE_PNG: str = "image/png"
    APPLICATION_URL_ENCODED: str = "application/x-www-form-urlencoded"
    APPLICATION_JSON: str = 'application/json; charset=utf-8'
    APPLICATION_OCTET_STREAM: str = 'application/octet-stream'


class InvalidRequest(Exception):
    def __init__(self, message: str, status: int) -> None:
        super().__init__(message)
        self.message = message
        self.status = status


class WebSocketConnectError(Exception):
    pass


class Embed:
    __slots__ = (
        'object_id',
        'object_type',
        'link',
        'title',
        'content',
        'image'
    )

    def __init__(self,
                 object_id: Optional[str] = None,
                 object_type: Optional[int] = None,
                 link: Optional[str] = None,
                 title: Optional[str] = None,
                 content: Optional[str] = None,
                 image: Optional[str] = None) -> None:
        self.object_id = object_id
        self.object_type = object_type
        self.link = link
        self.title = title
        self.content = content
        self.image = image

    def dict(self) -> Dict:
        return {
            "objectId": self.object_id,
            "objectType": self.object_type,
            "link": self.link,
            "title": self.title,
            "content": self.content,
            "mediaList": [[100, self.image, None]] if self.image is not None else None
        }


class MessageType:
    TEXT: int = 0
    STRIKE: int = 1
    VOICE: int = 2
    STICKER: int = 3
    TYPE_USER_SHARE_EXURL: int = 50
    TYPE_USER_SHARE_USER: int = 51
    VOICE_CHAT_NOT_ANSWERED: int = 52
    VOICE_CHAT_NOT_CANCELLED: int = 53
    VOICE_CHAT_NOT_DECLINED: int = 54
    VIDEO_CHAT_NOT_ANSWERED: int = 55
    VIDEO_CHAT_NOT_CANCELLED: int = 56
    VIDEO_CHAT_NOT_DECLINED: int = 57
    AVATAR_CHAT_NOT_ANSWERED: int = 58
    AVATAR_CHAT_NOT_CANCELLED: int = 59
    AVATAR_CHAT_NOT_DECLINED: int = 60
    DELETE_MESSAGE: int = 100
    GROUP_MEMBER_JOIN: int = 101
    GROUP_MEMBER_LEAVE: int = 102
    CHAT_INVITE: int = 103
    CHAT_BACKGROUND_CHANGED: int = 104
    CHAT_TITLE_CHANGED: int = 105
    CHAT_ICON_CHANGED: int = 106
    VOICE_CHAT_START: int = 107
    VIDEO_CHAT_START: int = 108
    AVATAR_CHAT_START: int = 109
    VOICE_CHAT_END: int = 110
    VIDEO_CHAT_END: int = 111
    AVATAR_CHAT_END: int = 112
    CHAT_CONTENT_CHANGED: int = 113
    SCREEN_ROOM_START: int = 114
    SCREEN_ROOM_END: int = 115
    CHAT_HOST_TRANSFERED: int = 116
    TEXT_MESSAGE_FORCE_REMOVED: int = 117
    CHAT_REMOVED_MESSAGE: int = 118
    TEXT_MESSAGE_REMOVED_BY_ADMIN: int = 119
    CHAT_TIP: int = 120
    CHAT_PIN_ANNOUNCEMENT: int = 121
    VOICE_CHAT_PERMISSION_OPEN_TO_EVERYONE: int = 122
    VOICE_CHAT_PERMISSION_INVITED_AND_REQUESTED: int = 123
    VOICE_CHAT_PERMISSION_INVITE_ONLY: int = 124
    CHAT_VIEW_ONLY_ENABLED: int = 125
    CHAT_VIEW_ONLY_DISABLED: int = 126
    CHAT_UNPIN_ANNOUNCEMENT: int = 127
    CHAT_TIPPING_ENABLED: int = 128
    CHAT_TIPPING_DISABLED: int = 129
    TIMESTAMP_MESSAGE: int = 65281
    WELCOME_MESSAGE: int = 65282
    INVITE_MESSAGE: int = 65283
    ALL: Tuple[int, ...] = (
        TEXT,
        STRIKE,
        VOICE,
        STICKER,
        TYPE_USER_SHARE_EXURL,
        TYPE_USER_SHARE_USER,
        VOICE_CHAT_NOT_ANSWERED,
        VOICE_CHAT_NOT_CANCELLED,
        VOICE_CHAT_NOT_DECLINED,
        VIDEO_CHAT_NOT_ANSWERED,
        VIDEO_CHAT_NOT_CANCELLED,
        VIDEO_CHAT_NOT_DECLINED,
        AVATAR_CHAT_NOT_ANSWERED,
        AVATAR_CHAT_NOT_CANCELLED,
        AVATAR_CHAT_NOT_DECLINED,
        DELETE_MESSAGE,
        GROUP_MEMBER_JOIN,
        GROUP_MEMBER_LEAVE,
        CHAT_INVITE,
        CHAT_BACKGROUND_CHANGED,
        CHAT_TITLE_CHANGED,
        CHAT_ICON_CHANGED,
        VOICE_CHAT_START,
        VIDEO_CHAT_START,
        AVATAR_CHAT_START,
        VOICE_CHAT_END,
        VIDEO_CHAT_END,
        AVATAR_CHAT_END,
        CHAT_CONTENT_CHANGED,
        SCREEN_ROOM_START,
        SCREEN_ROOM_END,
        CHAT_HOST_TRANSFERED,
        TEXT_MESSAGE_FORCE_REMOVED,
        CHAT_REMOVED_MESSAGE,
        TEXT_MESSAGE_REMOVED_BY_ADMIN,
        CHAT_TIP,
        CHAT_PIN_ANNOUNCEMENT,
        VOICE_CHAT_PERMISSION_OPEN_TO_EVERYONE,
        VOICE_CHAT_PERMISSION_INVITED_AND_REQUESTED,
        VOICE_CHAT_PERMISSION_INVITE_ONLY,
        CHAT_VIEW_ONLY_ENABLED,
        CHAT_VIEW_ONLY_DISABLED,
        CHAT_UNPIN_ANNOUNCEMENT,
        CHAT_TIPPING_ENABLED,
        CHAT_TIPPING_DISABLED,
        TIMESTAMP_MESSAGE,
        WELCOME_MESSAGE,
        INVITE_MESSAGE
    )


class MediaType:
    TEXT: int = 0
    AUDIO: int = 110
    GIF_AND_IMAGE: int = 100
    STICKER: int = 113
    ALL: Tuple[int, int, int, int] = (TEXT, AUDIO, GIF_AND_IMAGE, STICKER)


class File:

    @staticmethod
    def load(path: str) -> bytes:
        with open(path, 'rb') as file:
            data = file.read()
        return data


class LinkSnippet:
    __slots__ = (
        'link',
        'media_upload_value',
        'media_type',
        'media_upload_value_content_type'
    )

    def __init__(self,
                 link: str,
                 media_upload_value: bytes,
                 media_type: int = 100,
                 media_upload_value_content_type: str = "image/png"):
        self.link = link
        self.media_upload_value = b64encode(media_upload_value).decode()
        self.media_type = media_type
        self.media_upload_value_content_type = media_upload_value_content_type

    def dict(self) -> Dict:
        return {
            "link": self.link,
            "mediaType": self.media_type,
            "mediaUploadValue": self.media_upload_value,
            "mediaUploadValueContentType": self.media_upload_value_content_type
        }


Path = TypeVar("Path", bound=str)


class Slot:
    __slots__ = (
        'image',
        'x',
        'y',
        'align',
        'sticker_id',
        'path'
    )

    def __init__(self,
                 image: Union[Path, bytes],
                 align: int,
                 x: int,
                 y: int,
                 sticker_id: Optional[str] = None) -> None:
        if isinstance(image, str):
            self.image = File.load(image)
        self.x = x
        self.y = y
        self.align = align
        self.sticker_id = sticker_id
        self.path = f"a{self.align}x{self.x}y{self.y}.png"

    def dict(self):
        return {
            "y": self.y,
            "path": self.path,
            "align": self.align,
            "x": self.x,
            "stickerId": self.sticker_id
        }


class AllowedSlot:
    __slots__ = (
        'x',
        'y',
        'align'
    )
    x: int
    y: int
    align: int

    def __init__(self, x: int, y: int, align: int):
        self.x = x
        self.y = y
        self.align = align

    def dict(self):
        return {
            "y": self.y,
            "align": self.align,
            "x": self.x
        }


class ChatBubbleConfig:
    __slots__ = (
        'image',
        'template_id',
        'name',
        'cover_image_url',
        'preview_background_url',
        'color',
        'link_color',
        'slots',
        'content_insets',
        'allowed_slots',
        'zoom_point'
    )

    def __init__(self,
                 image_or_path: Union[bytes, Path],
                 name: Optional[str] = 'Custom bubble',
                 color: Optional[str] = "#ffffff",
                 link_color: Optional[str] = '#ffffff',
                 slots: Optional[Tuple[Slot, ...]] = None,
                 cover_image_url: Optional[str] = None,
                 preview_background_url: Optional[str] = None,
                 allowed_slots: Optional[Tuple[AllowedSlot, ...]] = None,
                 content_insets: Optional[Tuple[int, int, int, int]] = None,
                 zoom_point: Optional[Tuple[int, int]] = None,
                 template_id: Optional[str] = None) -> None:

        if content_insets is None:
            content_insets = (40, 65, 35, 17)

        if zoom_point is None:
            zoom_point = (58, 43)

        self.content_insets = content_insets
        self.image = image_or_path
        self.template_id = template_id
        self.name = name
        self.cover_image_url = cover_image_url
        self.preview_background_url = preview_background_url
        self.color = color
        self.link_color = link_color
        self.slots = slots
        self.content_insets = content_insets
        self.allowed_slots = allowed_slots
        self.zoom_point = zoom_point

    def get_zip(self) -> bytes:
        config = {
            "templateId": self.template_id,
            "contentInsets": self.content_insets,
            "coverImage": self.cover_image_url,
            "id": "a7ee5618-a7aa-47ed-b68d-80088a0606e6",
            "name": self.name,
            "previewBackgroundUrl": self.preview_background_url,
            "slots": (slot.dict() for slot in self.slots) if self.slots is not None else None,
            "version": 1,
            "vertexInset": 0,
            "bubbleType": 1,
            "zoomPoint": self.zoom_point,
            'authors': 'Svyt Dola#2666 & Resq#5909',
            "color": self.color,
            "linkColor": self.link_color,
            "allowedSlots": (slot.dict() for slot in self.allowed_slots) if self.allowed_slots else None,
        }
        fm = BytesIO()

        with ZipFile(fm, 'w', ZIP_DEFLATED) as zip_arc:
            if isinstance(self.image, str):
                zip_arc.write(self.image)
                config["backgroundPath"] = self.image
            else:
                zip_arc.writestr('background.png', self.image)
                config["backgroundPath"] = 'background.png'
            zip_arc.writestr('config.json', dumps(config).encode())

            if self.slots is not None:
                for slot in self.slots:
                    zip_arc.writestr(slot.path, slot.image)

        return fm.getvalue()
