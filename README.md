# edamino
Async api for amino

## Installation: 
`pip install ed-amino`

### Example Bot.
```py
from edamino import Bot, Context, logger

bot = Bot(email='email', password='password', prefix="/")


@bot.on_ready
async def on_ready():
    logger.info('Ready.')


@bot.command('ping')
async def echo(ctx: Context):
    await ctx.reply('Pong!')


if __name__ == '__main__':
    bot.start()
```
![](http://pa1.narvii.com/8168/a50b17297b87ef1269b1631ff409f99ea8cd3570r1-428-599_00.gif)

If you have any problems, please write to this discord https://discord.gg/SfzWs5djpT
