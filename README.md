![Logo. Created by Resq#5909](https://media.discordapp.net/attachments/807254355127566357/947572597481152582/PicsArt_02-27-10.13.56.png?width=600&height=200)

# edamino
An unofficial python wrapper for the async Amino API, based off aiohttp.


![PyPI](https://img.shields.io/pypi/v/ed-amino.svg?style=flat-square)
![PyPI - License](https://img.shields.io/pypi/l/ed-amino.svg?style=flat-square)


# Installing
```
pip install ed-amino
```

# Example
```py
from edamino import Bot, Context, logger
from edamino.objects import UserProfile

bot = Bot(email='email', password='password', prefix="/")


@bot.event()
async def on_ready(profile: UserProfile):
    logger.info(f'{profile.nickname} ready')
    

@bot.command('ping')
async def echo(ctx: Context):
    await ctx.reply('Pong!')


if __name__ == '__main__':
    bot.start()
```



![](https://media.discordapp.net/attachments/868188677602422804/931159730393591870/anim.gif)

# Examples

 - [You can see all the examples at this link.](https://github.com/SvytDola/edamino/blob/master/docs/docs.md)


# Contact

If you encounter a bug, please open an [issue].

[issue]: https://github.com/SvytDola/edamino/issues

- [Discord Server](https://discord.gg/SfzWs5djpT)


# Translations

This README is available in other languages:

- [Spanish](https://github.com/drevenzz/DocsEdAminoSpanish)

Only this README file is guaranteed to be up-to-date.
