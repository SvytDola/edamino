from time import time
from os import environ

from ujson import loads
from .client import Client
from .logger import logger as log
from .context import Context
from .objects import Message
from .api import MessageType, MediaType, WebSocketConnectError

from dotenv import load_dotenv
from asyncio import get_event_loop, AbstractEventLoop, iscoroutinefunction
from collections import namedtuple
from typing import Optional, List, Union, Tuple, Dict, Callable

load_dotenv('.env')

Handler = namedtuple('Handler', ['media_types', 'message_types', 'callback', 'description', 'annotations'])
HANDLERS_COMMANDS: Dict[str, Handler] = {}
HANDLERS_EVENTS: List[Handler] = []
ON_READY: Optional[Callable] = None


class TheCommandAlreadyExists(Exception):
    pass

class IsNotCorutineFunction(Exception):
    pass

class Bot:
    __slots__ = ('email', 'password', 'prefix', 'loop', 'sid', 'uid', 'timestamp', 'ws')

    def __init__(self, email: str, password: str, prefix: str = ""):
        self.uid = None
        self.sid = None
        self.loop = None
        self.email = email
        self.password = password
        self.prefix = prefix
        self.timestamp = None
        self.ws = None

    def get_context(self, client: Client, msg: Message, ws):
        client_context = Client(session=client.session, device_id=client.device_id, com_id=msg.ndcId)
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
            global ON_READY
            if callback.__name__ == "on_ready":
                ON_READY = callback
                return callback

            handler = Handler(
                description=None,
                media_types=tuple(media_types),
                message_types=tuple(message_types),
                callback=callback,
                annotations=None
            )
            HANDLERS_EVENTS.append(handler)
            return callback

        return register_handler

    def command(self,
                command: str,
                description: str = "Not description.",
                message_types: Optional[Union[List[int], Tuple[int, ...]]] = None,
                media_types: Optional[Union[List[int], Tuple[int, ...]]] = None):

        command = command.lower()
        if not message_types:
            message_types = [MessageType.TEXT]
        if not media_types:
            media_types = [MediaType.TEXT]

        def register_handler(callback):
            if iscoroutinefunction(callback) is False:
                raise IsNotCorutineFunction(callback.__name__)
            
            annotations = [annotation for annotation in callback.__annotations__.values()][1:]
            handler = Handler(
                description=description,
                media_types=tuple(media_types),
                message_types=tuple(message_types),
                callback=callback,
                annotations=tuple(annotations)
            )
            ncommand = f"{self.prefix}{command}"
            
            if ncommand in HANDLERS_COMMANDS:
                raise TheCommandAlreadyExists(ncommand)
            
            HANDLERS_COMMANDS[ncommand] = handler

            return callback

        return register_handler

    async def __call(self, client: Client) -> None:
        self.ws = await client.ws_connect()
        if ON_READY:
            await ON_READY()

        while True:
            try:
                if self.ws.closed:
                    if time() - self.timestamp > 60 * 60 * 12:
                        login = await client.login(self.email, self.password)
                        log.info('Login.')
                        self.sid = login.sid
                        self.uid = login.auid
                        self.update_cfg()

                    self.ws = await client.ws_connect()
                    log.info('Reconnected.')

                data = await self.ws.receive_json(loads=loads)
                if data['t'] == 1000:
                    msg = Message(**data['o']['chatMessage'], ndcId=data['o']['ndcId'])

                    if msg.author.uid != self.uid:
                        for handler in HANDLERS_EVENTS:
                            if msg.type in handler.message_types and msg.mediaType in handler.media_types:
                                context = self.get_context(client, msg, self.ws)
                                self.loop.create_task(handler.callback(context))

                        if msg.content is not None:
                            words = msg.content.split(" ")
                            command = words[0].lower()
                            handler = HANDLERS_COMMANDS[command]
                            context = self.get_context(client, msg, self.ws)

                            if '-h' in msg.content:
                                await context.reply(handler.description)
                                continue

                            args = [context]

                            try:
                                if handler.annotations:

                                    if words[1:]:
                                        for word, annotation in zip(words[1:], handler.annotations):
                                            args.append(annotation(word))
                                    else:
                                        continue
                            except ValueError as error:
                                log.error(repr(error) + f"\nfunction: {handler.callback.__name__}")
                                continue
                            if msg.type in handler.media_types and msg.mediaType in handler.media_types:
                                self.loop.create_task(handler.callback(*args))

            except (TypeError, KeyError, AttributeError, WebSocketConnectError):
                continue

    def start(self, loop: Optional[AbstractEventLoop] = None, device_id: Optional[str] = None) -> None:
        self.check_cfg()
        self.loop = loop if loop is not None else get_event_loop()

        client = Client(device_id=device_id)
        try:
            if self.sid is None:
                login = self.loop.run_until_complete(client.login(self.email, self.password))
                self.sid = login.sid
                self.uid = login.auid
                log.info("Update config.")
                self.update_cfg()

            client.sid = self.sid
            client.uid = self.uid
            self.loop.run_until_complete(self.__call(client))
        except KeyboardInterrupt:
            log.info("Goodbye. ^^")
        finally:
            self.loop.run_until_complete(client.session.close())
