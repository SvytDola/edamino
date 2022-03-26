from asyncio import TimeoutError
from pathlib import Path
from re import search
from time import time
from os import environ

from ujson import loads
from .client import Client
from .logger import logger as log
from .context import Context
from .objects import Message, UserProfile, SocketAnswer
from .api import MessageType, MediaType, WebSocketConnectError

from dotenv import load_dotenv
from asyncio import get_event_loop, AbstractEventLoop, iscoroutinefunction, Future, wait_for
from collections import namedtuple
from typing import Optional, List, Union, Tuple, Dict, Callable, Awaitable
from functools import partial
from contextlib import suppress

__all__ = ['Bot']

load_dotenv('.env')

Handler = namedtuple('Handler', ['commands', 'media_types', 'message_types', 'callback', 'description'])

HANDLERS_COMMANDS: List[Handler] = []
HANDLERS_EVENTS: List[Handler] = []
CALLBACKS: List[Callable[[Client], Awaitable[None]]] = []

ON_READY: Optional[Callable] = None
ON_MENTION: Optional[Callable[[Context], Awaitable[None]]] = None


class TheCommandAlreadyExists(Exception):
    pass


class IsNotCoroutineFunction(Exception):
    pass


class ArgumentsNotFound(Exception):
    pass


def get_annotations(handler: Handler, words: List[str], command: str, message: str) -> List:
    args = []
    for count, (name, annotation) in enumerate([item for item in handler.callback.__annotations__.items()][1:]):
        if name == 'args':
            string = message.replace(command, '', 1)
            args.append(string)
        else:
            with suppress(IndexError):
                word = words[count]
                args.append(annotation(word))
                message = message.replace(word, '', 1)
    return args


