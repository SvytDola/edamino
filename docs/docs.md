* [Examples](#example)
    * [Minimal example](#min-example)
    * [Send image](#send-image)
    * [Send gif](#send-gif)
    * [Send sticker](#send-sticker)
    * [Send embed](#send-embed)
    * [Wait for](#wait-for)
* [Events](#event)
    * [on_ready](#on-ready-event)
    * [on_mention](#on-ready-event)
* [Decorator command capabilities](#command)
    * [Additional parameters](#command-parameters)


<br><br>
# Examples <a id=example>
## Minimal example <a id=min-example>

```py
from edamino import Bot, Context

bot = Bot('email', 'password', 'prefix')


@bot.command('ping')
async def on_ping(ctx: Context):
    await ctx.reply('Pong!')


bot.start()
```

## Send image <a id=send-image>

```py
from edamino import Bot, Context
from edamino.api import File

bot = Bot('email', 'password', 'prefix')


@bot.command('image')
async def on_image(ctx: Context):
    image = File.load('path_to_file')
    await ctx.send_image(image)

    # You can also upload an image asynchronously

    image = await File.async_load('path_to_file')
    await ctx.send_image(image)

    # You can also download yourself

    with open('path_to_file', 'rb') as file:
        image = file.read()

    await ctx.send_image(image)

    # You can even download an image from the internet

    image = await ctx.download_from_link('link_to_image')
    await ctx.send_image(image)


bot.start()
```

## Send sticker <a id=send-sticker>

```py
from edamino import Bot, Context

bot = Bot('email', 'password', 'prefix')


@bot.command('sticker')
async def on_gif(ctx: Context):
    await ctx.send_sticker('sticker id')


bot.start()
```

## Send embed <a id=send-embed>

```py
from edamino import Bot, Context
from edamino.api import Embed

bot = Bot('email', 'password', 'prefix')


@bot.command('embed')
async def on_embed(ctx: Context):
    embed = Embed(
        title=ctx.msg.author.nickname,
        object_type=0,
        object_id=ctx.msg.author.uid,
        content="lalala"
    )
    await ctx.send(embed=embed)


bot.start()
```
## Wait for <a id=wait-for>
**NOTE: The `bot.wait_fro` necessary if you want to receive the following message..**

```py
from edamino import Bot, Context
from edamino.objects import Message

bot = Bot('email', 'password', 'prefix')


@bot.command('check')
async def on_check(ctx: Context):
    def check(m: Message):
        return m.content == 'Sh'

    msg = await bot.wait_for(check=check)
    await ctx.send('Ok', reply=msg.messageId)

bot.start()
```

# Events <a id=event>

## `on_ready` <a id=on-ready-event>

**NOTE: The `on_ready` event is designed to find out when the bot will start its work. It takes the bot global profile
as the parameter.**

```py
from edamino import Bot, logger
from edamino.objects import UserProfile

bot = Bot(email='email', password='password', prefix="/")


@bot.event()
async def on_ready(profile: UserProfile):
    logger.info(f'{profile.nickname} ready')


bot.start()
```

## `on_mention` <a id=on-mention-event>

**NOTE: The `on_mention` event is triggered if the bot is mentioned or responded to.**

```py
from edamino import Bot, Context

bot = Bot(email='email', password='password', prefix="/")


@bot.event()
async def on_mention(ctx: Context):
    await ctx.reply('lala')


bot.start()
```
