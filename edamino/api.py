from base64 import b64encode
from typing import Optional, Dict, Tuple

DEVICE_ID = "327766716D73766C776A6F767078766740676D61696C2E636F6D5DA1DCD8E8E7C6BDDEFD7128E05113FFE25F6239"


class ContentType:
    AUDIO_AAC = "audio/aac"
    IMAGE_JPG = "image/jpg"
    IMAGE_PNG = "image/png",
    APPLICATION = "application/x-www-form-urlencoded"
    APPLICATION_JSON = 'application/json; charset=utf-8'


class InvalidRequest(Exception):
    pass


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