class Bot:
    # Most of the features are taken from the amsync library :D

    __slots__ = ('email', 'password', 'prefix', 'loop', 'sid', 'uid', 'timestamp', 'ws', 'client', 'futures', 'proxy')

    loop: Optional[AbstractEventLoop]

    def __init__(self, email: str, password: str, prefix: str = "", proxy: Optional[str] = None):
        self.uid = None
        self.sid = None
        self.loop = None
        self.email = email
        self.password = password
        self.prefix = prefix.lower()
        self.timestamp = None
        self.ws = None
        self.proxy = proxy
        self.futures: List[Future] = []
        self.client = None

    def get_context(self, client: Client, msg: Message, ws):
        client_context = Client(session=client.session, device_id=client.device_id, com_id=msg.ndcId, proxy=self.proxy)
        client_context.login_sid(self.sid, self.uid)
        context = Context(msg=msg, client=client_context, ws=ws)
        return context

    def check_cfg(self):
        email = environ.get('email')
        password = environ.get('password')

        if email != self.email:
            self.sid = None
            return

        if password == self.password:
            self.sid = environ.get('sid')
            self.uid = environ.get('uid')
        else:
            self.sid = None

        try:
            self.timestamp = int(environ.get('timestamp'))
            if time() - self.timestamp > 60 * 60 * 12:
                self.sid = None
        except TypeError:
            self.timestamp = int(time())
            self.sid = None

    def update_cfg(self):
        self.timestamp = int(time())
        string = f"sid={self.sid}\n" \
                 f"uid={self.uid}\n" \
                 f"email={self.email}\n" \
                 f"password={self.password}\n" \
                 f"timestamp={self.timestamp}"

        with open('.env', 'w') as file:
            file.write(string)

    @staticmethod
    def event(
            message_types: Optional[Union[List[int], Tuple[int, ...]]] = None,
            media_types: Optional[Union[List[int], Tuple[int, ...]]] = None):

        if not message_types:
            message_types = [MessageType.TEXT]
        if not media_types:
            media_types = [MediaType.TEXT]

        def register_handler(callback):
            global ON_READY, ON_MENTION

            name_callback = callback.__name__

            if name_callback == "on_ready":
                ON_READY = callback
                return callback

            if name_callback == "on_mention":
                ON_MENTION = callback
                return callback

            handler = Handler(
                description=None,
                media_types=tuple(media_types),
                message_types=tuple(message_types),
                callback=callback,
                commands=None
            )
            HANDLERS_EVENTS.append(handler)
            return callback

        return register_handler

    def command(self,
                commands: Union[str, List[str]],
                description: str = "Not description.",
                message_types: Optional[Union[List[int], Tuple[int, ...]]] = None,
                media_types: Optional[Union[List[int], Tuple[int, ...]]] = None,
                prefix: Optional[str] = None):

        if isinstance(commands, str):
            commands = [commands]
        if not message_types:
            message_types = [MessageType.TEXT]
        if not media_types:
            media_types = [MediaType.TEXT]

        prefix = prefix.lower() if prefix is not None else self.prefix
        commands = [f'{prefix}{command}' for command in commands]

        def register_handler(callback):
            if iscoroutinefunction(callback) is False:
                raise IsNotCoroutineFunction(callback.__name__)

            current_command_list = [item for item_list in HANDLERS_COMMANDS for item in item_list.commands]
            for command in commands:
                if command in current_command_list:
                    raise TheCommandAlreadyExists(command)

            handler = Handler(
                commands=commands,
                description=description,
                media_types=tuple(media_types),
                message_types=tuple(message_types),
                callback=callback
            )
            HANDLERS_COMMANDS.append(handler)
            return callback

        return register_handler

    async def __call__handlers(self, data: Dict):
        s = SocketAnswer(**data)
        if self.futures:
            for future in self.futures:
                future.set_result(s)
            self.futures.clear()

        if s.t == 1000:

            msg = s.o.chatMessage
            msg.ndcId = s.o.ndcId

            if msg.uid != self.uid:
                if ON_MENTION is not None:
                    uids = ()
                    with suppress(Exception):
                        uids = (u.uid for u in msg.extensions.mentionedArray)
                    with suppress(Exception):
                        if self.uid in uids or self.uid == msg.extensions.replyMessage.uid:
                            self.loop.create_task(ON_MENTION(self.get_context(self.client, msg, self.ws)))

                for handler in HANDLERS_EVENTS:
                    if msg.type in handler.message_types and msg.mediaType in handler.media_types:
                        context = self.get_context(self.client, msg, self.ws)
                        self.loop.create_task(handler.callback(context))

                if msg.content is not None:
                    command = msg.content.lower()

                    for handler in HANDLERS_COMMANDS:
                        is_command_list = [command.startswith(c) for c in handler.commands]
                        if any(is_command_list):
                            context = self.get_context(self.client, msg, self.ws)
                            if '-h' in msg.content:
                                await context.reply(handler.description)
                                continue

                            args = [context]
                            current_command = handler.commands[is_command_list.index(True)]
                            content = msg.content[len(current_command):]
                            words = content.split()
                            try:
                                args += get_annotations(handler, words, current_command, content)
                            except ValueError as error:
                                log.error(repr(error) + f"\nfunction: {handler.callback.__name__}")
                                continue
                            except ArgumentsNotFound as error:
                                log.info(error)
                                continue
                            if msg.type in handler.media_types and msg.mediaType in handler.media_types:
                                try:
                                    self.loop.create_task(handler.callback(*args))
                                except TypeError as e:
                                    log.error(e)
                            break

    async def __call(self) -> None:
        timestamp: int = int(time())
        self.ws = await self.client.ws_connect()

        if ON_READY:
            await ON_READY()

        if CALLBACKS:
            async def run_while_task(cal) -> None:
                while True:
                    await cal(self.client)

            for callback in CALLBACKS:
                self.loop.create_task(run_while_task(callback))

        while True:
            try:
                if int(time()) - timestamp >= 180:
                    self.ws = await self.client.ws_connect()
                    timestamp = int(time())
                    if ON_READY:
                        await ON_READY()

                    if time() - self.timestamp > 60 * 60 * 12:
                        login = await self.client.login(self.email, self.password)
                        self.sid = login.sid
                        self.uid = login.auid
                        self.update_cfg()

                data = await self.ws.receive_json(loads=loads)
                await self.__call__handlers(data)

            except (TypeError, KeyError, AttributeError, WebSocketConnectError):
                continue

    def start(self,
              loop: Optional[AbstractEventLoop] = None,
              device_id: Optional[str] = None,
              check_updates: bool = True) -> None:

        global ON_READY
        self.check_cfg()
        self.loop = loop if loop is not None else get_event_loop()

        self.client = Client(device_id=device_id, proxy=self.proxy)

        try:
            if check_updates:
                response = self.loop.run_until_complete(
                    self.client.request('GET', 'https://pypi.org/pypi/ed-amino/json', full_url=True))

                version = response['info']['version']

                with open(f'{Path(__file__).parent}/__init__.py') as f:
                    __version__ = search(r"'\d*.\d*.\d*.\d*'", f.read()).group().replace("'", '')
                if __version__ != version:
                    log.info(f'Please update to the latest version: {version}. Current version: {__version__}')

            profile: UserProfile
            if self.sid is None:
                login = self.loop.run_until_complete(self.client.login(self.email, self.password))
                self.sid = login.sid
                self.uid = login.auid
                log.info("Update config.")
                self.update_cfg()
                profile = login.userProfile
            else:
                profile = self.loop.run_until_complete(self.client.get_user_info(self.uid))

            self.client.sid = self.sid
            self.client.uid = self.uid

            if ON_READY:
                ON_READY = partial(ON_READY, profile)

            self.loop.run_until_complete(self.__call())
        except KeyboardInterrupt:
            log.info("Goodbye. ^^")
        finally:
            self.loop.run_until_complete(self.client.session.close())

    @staticmethod
    def background_task(callback: Callable[[Client], Awaitable[None]]):
        if iscoroutinefunction(callback) is False:
            raise IsNotCoroutineFunction(callback.__name__)

        CALLBACKS.append(callback)

        return callback

    async def wait_for(self, check: Callable[[SocketAnswer], bool], timeout: Optional[float] = None) -> SocketAnswer:
        while True:
            index = len(self.futures)
            try:
                future = self.loop.create_future()
                self.futures.append(future)
                msg = await wait_for(future, timeout=timeout)
                if check(msg):
                    return msg
            except TimeoutError:
                del self.futures[index]
                raise TimeoutError("Message not found.")
